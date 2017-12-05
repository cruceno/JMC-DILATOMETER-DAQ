# -*- coding: utf-8 -*-
'''
Created on 28 jul. 2017

@author: javier
'''

# Importar librerias necesarias
# Interfaz grafica
from PyQt4 import QtCore, QtGui

# Comunicacion con sistema y manejo de puerto serie
import os
import sys
import logging
import time

# Importar libreria para cargar archivos de configuracion
from configobj import ConfigObj
# Funcion para pasar datos como si fueran un archivo de texto
from io import StringIO

# Manejo numerico de datos
import numpy as np
from dilatometer.gui.mainUI import Ui_MainWindow
from dilatometer.worker.rundaq import Test_Dilatometria
from dilatometer.instrument.MultimetrosAgilent import list_agilent_multimeters
from pyoma.ploter.qtmatplotlib import canvas as PlotCanvas
from pyoma.ploter.qtmatplotlib import NavigationToolbar


class Main(QtGui.QMainWindow, Ui_MainWindow):
    """La ventana principal de la aplicacion."""

    def __init__(self):

        # Inicializamos interfaz graica ---------------------------
        QtGui.QMainWindow.__init__(self)
        from dilatometer.gui.splash import SplashScreen
        pixmap = QtGui.QPixmap('./gui/images/splash.png')
        self.splash = SplashScreen(pixmap)
        self.splash.setTitle('DILATOMETER DAQ')
        self.splash.show()
        self.splash.connect(self,
                            QtCore.SIGNAL('splashUpdate(QString, int)'),
                            self.splash.showMessage
                            )
        self.setupUi(self)

        # Cargar configuracion por defecto.
        self.default_config_file = 'default.ini'
        self.load_config(True)
        # ---------------------------------------------------------
        # Generamos los planos donde graficaremos los datos--------
        # Inicializando base de ploteo para mainplot---------------
        self.vbl_main = QtGui.QVBoxLayout(self.gb_mainplot)
        self.maincanvas = PlotCanvas(self.gb_mainplot)
        self.vbl_main.insertWidget(0, self.maincanvas)
        # ---------------------------------------------------------

        # Inicializando base de ploteo para auxplot_1--------------
        self.vbl_aux_1 = QtGui.QVBoxLayout(self.gb_auxplot_1)
        self.auxcanvas_1 = PlotCanvas(self.gb_auxplot_1)
        self.vbl_aux_1.insertWidget(0, self.auxcanvas_1)
        # ----------------------------------------------------------

        # Inicializando base de ploteo para auxplot_2---------------
        self.vbl_aux_2 = QtGui.QVBoxLayout(self.gb_auxplot_2)
        self.auxcanvas_2 = PlotCanvas(self.gb_auxplot_2)
        self.vbl_aux_2.insertWidget(0, self.auxcanvas_2)
        # ----------------------------------------------------------

        # Configurar subproceso encargado de la adquisicion de datos
        self.dilatometria = Test_Dilatometria()
        self.thread = QtCore.QThread()
        self.thread.started.connect(self.dilatometria.test)
        self.connect(self.dilatometria,
                     QtCore.SIGNAL("finished()"),
                     self.thread.quit)

        self.dilatometria.moveToThread(self.thread)

        self.visa_suported = ['AG_34405A', 'AG_34410A']
        # Conectamos seniales de los threads con funciones de manejo de datos---------------
        self.connect(self.dilatometria, QtCore.SIGNAL("LVDT_readsignal(PyQt_PyObject)"), self.show_incoming_data)
        # ----------------------------------------------------------------------------------
        self.read_data = False

    def load_list_of_visa_instruments(self, lvdt, temperature):
        resouces_list = list_agilent_multimeters()
        if lvdt:
            i = self.cbx_dilatometer_lvdt_channel.count()
            while -1 < i:
                # Si hay algun item en el combobox removerlo
                self.cbx_dilatometer_lvdt_channel.removeItem(i)
                i -= 1
            for inst in resouces_list:
                self.cbx_dilatometer_lvdt_channel.addItem(inst[1], str(inst[0]))

        if temperature:
            i = self.cbx_dilatometer_temperature_channel.count()
            while -1 < i:
                # Si hay algun item en el combobox removerlo'
                self.cbx_dilatometer_temperature_channel.removeItem(i)
                i -= 1
            for inst in resouces_list:
                self.cbx_dilatometer_temperature_channel.addItem(inst[1], str(inst[0]))

    def load_list_of_mcc_board_channels(self, lvdt, temperature):

        if lvdt:
            i = self.cbx_dilatometer_lvdt_channel.count()
            while -1 < i:
                # Si hay algun item en el combobox removerlo
                self.cbx_dilatometer_lvdt_channel.removeItem(i)
                i -= 1
            for channel in range(4):

                self.cbx_dilatometer_lvdt_channel.addItem(str(channel))

        if temperature:
            i = self.cbx_dilatometer_temperature_channel.count()
            while -1 < i:
                # print ' Si hay algun item en el combobox removerlo'
                self.cbx_dilatometer_temperature_channel.removeItem(i)
                i -= 1
            for channel in range(4):

                self.cbx_dilatometer_temperature_channel.addItem(str(channel), channel)

    def on_cbx_dilatometer_temperature_input_activated(self):
        if self.cbx_dilatometer_temperature_input.currentIndex() == 0:
            self.load_list_of_visa_instruments(False, True)
        else:
            self.load_list_of_mcc_board_channels(False, True)

    def on_cbx_dilatometer_lvdt_input_activated(self):
        if self.cbx_dilatometer_lvdt_input.currentIndex() == 0:
            self.load_list_of_visa_instruments(True, False)
        elif self.cbx_dilatometer_lvdt_input.currentIndex() == 1:
            self.load_list_of_mcc_board_channels(True, False)
        elif self.cbx_dilatometer_lvdt_input.currentIndex() == 2:
            self.load_serial_devices()

    def load_serial_devices(self):
        from dilatometer.instrument.serialutil import scan_serial_ports
        ports = scan_serial_ports(20, False)
        i = self.cbx_dilatometer_lvdt_channel.count()
        while -1 < i:
            # Si hay algun item en el combobox removerlo
            self.cbx_dilatometer_lvdt_channel.removeItem(i)
            i -= 1
        for channel in ports:
            self.cbx_dilatometer_lvdt_channel.addItem(str(channel[1]))

    # Las siguientes 4 funciones son las encargadas de ajustar la escala de la grafica principal
    # por medio de los controles proporcionados al usuario

    @QtCore.pyqtSlot(int)
    def on_sb_xmin_valueChanged(self):
        self.maincanvas.axes.set_xlim(self.sb_xmin.value(), self.sb_xmax.value())
        self.maincanvas.draw()

    @QtCore.pyqtSlot(int)
    def on_sb_xmax_valueChanged(self):
        self.maincanvas.axes.set_xlim(self.sb_xmin.value(), self.sb_xmax.value())
        self.maincanvas.draw()

    @QtCore.pyqtSlot(int)
    def on_sb_ymin_valueChanged(self):
        self.maincanvas.axes.set_ylim(self.sb_ymin.value(), self.sb_ymax.value())
        self.maincanvas.draw()

    @QtCore.pyqtSlot(int)
    def on_sb_ymax_valueChanged(self):
        self.maincanvas.axes.set_ylim(self.sb_ymin.value(), self.sb_ymax.value())
        self.maincanvas.draw()
    # ------------------------------------------------------------------------------------

    # Funciones de los botones accionados por el usuario para controlar el inicio y el final
    # del ensayo

    @QtCore.pyqtSlot()
    def on_pb_start_clicked(self):
        self.Dilatometer_test()
        self.pb_start.setEnabled(False)

    @QtCore.pyqtSlot()
    def on_pb_end_clicked(self):
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
        for line in header.split('\n'):
            self.comented_header = self.comented_header + self.le_output_file_commentchar.text() + line + '\n'

        labels = self.le_output_file_commentchar.text() + 'Tiempo (s) \t Temperatura (C)  \t Deformacion (um) \t Temperatura (mV) \t Deformacion (V) \n'
        # Encabezado mas linea de encabezados de tabla.
        self.comented_header = self.comented_header + labels
        # Lee el archivo de salida completo y agrega al inicio y al final
        # el encabezado y el pie de pagina. -----------------------------
        f = open(self.le_output_file_path.text() + '.txt')
        s = self.comented_header + f.read()
        f.close()

        # Escribe tados los datos con encabezado y pie de pagina incluido
        # nuevamente en el arhivo. ---------------------------------------
        f = open(self.le_output_file_path.text() + '.txt', 'w')
        f.write(s)
        f.close()

        self.pb_start.setEnabled(True)
        self.pb_start_save_data.setEnabled(False)

    @QtCore.pyqtSlot()
    def on_pb_start_save_data_clicked(self):
        self.pb_start_save_data.setEnabled(False)
        self.dilatometria.time_stamp = 0
        self.dilatometria.zero_time = time.time()
        self.maincanvas.axes.cla()
        self.maincanvas.axes.grid(True)
        self.auxcanvas_2.axes.cla()
        self.auxcanvas_2.axes.grid(True)
        self.auxcanvas_1.axes.cla()
        self.auxcanvas_1.axes.grid(True)
        self.dilatometria.savedata = True
        self.read_data = True
    # -----------------------------------------------------------------------------------

    def Dilatometer_test(self):
        # inicializar archivos leer configuraciones inicializar puerto serie
        outfile = self.le_output_file_path.text()
        if outfile == '':
            self.statusBar.showMessage('El campo que indica el archivo de destino no puede estar vacio')
        else:
            outfile += '.txt'

            # Nombres que identifican los multimetros utilizados para la adquisicion de datos
            # Configuracion de entradas
            # (type:      'pyvisa' o 'mcc' o pyserial
            #  channel:   'pyvisa_address', (board, channel)), port
            lvdt_index = self.cbx_dilatometer_lvdt_input.currentIndex() 
            lvdt = {'type': self.cbx_dilatometer_lvdt_input.itemData(lvdt_index),
                    'channel':(self.cbx_dilatometer_lvdt_channel.currentText(),
                               self.sb_lvdt_board_num.value()) if self.cbx_dilatometer_lvdt_input.itemData(lvdt_index) == 'mcc'
                               else self.cbx_dilatometer_lvdt_channel.currentText()
                    }

            temperature = {'type': 'pyvisa' if self.cbx_dilatometer_temperature_input.currentText() == 'Agilent Multimeter' else 'mcc',
                           'channel':self.cbx_dilatometer_temperature_channel.itemData(self.cbx_dilatometer_temperature_channel.currentIndex()).toString() if self.cbx_dilatometer_temperature_input.currentText() == 'Agilent Multimeter' else 
                                    (self.cbx_dilatometer_temperature_channel.currentText(), self.sb_temperature_board_num.value())}

            # print (self.dsb_lvdt_calibration_factor.value())
            # outfile,
            # lvdt,
            # temperature,
            # lvdt_calibration,
            # data_per_second

            self.dilatometria.test(outfile,
                                   lvdt,
                                   temperature,
                                   self.dsb_lvdt_calibration_factor.value(),
                                   self.sb_data_per_second.value())
            self.count = 0
            self.pb_start_save_data.setEnabled(True)
            self.pb_end.setEnabled(True)

    @QtCore.pyqtSlot()
    def show_incoming_data(self, data):
        del data
        if self.read_data:
            f = open(self.le_output_file_path.text() + '.txt')
            s = StringIO(f.read())
            f.close()
            s.seek(0)

            time_np, temp, lvdt = np.genfromtxt(s,
                                                usecols=(0, 1, 2),
                                                deletechars="\n",
                                                dtype=float,
                                                # comment='%',
                                                autostrip=True,
                                                unpack=True)

            # Muestra el tiempo transcurrido
            # Segundos
            if time_np[-1] < 60:
                self.lcd_time_second.display(str(int(time_np[-1])))

            # Minutos---------------------------------------------------
            else:
                # Minutos
                m = time_np[-1] // 60
                # Segundos
                s = time_np[-1] % 60

                # Si no paso mas de una hora se muestra solo minutos y segundos
                if m < 60:
                    self.lcd_time_second.display(str(int(s)))
                    self.lcd_time_minute.display(str(int(m)))
                # Horas--------------------------------------------------
                else:
                    # Horas
                    h = m // 60
                    # Minutos
                    m = m % 60
                    self.lcd_time_second.display(str(int(s)))
                    self.lcd_time_minute.display(str(int(m)))
                    self.lcd_time_hour.display(str(int(h)))
                # -------------------------------------------------------
            # Muestra Valor de temperatura
            self.lcd_var_1.display(str(temp[-1]))
            # Muestra Valor del LVDT
            self.lcd_var_3.display(str(lvdt[-1]))

            # Muestra las pendientes de la recta de temperatura formada
            # en funcion del tiempo (tomando solo los ultimpos 150 valores
            if np.size(lvdt) >= 30:
                temp_a = np.polyfit(time_np[-149:-1] / 60, temp[-149:-1], 1)[0]
                self.lcd_var_2.display(str(temp_a))

            # Ploteando en los canvas ya definidos con las funciones heredadas de la clase canvas
            # Deformacion en funcion de temperatura
            self.maincanvas.axes.cla()
            self.maincanvas.axes.grid(True)
            self.statusBar.showMessage('Ploteando principal...')
            self.maincanvas.axes.set_xlim(self.sb_xmin.value(), self.sb_xmax.value())
            self.maincanvas.axes.set_ylim(self.sb_ymin.value(), self.sb_ymax.value())
            self.maincanvas.axes.plot(temp, lvdt, 'og')
            self.maincanvas.fig.canvas.draw()

            if np.size(time_np) < 300:
                # Temperatura en funcion de tiempo
                self.auxcanvas_1.axes.cla()
                self.auxcanvas_1.axes.grid(True)
                self.statusBar.showMessage('Ploteando Auxiliar 1...')
                self.auxcanvas_1.axes.set_xlim(time_np[0], time_np[-1])
                self.auxcanvas_1.axes.set_ylim(np.min(temp) - abs(np.min(temp) * 20 / 100),
                                               np.max(temp) + abs(np.max(temp) * 20 / 100))
                self.auxcanvas_1.axes.plot(time_np, temp, 'blue')
                for label in self.auxcanvas_1.axes.get_xticklabels():
                    label.set_rotation(45)
                self.auxcanvas_1.fig.canvas.draw()

                # Deformacion en funcion de tiempo
                self.auxcanvas_2.axes.cla()
                self.auxcanvas_2.axes.grid(True)
                self.statusBar.showMessage('Ploteando Auxiliar 2...')
                self.auxcanvas_2.axes.set_xlim(time_np[0], time_np[-1])
                self.auxcanvas_2.axes.set_ylim(np.min(lvdt) - (np.max(lvdt) - np.min(lvdt)) * 10 / 100,
                                               np.max(lvdt) + (np.max(lvdt) - np.min(lvdt)) * 10 / 100)
                self.auxcanvas_2.axes.plot(time_np, lvdt, 'red')
                for label in self.auxcanvas_2.axes.get_xticklabels():

                    label.set_rotation(45)
                self.auxcanvas_2.fig.canvas.draw()
            else:
                # Temperatura en funcion de tiempo
                self.auxcanvas_1.axes.cla()
                self.auxcanvas_1.axes.grid(True)
                self.statusBar.showMessage('Ploteando Auxiliar 1...')
                self.auxcanvas_1.axes.set_xlim(time_np[-299], time_np[-1])
                self.auxcanvas_1.axes.set_ylim(np.min(temp[-299:-1]) - abs(np.min(temp[-299:-1]) * 20 / 100),
                                               np.max(temp[-299:-1]) + abs(np.max(temp[-299:-1]) * 20 / 100))
                self.auxcanvas_1.axes.plot(time_np[-299:-1], temp[-299:-1], 'blue')
                for label in self.auxcanvas_1.axes.get_xticklabels():
                    label.set_rotation(45)
                self.auxcanvas_1.fig.canvas.draw()

                # Deformacion en funcion de tiempo
                self.auxcanvas_2.axes.cla()
                self.auxcanvas_2.axes.grid(True)
                self.statusBar.showMessage('Ploteando Auxiliar 2...')
                self.auxcanvas_2.axes.set_xlim(time_np[-299], time_np[-1])
                self.auxcanvas_2.axes.set_ylim(np.min(lvdt[-299:-1]) - (np.max(lvdt[-299:-1]) - np.min(lvdt[-299:-1])) * 10 / 100,
                                               np.max(lvdt[-299:-1]) + (np.max(lvdt[-299:-1]) - np.min(lvdt[-299:-1])) * 10 / 100)
                self.auxcanvas_2.axes.plot(time_np[-299:-1], lvdt[-299:-1], 'red')
                for label in self.auxcanvas_2.axes.get_xticklabels():

                    label.set_rotation(45)
                self.auxcanvas_2.fig.canvas.draw()

            del temp, lvdt, time_np

        else:
            f = open('tempdata')
            s = StringIO(f.read())
            f.close()
            s.seek(0)

            data = np.genfromtxt(s,
                                 deletechars="\n",
                                 dtype=float,
                                 autostrip=True,
                                 unpack=True)

            # Muestra el tiempo transcurrido
            # Segundos
            if data[0] < 60:
                self.lcd_time_second.display(str(int(data[0])))
            # Minutos
            else:
                m = data[0] // 60
                s = data[0] % 60

                # Si no paso mas de una hora se muestra solo minutos y segundos
                if m < 60:
                    self.lcd_time_second.display(str(int(s)))
                    self.lcd_time_minute.display(str(int(m)))
                # Horas--------------------------------------------------
                else:
                    h = m // 60
                    m = m % 60

                    self.lcd_time_second.display(str(int(s)))
                    self.lcd_time_minute.display(str(int(m)))
                    self.lcd_time_hour.display(str(int(h)))
            # ---------------------------------------------------------------------------

            # Muestra el valor de tempperatura en el display
            # Muestra valor de temperatura
            self.lcd_var_1.display(str(data[1]))
            # Muestra valor de LVDT
            self.lcd_var_3.display(str(data[2]))

            del data
            # --------------------------------------------------------------------------------

    @QtCore.pyqtSlot()
    def on_tlb_output_file_path_pressed(self):
        # seleccionar archivo
        self.le_output_file_path.setText(QtGui.QFileDialog.getSaveFileName(parent=self,
                                                                           caption='Select Output File',
                                                                           directory=os.path.expanduser(self.config['OutputFile']['output_file_base_dir'])))

    def on_pb_save_config_pressed(self):

        self.config.filename = QtGui.QFileDialog.getSaveFileName(parent=self,
                                                                 caption='Select Config File',
                                                                 directory=os.path.expanduser(self.config['OutputFile']['output_file_base_dir']))
        self.config.write()

    def on_pb_load_config_pressed(self):

        self.config_file = QtGui.QFileDialog.getOpenFileName(self,
                                                             'Load config File',
                                                             directory=os.path.expanduser(self.config['OutputFile']['output_file_base_dir']))
        self.load_config()

    def load_config(self, default=False):
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
                warn = str(time.time()) + 'Default config file not found'
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
                warn = str(time.time()) + 'Selected config file not found'
                logging.warning(warn)


def main():

    logging.basicConfig(filename='./dilatometro_log.txt',
                        level=logging.WARNING)
    app = QtGui.QApplication(sys.argv)
    DAQ = Main()
    # Create a pixmap - not needed if you have your own.
    DAQ.splash.show()
    DAQ.splash.showMessage('DILATOMETRO Ver.:1.0a\n Loading User Interface...', QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
    for i in range(0, 101):
        DAQ.splash.progressBar.setValue(i)
        # Do something which takes some time.
        t = time.time()
        while time.time() < t + 0.1:
            app.processEvents()

    DAQ.show()
    DAQ.splash.finish(DAQ)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
