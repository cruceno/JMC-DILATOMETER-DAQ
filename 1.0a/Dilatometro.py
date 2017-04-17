#!../env/Scripts/python.exe
# Importar librerias necesarias
# Interfaz grafica
from PyQt4 import QtCore, QtGui
from mainUI import Ui_MainWindow
# Comunicacion con sistema y manejo de puerto serie
import os, sys, logging, time
# Importar librerias para manejo de protocolos VISA y Measure Computing
import MultimetrosAgilent, PlacasMeasureComputing
import UniversalLibrary as UL
#Importar libreria para cargar archivos de configuracion
from configobj import ConfigObj
#Funcion para pasar datos como si fueran un archivo de texto
from StringIO import StringIO
# Manejo numerico de datos
import numpy as np
# Librerias para graficar en el ploter
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigatioToolbar
from matplotlib.figure import Figure
from MultimetrosAgilent import list_agilent_multimeters

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
        FigureCanvas.setSizePolicy( self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding )
        # se notifica al sistema de la actualizacion de la politica
        FigureCanvas.updateGeometry( self )
        self.fig.canvas.draw()   
    
class Test_Dilatometria ( QtCore.QThread ):
    #Inicio de la clase Qthread
    def __init__ ( self ):
        QtCore.QThread.__init__( self )
        self.exiting = False
    #Funcion que va a ser llamada desde otro proceso para iniciar este hilo que lleva a 
    #cabo la medicion
    def test ( self, 
               outfile,
               lvdt, 
               temperature, 
               lvdt_calibration, 
               data_per_second ):
        
        #Configuracion de entradas
        # (type:      'pyvisa' o 'mcc'
        #  channel:   ('pyvisa_address', (board, channel) )
        
        if temperature['type']=='pyvisa':
            print temperature['channel']
            self.termo = MultimetrosAgilent.AG344XXA(str (temperature['channel']))
            self.termo.dev.write( '*RST' )
            self.termo.dev.write( 'CONF:VOLT:DC AUTO' )
        else:
            self.termo= PlacasMeasureComputing.ULINPUT(temperature['channel'][1], 'temp', temperature['channel'][0])
            
        if lvdt['type'] == 'pyvisa':   
            self.lvdt = MultimetrosAgilent.AG344XXA(lvdt['channel'])
            self.lvdt.dev.write( '*RST' )
            self.lvdt.dev.write( 'CONF:VOLT:DC AUTO' )
        else:
            self.lvdt= PlacasMeasureComputing.ULINPUT(lvdt['channel'][1], 'volt', lvdt['channel'][0])
        
        #Otras configuraciones
        self.time_stamp = 0
        self.delay=1/data_per_second
        self.lvdt_calibration = lvdt_calibration
        print self.lvdt_calibration
        self.savedata = False
        self.outfile = outfile
        self.errorfile= outfile+'_errorlog.txt'
        self.start()

    # Esta funcion leera continuamente los dispositivos hasta finalizar el ensayo
    def run ( self ):

        # Variable bandera que indica que es la primera vez qwue corre el proceso
        first = True
        # print 'Abrimos archivo de error'
        # self.error_fsock= open(self.errorfile, 'w')
        
        while not self.exiting:

            if first:
                
                self.fsock = open( self.outfile, 'w' )
                self.zero_time = time.time()
                first = False
                
            else:
                
                self.fsock = open( self.outfile, 'a' )
                self.time_stamp = time.time() - self.zero_time
                
            #=====================================================================================
            # Se usan las entencias "try" y "except" para evitar que se detenga el ensayo 
            # si llegara a producirse un error de lectura en alguno de los multimetros utilizados. 
            # y a su vez se guarda este error en un archivo para su posterior analisis
            #======================================================================================
            # Cambia el mensaje enm el dysplay secundario del multimetro
            if self.termo.type == 'pyvisa' and self.termo.message:
                self.termo.dev.write( 'DISP:WIND2:TEXT "Midiendo ..."' )
            elif self.lvdt.type == 'pyvisa' and self.lvdt.message:
                self.lvdt.dev.write ( 'DISP:WIND2:TEXT "Midiendo ..."')
            
            if self.termo.type == 'pyvisa': 
                try:
                    # print 'Midiendo termo'
                    temp_data=self.termo.dev.query( 'READ?' )
                except:
                    error = str (self.time_stamp) 
                    error+= '\tError Termocupla :'+self.termo.dev.query ('SYST:ERR?')+'\n'
                    logging.error(error)
                    continue
            else:
                temp_data= UL.cbTIn( int (self.termo.board),
                                     int (self.termo.channel),
                                     UL.CELSIUS ,
                                     0.0,
                                     UL.FILTER ) 
   
            if self.lvdt.type == 'pyvisa': 
                try:   
                    # print 'Midiento LVDT'
                    lvdt_data=self.lvdt.dev.query('READ?')
                except:
                    error= str (self.time_stamp)+': \tError LVDT: '+self.lvdt.dev.query('SYST:ERR?')
                    logging.error(error)
                    # print error_line
                    continue
            else: 
                # print self.lvdt.board
                lvdt_value= UL.cbVIn( int (self.lvdt.board),
                                     int (self.lvdt.channel),
                                     UL.cbGetConfig( UL.BOARDINFO,
                                                     int (self.lvdt.board),
                                                     int (self.lvdt.channel),
                                                     UL.BIRANGE,
                                                     ConfigVal = 0 ),
                                     0.0,
                                     Option = None )
            # print temp_data, lvdt_data
            #====================================================================================
            
            temp_data = float ( temp_data ) *1000
            lvdt_data = float(lvdt_value) 
            lvdt_data_um=float (lvdt_value)*self.lvdt_calibration #62.8 um/V
            temp_data_celcius=self.termo.temperature_calibration(temp_data) # Pasar de milivoltios a grados celcius
                
#           Guardar array
            data = [self.time_stamp, temp_data_celcius, lvdt_data_um, temp_data, lvdt_data]    
            # print data
            # Si se comienza el inicio de grabacion de datos se guardara todo en el archivo de salida 
            # indicado
            if self.savedata:
#                 print 'Guardando'
                # Muestra mensaje en multimetro AG34410A
                if self.termo.type == 'pyvisa' and self.termo.message:
                    self.termo.dev.write( 'DISP:WIND2:TEXT "Guardando..."' )
                elif self.lvdt.type == 'pyvisa' and self.lvdt.message:
                    self.termo.dev.write( 'DISP:WIND2:TEXT "Guardando..."' )
                    
                # Se arma linea de texto para guardar en el archivo
                line = str ( data[0] ) + '\t' + str ( data[1] ) + '\t' + str ( data[2])+'\t'+str (data[3]) +'\t'+str (data[4]) + '\n'
                # Se escribe linea en el archivo
                self.fsock.write( line )
                # Se cierra el archivo
                self.fsock.close()
                
            # Si no se inicia la grabacion de datos se guardara una sola linea de datos en un archivo temporal
            else:
#                 print 'Guardantdo temporal'
                tempfsock = open( 'tempdata', 'w' )
                line = str ( data[0] ) + '\t' + str ( data[1] ) + '\t' + str ( data[2])+'\t'+str (data[3]) +'\t'+str (data[4]) + '\n'
                tempfsock.write(line)
                tempfsock.close()
#             print 'Envisar senial'
            self.emit( QtCore.SIGNAL ( "LVDT_readsignal(PyQt_PyObject)" ), data )
            if self.termo.type == 'pyvisa' and self.termo.message:
                self.termo.dev.write( 'DISP:WIND2:TEXT "En espera..."' )
            elif self.lvdt.type == 'pyvisa' and self.lvdt.message:
                self.termo.dev.write( 'DISP:WIND2:TEXT "En espera..."' )
            time.sleep(self.delay)
            
        if self.termo.type == 'pyvisa' and self.termo.message:
            self.termo.dev.write( 'DISP:WIND2:TEXT:CLEAR' )
        elif self.lvdt.type == 'pyvisa' and self.lvdt.message:
            self.lvdt.dev.write ( 'DISP:WIND2:TEXT:CLEAR')
        self.fsock.close()

        self.exit()

    def __del__( self ):
        if self.termo.type == 'pyvisa' and self.termo.message:
            self.termo.dev.write( 'DISP:WIND2:TEXT:CLEAR' )
        elif self.lvdt.type == 'pyvisa' and self.lvdt.message:
            self.lvdt.dev.write ( 'DISP:WIND2:TEXT:CLEAR')
        self.fsock.close()
        self.exiting = True
        self.wait()

class Main( QtGui.QMainWindow, Ui_MainWindow ):
    """La ventana principal de la aplicacion."""

    def __init__( self ):

        #Inicializamos interfaz graica---------------------------
        QtGui.QMainWindow.__init__( self )
        self.setupUi(self)
        #Cargar configuracion por defecto.
        self.default_config_file='default.ini'
        self.load_config(True)
        #-------------------------------------------------------------------------------------

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
        
        self.visa_suported=['AG_34405A', 'AG_34410A']
        # Conectamos seniales de los threads con funciones de manejo de datos---------------
        self.connect( self.dilatometria, QtCore.SIGNAL ( "LVDT_readsignal(PyQt_PyObject)" ), self.show_incoming_data )
        #----------------------------------------------------------------------------------
        self.read_data = False
        
    def load_list_of_visa_instruments(self, lvdt, temperature):
        resouces_list=list_agilent_multimeters()
        if lvdt:
            i = self.cbx_dilatometer_lvdt_channel.count()
            while -1 < i:
                # Si hay algun item en el combobox removerlo
                self.cbx_dilatometer_lvdt_channel.removeItem(i)
                i -= 1 
            for inst in resouces_list:
                self.cbx_dilatometer_lvdt_channel.addItem(inst[1],str (inst[0]))
               
        if temperature:
            i =self.cbx_dilatometer_temperature_channel.count()
            while -1 < i:
                # Si hay algun item en el combobox removerlo'
                self.cbx_dilatometer_temperature_channel.removeItem(i)
                i-=1
            for inst in resouces_list:
                self.cbx_dilatometer_temperature_channel.addItem(inst[1], str (inst[0]))
                
    def load_list_of_mcc_board_channels(self,lvdt,temperature):
            
        if lvdt:
            i = self.cbx_dilatometer_lvdt_channel.count()
            while -1 < i:
                # Si hay algun item en el combobox removerlo
                self.cbx_dilatometer_lvdt_channel.removeItem(i)
                i -= 1 
            for channel in range(4):

                self.cbx_dilatometer_lvdt_channel.addItem(str(channel))
                
        if temperature:
            i =self.cbx_dilatometer_temperature_channel.count()
            while -1 < i:
                # print ' Si hay algun item en el combobox removerlo'
                self.cbx_dilatometer_temperature_channel.removeItem(i)
                i-=1
            for channel in range(4):

                self.cbx_dilatometer_temperature_channel.addItem(str (channel), channel)   
                
    def on_cbx_dilatometer_temperature_input_activated(self):
        if self.cbx_dilatometer_temperature_input.currentIndex() == 0 :
            self.load_list_of_visa_instruments(False, True)
        else:
            self.load_list_of_mcc_board_channels(False, True)
            
    def on_cbx_dilatometer_lvdt_input_activated(self):
        if self.cbx_dilatometer_lvdt_input.currentIndex() == 0 :
            self.load_list_of_visa_instruments(True, False)
        else: 
            self.load_list_of_mcc_board_channels(True, False)
            
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
        
        labels=self.le_output_file_commentchar.text()+'Tiempo (s) \t Temperatura (C)  \t Deformacion (um) \t Temperatura (mV) \t Deformacion (V) \n'
        # Encabezado mas linea de encabezados de tabla. 
        self.comented_header=self.comented_header+labels
        
            
        # Lee el archivo de salida completo y agrega al inicio y al final 
        # el encabezado y el pie de pagina. -----------------------------
        f = open( self.le_output_file_path.text() + '.txt')
        s = self.comented_header + f.read()
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
        self.pb_start_save_data.setEnabled(False)
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
            self.statusBar.showMessage( 'El campo que indica el archivo de destino no puede estar vacio' )
        else:
            outfile += '.txt'
               
            # Nombres que identifican los multimetros utilizados para la adquisicion de datos
            #Configuracion de entradas
            # (type:      'pyvisa' o 'mcc'
            #  channel:   'pyvisa_address', (board, channel) )
            
            lvdt = {'type': 'pyvisa' if self.cbx_dilatometer_lvdt_input.currentText() == 'Agilent Multimeter' else 'mcc', 
                    'channel':self.cbx_dilatometer_lvdt_channel.itemData(self.cbx_dilatometer_lvdt_channel.currentIndex()).toString() if self.cbx_dilatometer_lvdt_input.currentText() == 'Agilent Multimeter' else 
                            (self.cbx_dilatometer_lvdt_channel.currentText(), self.sb_lvdt_board_num.value()) }
            temperature = {'type': 'pyvisa' if self.cbx_dilatometer_temperature_input.currentText() == 'Agilent Multimeter' else 'mcc', 
                           'channel':self.cbx_dilatometer_temperature_channel.itemData(self.cbx_dilatometer_temperature_channel.currentIndex()).toString() if self.cbx_dilatometer_temperature_input.currentText() == 'Agilent Multimeter' else 
                                    (self.cbx_dilatometer_temperature_channel.currentText(), self.sb_temperature_board_num.value()) }
            print self.dsb_lvdt_calibration_factor.value()
        #      outfile,
        #      lvdt, 
        #      temperature, 
        #       lvdt_calibration, 
        #       data_per_second 
        
            self.dilatometria.test( outfile,
                                    lvdt,
                                    temperature,
                                    self.dsb_lvdt_calibration_factor.value(),
                                    self.sb_data_per_second.value() )
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
            # en funcion del tiempo (tomando solo los ultimpos 150 valores 
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
        self.le_output_file_path.setText( QtGui.QFileDialog.getSaveFileName( parent = None, 
                                                                             caption= 'Select Output File',
                                                                             directory=os.path.expanduser(self.config['OutputFile']['output_file_base_dir']) ) )
        
    def on_pb_save_config_pressed(self):

        self.config.filename=QtGui.QFileDialog.getSaveFileName( parent = None, 
                                                                             caption= 'Select Config File',
                                                                             directory=os.path.expanduser(self.config['OutputFile']['output_file_base_dir']) ) 
        self.config.write()
        
    def on_pb_load_config_pressed(self):
        
        self.config_file= QtGui.QFileDialog.getOpenFileName(None, 'Load config File',
                                                            directory=os.path.expanduser(self.config['OutputFile']['output_file_base_dir'])) 
        self.load_config()
           
    def load_config (self, default=False):
        if default: 
            if os.path.isfile(self.default_config_file):
                self.config = ConfigObj(self.default_config_file)
                self.le_output_file_commentchar.setText(self.config['OutputFile']['coment_char'])
                self.cbx_dilatometer_temperature_input.setCurrentIndex(int(self.config['InputDevices']['termo']['input']))
                self.on_cbx_dilatometer_temperature_input_activated()
                self.cbx_dilatometer_lvdt_input.setCurrentIndex(int(self.config['InputDevices']['lvdt']['input']))
                self.on_cbx_dilatometer_lvdt_input_activated()
                self.cbx_dilatometer_temperature_channel.setCurrentIndex(self.cbx_dilatometer_temperature_channel.findText(self.config['InputDevices']['termo']['channel']))
                self.cbx_dilatometer_lvdt_channel.setCurrentIndex(self.cbx_dilatometer_lvdt_channel.findText(self.config['InputDevices']['lvdt']['channel']))
                self.sb_temperature_board_num.setValue(int(self.config['InputDevices']['termo']['board']))
                self.sb_lvdt_board_num.setValue(int(self.config['InputDevices']['lvdt']['board']))
                self.dsb_lvdt_calibration_factor.setValue(float(self.config['InputDevices']['lvdt']['calibration']))
                self.sb_data_per_second.setValue(int(self.config['InputDevices']['dps']))
                
            else:
                warn=str(time.time())+ 'Default config file not found'
                logging.warning(warn) 
        else:    
            if os.path.isfile(self.config_file):
                self.config = ConfigObj(str(self.config_file))
                self.le_output_file_commentchar.setText(self.config['OutputFile']['coment_char'])
                self.cbx_dilatometer_temperature_input.setCurrentIndex(int(self.config['InputDevices']['termo']['input']))
                self.on_cbx_dilatometer_temperature_input_activated()
                self.cbx_dilatometer_lvdt_input.setCurrentIndex(int(self.config['InputDevices']['lvdt']['input']))
                self.on_cbx_dilatometer_lvdt_input_activated()
                self.cbx_dilatometer_temperature_channel.setCurrentIndex(self.cbx_dilatometer_temperature_channel.findText(self.config['InputDevices']['termo']['channel']))
                self.cbx_dilatometer_lvdt_channel.setCurrentIndex(self.cbx_dilatometer_lvdt_channel.findText(self.config['InputDevices']['lvdt']['channel']))
                self.sb_temperature_board_num.setValue(int(self.config['InputDevices']['termo']['board']))
                self.sb_lvdt_board_num.setValue(int(self.config['InputDevices']['lvdt']['board']))
                self.dsb_lvdt_calibration_factor.setValue(float(self.config['InputDevices']['lvdt']['calibration']))
                self.sb_data_per_second.setValue(int(self.config['InputDevices']['dps']))
            else:
                warn=str(time.time())+ 'Selected config file not found'
                logging.warning(warn)
def SplashMouseEvent (event):
    pass    
def main():
    logging.basicConfig (filename='./dilatometro_log.txt', level=logging.WARNING)
    app = QtGui.QApplication( sys.argv )
    # Create a pixmap - not needed if you have your own.
    pixmap = QtGui.QPixmap('splash.png')
 
    splash = QtGui.QSplashScreen(pixmap)
    progressBar = QtGui.QProgressBar(splash)
    progressBar.setGeometry(splash.width()/10, 8*splash.height()/10,
                       8*splash.width()/10, splash.height()/10)
    splash.mousePressEvent=SplashMouseEvent
    QtGui.QFontDatabase.addApplicationFont("./fonts/EXO2REGULAR.TTF")
    font=QtGui.QFont('Exo 2')
    #font.setFamily('Exo 2')
    font.setBold(False)
    font.setItalic(True)
    font.setPixelSize(23)
    #font.setStretch(125)
    splash.setFont(font)
    splash.show()
    splash.showMessage('DILATOMETRO Ver.:1.0a\n Loading User Interface...', QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
    
    for i in range(0, 101):
        progressBar.setValue(i)
        # Do something which takes some time.
        t = time.time()
        while time.time() < t + 0.1:
            app.processEvents()
    


    DAQ = Main()
    DAQ.show()
    splash.finish(DAQ)
    sys.exit( app.exec_() )
if __name__ == '__main__':
    main()
