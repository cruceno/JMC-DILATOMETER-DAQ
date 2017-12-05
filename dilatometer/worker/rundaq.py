import time
import logging
from PyQt4 import QtCore
from dilatometer.instrument.MultimetrosAgilent import AG344XXA
from dilatometer.instrument.PlacasMeasureComputing import ULINPUT
import dilatometer.UniversalLibrary as UL
import serial

class Test_Dilatometria (QtCore.QThread):

    # Inicio de la clase Qthread
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.exiting = False
    # Funcion que va a ser llamada desde otro proceso para iniciar este hilo que lleva a
    # cabo la medicion

    def test(self,
             outfile,
             lvdt,
             temperature,
             lvdt_calibration,
             data_per_second
             ):

        # Configuracion de entradas
        # (type:      'pyvisa' o 'mcc'
        #  channel:   ('pyvisa_address', (board, channel) )

        if temperature['type'] == 'pyvisa':
            print(temperature['channel'])
            self.termo = AG344XXA(str(temperature['channel']))
            self.termo.dev.write('*RST')
            self.termo.dev.write('CONF:VOLT:DC AUTO')
        elif temperature == "mcc":
            self.termo = ULINPUT(temperature['channel'][1], 'temp', temperature['channel'][0])

        if lvdt['type'] == 'pyvisa':
            self.lvdt = AG344XXA(lvdt['channel'])
            self.lvdt.dev.write('*RST')
            self.lvdt.dev.write('CONF:VOLT:DC AUTO')
        elif lvdt['type'] == 'mcc':
            self.lvdt = ULINPUT(lvdt['channel'][1], 'volt', lvdt['channel'][0])
        elif lvdt['type'] == 'pyserial':
            self.lvdt = serial.Serial(lvdt['channel'],
                                      baudrate=9600,
                                      bytesize=8,
                                      parity='N',
                                      stopbits=1,
                                      timeout=1)
            self.lvdt.readline()

        # Otras configuraciones
        self.time_stamp = 0
        self.delay = 1 / data_per_second
        self.lvdt_calibration = lvdt_calibration
        print(self.lvdt_calibration)
        self.savedata = False
        self.outfile = outfile
        self.errorfile = outfile + '_errorlog.txt'
        self.start()

    # Esta funcion leera continuamente los dispositivos hasta finalizar el ensayo
    def run(self):

        # Variable bandera que indica que es la primera vez qwue corre el proceso
        first = True
        # print 'Abrimos archivo de error'
        # self.error_fsock= open(self.errorfile, 'w')

        while not self.exiting:

            if first:

                self.fsock = open(self.outfile, 'w')
                self.zero_time = time.time()
                first = False

            else:

                self.fsock = open(self.outfile, 'a')
                self.time_stamp = time.time() - self.zero_time

            # =====================================================================================
            # Se usan las entencias "try" y "except" para evitar que se detenga el ensayo
            # si llegara a producirse un error de lectura en alguno de los multimetros utilizados.
            # y a su vez se guarda este error en un archivo para su posterior analisis
            # ======================================================================================
            # Cambia el mensaje enm el dysplay secundario del multimetro
            if self.termo.type == 'pyvisa' and self.termo.message:
                self.termo.dev.write('DISP:WIND2:TEXT "Midiendo ..."')
            elif self.lvdt.type == 'pyvisa' and self.lvdt.message:
                self.lvdt.dev.write('DISP:WIND2:TEXT "Midiendo ..."')

            if self.termo.type == 'pyvisa':
                try:
                    # print 'Midiendo termo'
                    temp_data = self.termo.dev.query('READ?')
                except(IOError):
                    error = str(self.time_stamp)
                    error += '\tError Termocupla :' + self.termo.dev.query('SYST:ERR?') + '\n'
                    logging.error(error)
                    continue
            else:
                temp_data = UL.cbTIn(int(self.termo.board),
                                     int(self.termo.channel),
                                     UL.CELSIUS,
                                     0.0,
                                     UL.FILTER
                                     )

            if self.lvdt.type == 'pyvisa':
                try:
                    # print 'Midiento LVDT'
                    lvdt_data = self.lvdt.dev.query('READ?')
                except():
                    error = str(self.time_stamp) + ':\tError LVDT: ' + self.lvdt.dev.query('SYST:ERR?')
                    logging.error(error)
                    # print error_line
                    continue

            elif self.lvdt.type == 'mcc':
                # print self.lvdt.board
                lvdt_value = UL.cbVIn(int(self.lvdt.board),
                                      int(self.lvdt.channel),
                                      UL.cbGetConfig(UL.BOARDINFO,
                                                     int(self.lvdt.board),
                                                     int(self.lvdt.channel),
                                                     UL.BIRANGE,
                                                     ConfigVal=0
                                                     ),
                                      0.0,
                                      Option=None
                                      )

            elif self.lvdt.type == 'pyserial':
                lvdt_data = self.lvdt.readline().decode().strip('\r\n')

            # print temp_data, lvdt_data
            # ====================================================================================
            temp_data = float(temp_data) * 1000
            lvdt_data = float(lvdt_value)
            lvdt_data_um = float(lvdt_value) * self.lvdt_calibration
            # Pasar de milivoltios a grados celcius
            temp_data_celcius = self.termo.temperature_calibration(temp_data)

#           Guardar array
            data = [self.time_stamp, temp_data_celcius, lvdt_data_um, temp_data, lvdt_data]
            # print data
            # Si se comienza el inicio de grabacion de datos se guardara todo en el archivo de salida
            # indicado
            if self.savedata:
                # print ('Guardando')
                # Muestra mensaje en multimetro AG34410A
                if self.termo.type == 'pyvisa' and self.termo.message:
                    self.termo.dev.write('DISP:WIND2:TEXT "Guardando..."')
                elif self.lvdt.type == 'pyvisa' and self.lvdt.message:
                    self.termo.dev.write('DISP:WIND2:TEXT "Guardando..."')
                # Se arma linea de texto para guardar en el archivo
                line = str(data[0]) + '\t' + str(data[1]) + '\t' + str(data[2]) + '\t' + str(data[3]) + '\t' + str(data[4]) + '\n'
                # Se escribe linea en el archivo
                self.fsock.write(line)
                # Se cierra el archivo
                self.fsock.close()

            # Si no se inicia la grabacion de datos se guardara una sola linea de datos en un archivo temporal
            else:
                # print 'Guardantdo temporal'
                tempfsock = open('tempdata', 'w')
                line = str(data[0]) + '\t' + str(data[1]) + '\t' + str(data[2]) + '\t' + str(data[3]) + '\t' + str(data[4]) + '\n'
                tempfsock.write(line)
                tempfsock.close()
#             print 'Envisar senial'
            self.emit(QtCore.SIGNAL("LVDT_readsignal(PyQt_PyObject)"), data)
            if self.termo.type == 'pyvisa' and self.termo.message:
                self.termo.dev.write('DISP:WIND2:TEXT "En espera..."')
            elif self.lvdt.type == 'pyvisa' and self.lvdt.message:
                self.termo.dev.write('DISP:WIND2:TEXT "En espera..."')
            time.sleep(self.delay)

        if self.termo.type == 'pyvisa' and self.termo.message:
            self.termo.dev.write('DISP:WIND2:TEXT:CLEAR')
        elif self.lvdt.type == 'pyvisa' and self.lvdt.message:
            self.lvdt.dev.write('DISP:WIND2:TEXT:CLEAR')
        self.fsock.close()

        self.exit()

    def __del__(self):
        self.exiting = True
        self.wait()
