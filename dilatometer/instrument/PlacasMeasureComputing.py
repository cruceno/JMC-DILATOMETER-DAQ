'''
Created on 4 abr. 2017

@author: cruce
'''


class ULINPUT(object):
    def __init__(self, board, inputType, channel):
        self.board = board
        self.inputType = inputType
        self.channel = channel
        self.type = 'mcc'

    def temperature_calibration(self, temp_data):
        # Pasar de milivoltios a gracdos centigrado el valor leido por el multimetro
        # Polinomio para rango intermedio  -272 a 150 C
        if temp_data < 2:

            Y = 25.39459 * temp_data
            Y -= 0.44494 * temp_data ** 2
            Y += 0.05652 * temp_data ** 3
            Y -= 0.00412 * temp_data ** 4
            Y += 0.0011 * temp_data ** 5
            Y -= 1.39776E-4 * temp_data ** 6
            Y += 4.40583E-6 * temp_data ** 7
            Y += 7.709E-8 * temp_data ** 8

        # Polinomio para rango positivo 0 a 500 C
        if temp_data >= 2:

            Y = 25.26032 * temp_data
            Y -= 0.57128 * temp_data ** 2
            Y += 0.13393 * temp_data ** 3
            Y -= 0.01411 * temp_data ** 4
            Y += 7.7329E-4 * temp_data ** 5
            Y -= 2.32438E-5 * temp_data ** 6
            Y += 3.64924E-7 * temp_data ** 7
            Y -= 2.34283E-9 * temp_data ** 8

        return Y
