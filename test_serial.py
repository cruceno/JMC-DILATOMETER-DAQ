'''
Created on 6 jul. 2017

@author: javier
'''

import serial
from time import sleep, time

ser = serial.Serial('/dev/ttyUSB1',
                    baudrate=9600,
                    bytesize=8,
                    stopbits=1,
                    parity='N')

# ser.write(b'READ?\x0a')
# sleep(0.1)
# print (ser.readline())
with ser as s:
    t = time()
    s.flushOutput()
    s.flushOutput()
    sleep(0.3)
    cmd=b'READ?\n'
    while True:
        #print ('Escribiendo')
        #ser.write('READ?\x0a'.encode('ascii'))
        s.write(cmd)
        #print('Leyendo')
        print(s.readline(),time()-t)
        t=time()

