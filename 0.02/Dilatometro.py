'''
Created on 12/09/2013

@author: Javier Cruce%A4o
'''
# Importar librerias necesarias

# Interfaz grafica
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
    def test ( self, outfile, AG34410A, AG34405A ):
        
        #Configuracion de Multimetro Agilent 33410A para leer termocupla
        self.termo = visa.instrument( AG34405A )
        self.lvdt = visa.Instrument( AG34410A )
        
        self.termo.write( '*RST' )
        self.lvdt.write( '*RST' )
        time.sleep(5)
    
        self.termo.write( 'CONF:VOLT:DC AUTO' )
        self.lvdt.write( 'CONF:VOLT:AC 10' )
        
        time.sleep(0.1)
        self.lvdt.write('SENS:VOLT:AC:BAND 20')
        time.sleep(0.5)
        
        #Otras configuraciones
        self.time_stamp = 0
        self.savedata = False
        self.outfile = outfile
        self.errorfile= outfile+'_errorlog.txt'
        self.start()

    # Esta funcion leera continuamente los dispositivos hasta finalizar el ensayo
    def run ( self ):
        # Cambia el mensaje enm el dysplay secundario del multimetro
        self.lvdt.write( 'DISP:WIND2:TEXT "Midiendo ..."' )
        # Variable bandera que indica que es la primera vez qwue corre el proceso
        first = True
        print 'Abrimos archivo de error'
        error_fsock= open(self.errorfile, 'w')
        
        while not self.exiting:

            if first:
                
                fsock = open( self.outfile, 'w' )
                self.zero_time = time.time()
                first = False
                
            else:
                
                fsock = open( self.outfile, 'a' )
                self.time_stamp = time.time() - self.zero_time
                
            #=====================================================================================
            # Se usan las entencias "try" y "except" para evitar que se detenga el ensayo 
            # si llegara a producirse un error de lectura en alguno de los multimetros utilizados. 
            # y a su vez se guarda este error en un archivo para su posterior analisis
            #======================================================================================

            try:
                print 'Midiendo termo'
                self.termo.write( 'READ?' )
                time.sleep(0.02)
                temp_data = self.termo.read()
                
                print 'Midiento LVDT'
                self.lvdt.write('READ?')
                time.sleep(0.02)
                lvdt_data = self.lvdt.read()

                print temp_data, lvdt_data
                
            except:
                
                error_line= str (self.time_stamp) 
                error_line+= ' \tError LVDT: '+self.lvdt.ask('SYST:ERR?')
                error_line+= '\tError Termocupla :'+self.termo.ask ('SYST:ERR?')+'\n'
                error_fsock.write(error_line)
                print error_line
                
                continue
            #====================================================================================
            
            temp_data = float ( temp_data ) *1000
            lvdt_data=float (lvdt_data)*1.7926 #mm/V
            
#           Pasar de milivoltios a gracdos centigrado el valor leido por el multimetro
            # Polinomio para rango intermedio  -272 a 150 C

            if temp_data < 2: 
                
                Y = 25.39459 * temp_data 
                Y-= 0.44494 * temp_data ** 2 
                Y+= 0.05652 * temp_data ** 3 
                Y-= 0.00412 * temp_data ** 4 
                Y+= 0.0011 * temp_data ** 5 
                Y-= 1.39776E-4 * temp_data ** 6 
                Y+= 4.40583E-6 * temp_data ** 7 
                Y+= 7.709E-8 * temp_data ** 8
                
            #Polinomio para rango positivo 0 a 500 C     
            if temp_data >=2 :
                
                Y = 25.26032 * temp_data
                Y-= 0.57128 * temp_data ** 2
                Y+= 0.13393 * temp_data ** 3
                Y-= 0.01411 * temp_data ** 4
                Y+= 7.7329E-4 * temp_data ** 5
                Y-= 2.32438E-5 * temp_data ** 6
                Y+= 3.64924E-7 * temp_data ** 7
                Y-= 2.34283E-9 * temp_data ** 8
                
#           Guardar array
            data = [self.time_stamp, Y, lvdt_data, temp_data]    
            print data
            # Si se comienza el inicio de grabacion de datos se guardara todo en el archivo de salida 
            # indicado
            if self.savedata:
#                 print 'Guardando'
                # Muestra mensaje en multimetro AG34410A
                self.lvdt.write( 'DISP:WIND2:TEXT "Guardando..."' )
                # Se arma linea de texto para guardar en el archivo
                line = str ( data[0] ) + '\t' + str ( data[1] ) + '\t' + str ( data[2])+'\t'+str (data[3]) + '\n'
                # Se escribe linea en el archivo
                fsock.write( line )
                # Se cierra el archivo
                fsock.close()
                
            # Si no se inicia la grabacion de datos se guardara una sola linea de datos en un archivo temporal
            else:
#                 print 'Guardantdo temporal'
                tempfsock = open( 'tempdata', 'w' )
                line = str ( data[0] ) + '\t' + str ( data[1] ) + '\t' + str ( data[2] ) + '\n'
                tempfsock.write(line)
                tempfsock.close()
#             print 'Envisar senial'
            self.emit( QtCore.SIGNAL ( "LVDT_readsignal(PyQt_PyObject)" ), data )
                
        self.lvdt.write( 'DISP:WIND2:TEXT:CLEAR' )
        fsock.close()
        error_fsock.close()
        self.exit()

    def __del__( self ):
        self.lvdt.write( 'DISP:WIND2:TEXT:CLEAR' )
        self.exiting = True
        fsock.close()
        error_fsock.close()
        self.ser.close()
        self.wait()

class Main( QtGui.QMainWindow ):
    """La ventana principal de la aplicacion."""

    def __init__( self ):

        #Inicializamos interfaz graica---------------------------
        QtGui.QMainWindow.__init__( self )

        # Cargamos la interfaz desde el archivo .ui
        uic.loadUi( 'DilatometroUI.ui', self )
        #--------------------------------------------------------

        #-------------------------------------------------------------------------------------
        # Cargamos los procesos que leeran la informacion de los dispositivos-----------------
        # Generamos los planos donde graficaremos los datos--------------------------
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
        
        # Configurar subproceso encargado de la adquisicion de datos        
        self.dilatometria = Test_Dilatometria()
        self.thread=QtCore.QThread()
        self.thread.started.connect(self.dilatometria.test)
        self.connect( self.dilatometria, QtCore.SIGNAL ( "finished()" ), self.thread.quit )
        self.dilatometria.moveToThread(self.thread)
        
        
        self.read_data = False
        # Conectamos seniales de los threads con funciones de manejo de datos---------------
        self.connect( self.dilatometria, QtCore.SIGNAL ( "LVDT_readsignal(PyQt_PyObject)" ), self.show_incoming_data )
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
        # Detiene ele subproceso de adquisicion de datos.
        self.dilatometria.exiting = True
        while self.dilatometria.isRunning():
            continue
        time.sleep(1)
        self.dilatometria.terminate()
        time.sleep(1)
        
        # Se toma lo escrito en el encabezado para guardarlo en el arhivo comentado con el caracter de 
        # de comentario elegido.
        header = self.ptx_header.toPlainText()
        self.comented_header = ''
        for line in header.split( '\n' ):
            self.comented_header = self.comented_header + self.le_output_file_commentchar.text() + line + '\n'
        
        labels='Tiempo (s) \t Temperatura (C)  \t Deformacion (mm) \t Temperatura (mV)\n'
        # Encabezado mas linea de encabezados de tabla. 
        self.comented_header=self.comented_header+labels
        
        # Se toma lo escrito en el pie de pagina para guardarlo en el arhivo comentado con el caracter de 
        # de comentario elegido.
        footer = self.ptx_footer.toPlainText() + '\n'
        self.comented_footer = ''
        for line in footer.split( '\n' ):
            self.comented_footer = self.comented_footer + self.le_output_file_commentchar.text() + line + '\n'
            
        # Lee el archivo de salida completo y agrega al inicio y al final 
        # el encabezado y el pie de pagina. -----------------------------
        f = open( self.le_output_file_path.text() + '.txt' )
        s = self.comented_header + f.read() + self.comented_footer
        f.close()
        
        # Escribe tados los datos con encabezado y pie de pagina incluido
        # nuevamente en el arhivo. ---------------------------------------
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
                
            # Nombres que identifican los multimetros utilizados para la adquisicion de datos
            AG34410A = 'USB0::2391::1543::my47030898::0::INSTR'
            AG34405A = 'USB0::0x0957::0x0618::MY51320020::0::INSTR'
            
            self.dilatometria.test( outfile, AG34410A, AG34405A )
            self.count = 0
            self.pb_start_save_data.setEnabled( True )
            self.pb_end.setEnabled( True )

    @QtCore.pyqtSlot ()
    def show_incoming_data ( self, data ):
        del data
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


            # Muestra el tiempo transcurrido--------------------------------------------
            # Segundos-------------------------------------------------
            if time_np[-1] < 60:
                self.lcd_time_second.display( str ( int ( time_np[-1] ) ) )
            
            # Minutos---------------------------------------------------
            else:
                m = time_np[-1] // 60 # Minutos
                s = time_np[-1] % 60 # Segundos
                
                # Si no paso mas de una hora se muestra solo minutos y segundos
                if m < 60:
                    self.lcd_time_second.display( str ( int ( s ) ) )
                    self.lcd_time_minute.display( str ( int ( m ) ) )
                # Horas--------------------------------------------------
                else:
                    h = m // 60 # Horas
                    m = m % 60 # Minutos
                    self.lcd_time_second.display( str ( int ( s ) ) )
                    self.lcd_time_minute.display( str ( int ( m ) ) )
                    self.lcd_time_hour.display( str ( int ( h ) ) )
            #---------------------------------------------------------------------------
            
            self.lcd_var_1.display( str (temp[-1]) ) # Muestra Valor de temperatura
            self.lcd_var_3.display( str ( lvdt[-1] ) ) # Muestra Valor del LVDT

            # Muestra las pendientes de la recta de temperatura formada
            # En funcion del tiempo (tomando solo los ultimpos 150 valores 
            if np.size( lvdt ) >= 30:
                temp_a=np.polyfit(time_np[-149:-1]/60, temp[-149:-1],1)[0] 
                self.lcd_var_2.display( str ( temp_a ) )
                
            # Ploteando en los canvas ya definidos con las funciones heredadas de la clase canvas
            # Deformacion en funcion de temperatura
            self.maincanvas.axes.cla()
            self.maincanvas.axes.grid( True )
            self.statusBar.showMessage( 'Ploteando principal...' )
            self.maincanvas.axes.set_xlim( self.sb_xmin.value(), self.sb_xmax.value() )
            self.maincanvas.axes.set_ylim( self.sb_ymin.value(), self.sb_ymax.value() )
            self.maincanvas.axes.plot( temp, lvdt, 'og' )
            self.maincanvas.fig.canvas.draw()

            if np.size( time_np ) < 300:
                # Temperatura en funcion de tiempo
                self.auxcanvas_1.axes.cla()
                self.auxcanvas_1.axes.grid( True )
                self.statusBar.showMessage( 'Ploteando Auxiliar 1...' )
                self.auxcanvas_1.axes.set_xlim( time_np[0], time_np[-1] )
                self.auxcanvas_1.axes.set_ylim( np.min( temp ) - abs (np.min( temp ) * 20 / 100),
                                                np.max( temp ) + abs (np.max( temp ) * 20 / 100) )
                self.auxcanvas_1.axes.plot( time_np, temp, 'blue' )
                for label in self.auxcanvas_1.axes.get_xticklabels():
                # label is a Text instance
                    label.set_rotation ( 45 )
                self.auxcanvas_1.fig.canvas.draw()

                # Deformacion en funcion de tiempo
                self.auxcanvas_2.axes.cla()
                self.auxcanvas_2.axes.grid( True )
                self.statusBar.showMessage( 'Ploteando Auxiliar 2...' )
                self.auxcanvas_2.axes.set_xlim( time_np[0], time_np[-1] )
                self.auxcanvas_2.axes.set_ylim( np.min( lvdt ) - (np.max( lvdt )-np.min (lvdt)) * 10 / 100,
                                                np.max( lvdt ) + (np.max( lvdt )-np.min (lvdt)) * 10 / 100 )
                self.auxcanvas_2.axes.plot( time_np, lvdt, 'red' )
                for label in self.auxcanvas_2.axes.get_xticklabels():
                # label is a Text instance
                    label.set_rotation ( 45 )
                self.auxcanvas_2.fig.canvas.draw()
            else:
                # Temperatura en funcion de tiempo
                self.auxcanvas_1.axes.cla()
                self.auxcanvas_1.axes.grid( True )
                self.statusBar.showMessage( 'Ploteando Auxiliar 1...' )
                self.auxcanvas_1.axes.set_xlim( time_np[-299], time_np[-1] )
                self.auxcanvas_1.axes.set_ylim( np.min( temp[-299:-1] ) - abs (np.min( temp[-299:-1] ) * 20 / 100),
                                                np.max( temp[-299:-1] ) + abs (np.max( temp[-299:-1] ) * 20 / 100 ))
                self.auxcanvas_1.axes.plot( time_np[-299:-1], temp[-299:-1], 'blue' )
                for label in self.auxcanvas_1.axes.get_xticklabels():
                # label is a Text instance
                    label.set_rotation ( 45 )
                self.auxcanvas_1.fig.canvas.draw()
                
                # Deformacion en funcion de tiempo
                self.auxcanvas_2.axes.cla()
                self.auxcanvas_2.axes.grid( True )
                self.statusBar.showMessage( 'Ploteando Auxiliar 2...' )
                self.auxcanvas_2.axes.set_xlim( time_np[-299], time_np[-1] )
                self.auxcanvas_2.axes.set_ylim( np.min( lvdt[-299:-1] ) - (np.max( lvdt[-299:-1] )-np.min(lvdt[-299:-1])) * 10 / 100,
                                                np.max( lvdt[-299:-1] ) + (np.max( lvdt[-299:-1] )-np.min(lvdt[-299:-1])) * 10 / 100 )
                self.auxcanvas_2.axes.plot( time_np[-299:-1], lvdt[-299:-1], 'red' )
                for label in self.auxcanvas_2.axes.get_xticklabels():
                # label is a Text instance
                    label.set_rotation ( 45 )
                self.auxcanvas_2.fig.canvas.draw()

            del temp, lvdt, time_np
            
        else:
            f = open( 'tempdata' )
            s = StringIO( f.read() )
            f.close()
            s.seek( 0 )

            data = np.genfromtxt( s,
                                       deletechars = "\n",
                                       dtype = float,
                                       autostrip = True,
                                       unpack = True )
            
            # Muestra el tiempo transcurrido--------------------------------------------
            # Segundos-------------------------------------------------
            if data[0] < 60:
                self.lcd_time_second.display( str ( int ( data[0] ) ) )
            
            # Minutos---------------------------------------------------
            else:
                m = data[0] // 60 # Minutos
                s = data[0] % 60 # Segundos
                
                # Si no paso mas de una hora se muestra solo minutos y segundos
                if m < 60:
                    self.lcd_time_second.display( str ( int ( s ) ) )
                    self.lcd_time_minute.display( str ( int ( m ) ) )
                # Horas--------------------------------------------------
                else:
                    h = m // 60 # Horas
                    m = m % 60 # Minutos
   
                    self.lcd_time_second.display( str ( int ( s ) ) )
                    self.lcd_time_minute.display( str ( int ( m ) ) )
                    self.lcd_time_hour.display( str ( int ( h ) ) )
            #---------------------------------------------------------------------------
            
            # Muestra el valor de tempperatura en el display
            
            self.lcd_var_1.display( str ( data[1] ) ) # Muestra valor de temperatura
            self.lcd_var_3.display( str ( data[2] ) ) # Muestra valor de LVDT
            
            del data
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
