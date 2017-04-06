'''
Created on 12/09/2013

@author: Javier Cruce%A4o
'''
# Importar librerias necesarias
# interfaz grafica
from PyQt4 import QtCore, QtGui, uic
# Comunicacion con sistema y manejo de puerto serie
import os, sys, serial, time
# Importar librerias para manejo de protocolos VISA
from pyvisa.vpp43 import visa_library
visa_library.load_library( "visa32.dll" )
import pyvisa.visa as visa

#Funcion para pasar datos como si fueran un archivo de texto
from StringIO import StringIO

# Manejo numerico de datos
import numpy as np
# Librerias para graficar en el ploter
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigatioToolbar
from matplotlib.figure import Figure

class canvas( FigureCanvas ):

    def __init__( self, parent ):
        # Se instancia el objeto figure
        self.fig = Figure()
        # Se define la grafica en coordenadas polares
        self.axes = self.fig.add_subplot( 111 )

        # Se define una grilla
        self.axes.grid( True )

        # se inicializa FigureCanvas
        FigureCanvas.__init__( self, self.fig )
        # se define el widget padre
        self.setParent( parent )
        # se define el widget como expandible
        FigureCanvas.setSizePolicy( self,
                QtGui.QSizePolicy.Expanding,
                QtGui.QSizePolicy.Expanding )
        # se notifica al sistema de la actualizacion
        # de la politica
        FigureCanvas.updateGeometry( self )
        self.fig.canvas.draw()


class Test_Dilatometria ( QtCore.QThread ):
    #Inicio de la clase Qthread
    def __init__ ( self ):
        QtCore.QThread.__init__( self )
        self.exiting = False
    #Funcion que va a ser llamada desde otro proceso para iniciar este hilo que lleva a 
    #cabo la medicion
    def test ( self, outfile, s_port, multimeter ):
        #Configuracion de puerto serie para leer valores del LVDT
        self.ser = serial.Serial( port = s_port,
                          baudrate = 9600,
                          parity = serial.PARITY_NONE,
                          stopbits = 1,
                          bytesize = 8,
                          timeout = 2 )
        #Configuracion de Multimetro Agilent 33410A paqra leer termocupla
        self.multimeter = visa.instrument( multimeter )
        self.multimeter.write( '*CLS' )
        time.sleep( 0.1 )
        self.multimeter.write( 'CONF:VOLT:DC AUTO,MAX' )
        time.sleep( 0.5 )
        self.multimeter.write( 'INIT' )
        time.sleep( 0.5 )
        #Otras configuraciones
        self.time_stamp = 0
        self.savedata = False
        self.outfile = outfile
        self.start()

    #Esta funcion leera continuamente los dispositivos hasta finalizar el ensayo
    def run ( self ):
        #Cambia el mensaje enm el dysplay secundario del multimetro
        self.multimeter.write( 'DISP:WIND2:TEXT "Midiendo ..."' )
        #Variable bandera que indica que es la primera vez qwue corre el proceso
        first = True
        
        while not self.exiting:
            #===================================================================
            # Si es la primera vez que corre el programa va a abrir el archivo de salida 
            # sobrescribiendo el existente
            #===================================================================
            if first:
                fsock = open( self.outfile, 'w' )
                self.zero_time = time.time()
                first = False
            #===================================================================
            # Si no es la primera vez que corre va abrir el archivo de salida de modo que 
            # adjunte los nuevos datos al final del archivo con el que se esta trabajando 
            #===================================================================
            else:
                fsock = open( self.outfile, 'a' )
                self.time_stamp = time.time() - self.zero_time
            #===================================================================
            # El controlador del LVDT envia datos continuamente desde que se enciende.
            # Para evitar datos truncos se vacia el bufer del puerto serie. 
            #===================================================================
            
            if self.ser.inWaiting() > 0:
                self.ser.read( self.ser.inWaiting() )
                
#           Luego se lee una linea de los datos que fueron enviados por el controlador
            line = self.ser.readline()
            # y se toma una lectura del multimetrlo
            temp_data = self.multimeter.ask( 'READ?' )
            # Se comprueba la longitud de la linea leida desde el controlasdor del LVDT, 
            # la misma debe ser de 14 carateres de longitud para quec este completa y estemos seguros
            # de que los datos no esten truncos. 
            l = len( line ) 
            if l == 14:
                # La salida que me manda el puerto es una cadena con 14 caracteres
#                 temp_data = line[0:4] # Los 5 primeros caracteres dan un valor de temperatura que se va
                                        # a tomar con el multimetro
                lvdt_data = int (line[6:12])*(-1)*1.56425E-4   # Los otros restantes un valor de voltaje. Se los multiplica por -1 por una 
                                                    # conveniencia en la representacion grafica
                                                    # 1.56425E-4 es el factor de calibracion a mm
                
                
                temp_data = float ( temp_data ) * 1000
                
                Y = 25.39459 * temp_data 
                Y-= 0.44494 * temp_data ** 2 
                Y+= 0.05652 * temp_data ** 3 
                Y-= 0.00412 * temp_data ** 4 
                Y+= 0.0011 * temp_data ** 5 
                Y-= 1.39776E-4 * temp_data ** 6 
                Y+= 4.40583E-6 * temp_data ** 7 
                Y+= 7.709E-8 * temp_data ** 8
                
                data = [self.time_stamp, Y, lvdt_data]                
                
                if self.savedata:
                    self.multimeter.write( 'DISP:WIND2:TEXT "Guardando..."' )
                    line = str ( data[0] ) + '\t' + str ( data[1] ) + '\t' + str ( data[2] ) + '\n'
                    print line
                    fsock.write( line )
                    fsock.close()
    
                self.emit( QtCore.SIGNAL ( "LVDT_readsignal(PyQt_PyObject)" ), data )
            elif len( line ) == 0:  # si deja de recibir datos sale? del programita...
                continue
        self.ser.close()
        self.multimeter.write( 'DISP:WIND2:TEXT:CLEAR' )
        fsock.close()
        self.exit()

    def __del__( self ):
        self.multimeter.write( 'DISP:WIND2:TEXT:CLEAR' )
        self.exiting = True
        self.ser.close()
        self.wait()

class Main( QtGui.QMainWindow ):
    """La ventana principal de la aplicacion."""

    def __init__( self ):

        #Inicializamos interfaz graica---------------------------
        QtGui.QMainWindow.__init__( self )

        # Cargamos la interfaz desde el archivo .ui
#         self.ui = Ui_MainWindow()
#         self.ui.setupUi( self)
        uifile = os.path.join( 
             os.path.abspath( 
                 os.path.dirname( __file__ ) ), '../UI/DilatometroUI.ui' )
        uic.loadUi( uifile, self )
        #--------------------------------------------------------

        # Lista puertos serie y los agrega a los menu de seleccion de puertos
        for i in range ( 50 ):
            try:
                s = serial.Serial( i )
#                 self.cbx_AG34401A_serial_port.addItem( s.portstr, s.portstr )
                self.cbx_LVDT_serial_port.addItem( s.portstr, s.portstr )
                s.close()
            except:
                pass
#         for baudrate in serial.SerialBase.BAUDRATES:
#             if 2400 <= baudrate and baudrate <= 19200:
#                 self.cbx_LVDT_serial_baudrate.addItem( str ( baudrate ), str ( baudrate ) )
#                 self.cbx_AG34401A_serial_baudrate.addItem( str ( baudrate ) , str ( baudrate ) )
        #----------------------------------------------------------------------------------
        # Inicializamos variables necesarias para el manejo de los datos y de los dispositivos

        #-------------------------------------------------------------------------------------
        # Cargamos los procesos que leeran la informacion de los dispositivos-----------------
        #Generamos los planos donde graficaremos los datos--------------------------
        # Inicializando base de ploteo para mainplot--------------------------------
        self.vbl_main = QtGui.QVBoxLayout( self.gb_mainplot )
        self.maincanvas = canvas( self.gb_mainplot )
        self.vbl_main.insertWidget( 0, self.maincanvas )
        #--------------------------------------------------------------------------
        # Inicializando base de ploteo para auxplot_1------------------------------
        self.vbl_aux_1 = QtGui.QVBoxLayout( self.gb_auxplot_1 )
        self.auxcanvas_1 = canvas( self.gb_auxplot_1 )
        self.vbl_aux_1.insertWidget( 0, self.auxcanvas_1 )
        #--------------------------------------------------------------------------
        # Inicializando base de ploteo para auxplot_2------------------------------
        self.vbl_aux_2 = QtGui.QVBoxLayout( self.gb_auxplot_2 )
        self.auxcanvas_2 = canvas( self.gb_auxplot_2 )
        self.vbl_aux_2.insertWidget( 0, self.auxcanvas_2 )
        #--------------------------------------------------------------------------
        # Inicializando base de ploteo para auxplot_1------------------------------
        # self.vbl_aux_3 = QtGui.QVBoxLayout( self.gb_auxplot_3 )
        # self.auxcanvas_3 = canvas( self.gb_auxplot_3 )
        # self.vbl_aux_3.insertWidget( 0, self.auxcanvas_3 )
        #--------------------------------------------------------------------------
        #--------------------------------------------------------------------------
        self.dilatometria = Test_Dilatometria()
        self.read_data = False
        #Conectamos seniales de los threads con funciones de manejo de datos---------------
        self.connect( self.dilatometria, QtCore.SIGNAL ( "LVDT_readsignal(PyQt_PyObject)" ), self.show_incoming_data )
        #self.connect( self.dilatometria, QtCore.SIGNAL ( "LVDT_readsignal(PyQt_PyObject)" ), self.save_incoming_data )
        #----------------------------------------------------------------------------------

    # Las siguientes 4 funciones son las encargadas de ajustar la escala de la grafica principal
    # por medio de los controles proporcionados al usuario
    @QtCore.pyqtSlot(int)
    def on_sb_xmin_valueChanged( self ):
        self.maincanvas.axes.set_xlim( self.sb_xmin.value(), self.sb_xmax.value() )
        self.maincanvas.draw()
    @QtCore.pyqtSlot( int )
    def on_sb_xmax_valueChanged( self ):
        self.maincanvas.axes.set_xlim( self.sb_xmin.value(), self.sb_xmax.value() )
        self.maincanvas.draw()
    @QtCore.pyqtSlot( int )
    def on_sb_ymin_valueChanged( self ):
        self.maincanvas.axes.set_ylim( self.sb_ymin.value(), self.sb_ymax.value() )
        self.maincanvas.draw()
    @QtCore.pyqtSlot( int )
    def on_sb_ymax_valueChanged( self ):
        self.maincanvas.axes.set_ylim( self.sb_ymin.value(), self.sb_ymax.value() )
        self.maincanvas.draw()
        #------------------------------------------------------------------------------------
    # Funciones de los botones accionados por el usuario para controlar el inicio y el final
    # del ensayo
    @QtCore.pyqtSlot()
    def on_pb_start_clicked ( self ):
        self.Dilatometer_test()
        self.pb_start.setEnabled( False )
    
    @QtCore.pyqtSlot()
    def on_pb_end_clicked ( self ):
        self.dilatometria.exiting = True
        while self.dilatometria.isRunning():
            continue
        time.sleep(1)
        self.dilatometria.terminate()
        time.sleep(1)
        f = open( self.le_output_file_path.text() + '.txt' )
        s = self.comented_header + f.read() + self.comented_footer
        f.close()
        f = open( self.le_output_file_path.text() + '.txt', 'w' )
        f.write( s )
        f.close()
        self.pb_start.setEnabled( True )
        self.pb_start_save_data.setEnabled( False )

    @QtCore.pyqtSlot ()
    def on_pb_start_save_data_clicked ( self ):
        self.dilatometria.time_stamp = 0
        self.dilatometria.zero_time = time.time()
        self.maincanvas.axes.cla()
        self.maincanvas.axes.grid( True )
        self.auxcanvas_2.axes.cla()
        self.auxcanvas_2.axes.grid( True )
        self.auxcanvas_1.axes.cla()
        self.auxcanvas_1.axes.grid( True )
        self.dilatometria.savedata = True
        self.read_data = True
#-----------------------------------------------------------------------------------
    def Dilatometer_test ( self ):
        # inicializar archivos leer configuraciones inicializar puerto serie
        outfile = self.le_output_file_path.text()
        if outfile == '':
            self.statusBar().showMessage( 'El campo que indica el archivo de destino no puede estar vacio' )
        else:

            outfile += '.txt'

            header = 'Comentarios:' + self.ptx_header.toPlainText() + '\n'
            self.comented_header = ''
            for line in header.split( '\n' ):
                self.comented_header = self.comented_header + self.le_output_file_commentchar.text() + line + '\n'
            labels='Tiempo (s) \t Temperatura (C)  \t Deformacion (mm) \n'
            self.comented_header=self.comented_header+labels
            footer = self.ptx_footer.toPlainText() + '\n'
            self.comented_footer = ''
            for line in footer.split( '\n' ):
                self.comented_footer = self.comented_footer + self.le_output_file_commentchar.text() + line + '\n'

            port = str ( self.cbx_LVDT_serial_port.currentText() )
            multimeter = 'USB0::2391::1543::my47030898::0'
            self.dilatometria.test( outfile, port, multimeter )
            self.count = 0
            self.pb_start_save_data.setEnabled( True )
            self.pb_end.setEnabled( True )

    @QtCore.pyqtSlot ()
    def show_incoming_data ( self, data ):
        #Muestra el tiempo transcurrido
        if data[0] < 60:
            self.lcd_time_second.display( str ( int ( data[0] ) ) )
        else:
            m = data[0] // 60
            s = data[0] % 60
            if m < 60:
                self.lcd_time_second.display( str ( int ( s ) ) )
                self.lcd_time_minute.display( str ( int ( m ) ) )
            else:
                h = m // 60
                m = m % 60
                self.lcd_time_second.display( str ( int ( s ) ) )
                self.lcd_time_minute.display( str ( int ( m ) ) )
                self.lcd_time_hour.display( str ( int ( h ) ) )
        # Muestra el valor de tempperatura en el display
        self.lcd_var_3.display( str ( data[2] ) )

        if self.read_data:
            f = open( self.le_output_file_path.text() + '.txt' )
            s = StringIO( f.read() )
            f.close()
            s.seek( 0 )

            time_np, temp, lvdt = np.genfromtxt( s,
                                       usecols = ( 0, 1, 2 ),
                                       deletechars = "\n",
                                       dtype = float,
#                                        comment='%',
                                       autostrip = True,
                                       unpack = True )

            # Muestra las pendientes de la recta de deformacion y temperatura formadas
            #  en funcion del tiempo (tomando solo los ultimpos 100 valores 

            if np.size( lvdt ) >= 100:
                def_a=np.polyfit(time_np[-100:-1]/60, lvdt[-100:-1],1)[0]
                self.lcd_var_1.display( str ( def_a ) )
                temp_a=np.polyfit(time_np[-100:-1]/60, temp[-100:-1],1)[0]
                self.lcd_var_2.display( str ( temp_a ) )
                
            # Ploteando en los canvas ya definidos con las funciones heredadas de la clase canvas
            # Deformacion en funcion de temperatura
            self.maincanvas.axes.cla()
            self.maincanvas.axes.grid( True )
            self.statusBar.showMessage( 'Ploteando principal...' )
            self.maincanvas.axes.set_xlim( self.sb_xmin.value(), self.sb_xmax.value() )
            self.maincanvas.axes.set_ylim( self.sb_ymin.value(), self.sb_ymax.value() )
            #self.maincanvas.axes.set_xlim( temp[0], temp[-1] )
            #self.maincanvas.axes.set_ylim( np.min( lvdt ) - np.min( lvdt ) * 20 / 100, np.max( lvdt ) + np.max( lvdt ) * 20 / 100 )
            self.maincanvas.axes.plot( temp, lvdt, 'og' )
            self.maincanvas.fig.canvas.draw()

            if np.size( time_np ) < 300:
                # Temperatura en funcion de tiempo
                self.auxcanvas_1.axes.cla()
                self.auxcanvas_1.axes.grid( True )
                self.statusBar.showMessage( 'Ploteando Auxiliar 1...' )
                self.auxcanvas_1.axes.set_xlim( time_np[0], time_np[-1] )
                self.auxcanvas_1.axes.set_ylim( np.min( temp ) - np.min( temp ) * 20 / 100, np.max( temp ) + np.max( temp ) * 20 / 100 )
                self.auxcanvas_1.axes.plot( time_np, temp, 'blue' )
                self.auxcanvas_1.fig.canvas.draw()

                # Deformacion en funcion de tiempo
                self.auxcanvas_2.axes.cla()
                self.auxcanvas_2.axes.grid( True )
                self.statusBar.showMessage( 'Ploteando Auxiliar 2...' )
                self.auxcanvas_2.axes.set_xlim( time_np[0], time_np[-1] )
                self.auxcanvas_2.axes.set_ylim( np.min( lvdt ) - np.min( lvdt ) * 20 / 100, np.max( lvdt ) + np.max( lvdt ) * 20 / 100 )
                self.auxcanvas_2.axes.plot( time_np, lvdt, 'red' )
                self.auxcanvas_2.fig.canvas.draw()
            else:
                self.auxcanvas_1.axes.cla()
                self.auxcanvas_1.axes.grid( True )
                self.statusBar.showMessage( 'Ploteando Auxiliar 1...' )
                self.auxcanvas_1.axes.set_xlim( time_np[-299], time_np[-1] )
                self.auxcanvas_1.axes.set_ylim( np.min( temp[-299:-1] ) - np.min( temp[-299:-1] ) * 20 / 100, np.max( temp[-299:-1] ) + np.max( temp[-299:-1] ) * 20 / 100 )
                self.auxcanvas_1.axes.plot( time_np[-299:-1], temp[-299:-1], 'blue' )
                self.auxcanvas_1.fig.canvas.draw()
                # Deformacion en funcion de tiempo
                self.auxcanvas_2.axes.cla()
                self.auxcanvas_2.axes.grid( True )
                self.statusBar.showMessage( 'Ploteando Auxiliar 2...' )
                self.auxcanvas_2.axes.set_xlim( time_np[-299], time_np[-1] )
                self.auxcanvas_2.axes.set_ylim( np.min( lvdt[-299:-1] ) - np.min( lvdt[-299:-1] ) * 20 / 100, np.max( lvdt[-299:-1] ) + np.max( lvdt[-299:-1] ) * 20 / 100 )
                self.auxcanvas_2.axes.plot( time_np[-299:-1], lvdt[-299:-1], 'red' )
                self.auxcanvas_2.fig.canvas.draw()

            del temp, lvdt, time_np
#--------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def on_tlb_output_file_path_pressed( self ):
        # seleccionar archivo
        self.le_output_file_path.setText( QtGui.QFileDialog.getSaveFileName( parent = None ) )
def main():
    app = QtGui.QApplication( sys.argv )
    DAQ = Main()
    DAQ.show()
    sys.exit( app.exec_() )
if __name__ == '__main__':
    main()