# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '..\..\DilatometroUI.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(983, 681)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_5 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.tabmainwidget = QtGui.QTabWidget(self.centralwidget)
        self.tabmainwidget.setEnabled(True)
        self.tabmainwidget.setObjectName(_fromUtf8("tabmainwidget"))
        self.tab_output_config = QtGui.QWidget()
        self.tab_output_config.setObjectName(_fromUtf8("tab_output_config"))
        self.gridLayout_4 = QtGui.QGridLayout(self.tab_output_config)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.gb_output_file = QtGui.QGroupBox(self.tab_output_config)
        self.gb_output_file.setCheckable(False)
        self.gb_output_file.setChecked(False)
        self.gb_output_file.setObjectName(_fromUtf8("gb_output_file"))
        self.gridLayout_8 = QtGui.QGridLayout(self.gb_output_file)
        self.gridLayout_8.setObjectName(_fromUtf8("gridLayout_8"))
        self.lb_output_file_commentchar = QtGui.QLabel(self.gb_output_file)
        self.lb_output_file_commentchar.setObjectName(_fromUtf8("lb_output_file_commentchar"))
        self.gridLayout_8.addWidget(self.lb_output_file_commentchar, 1, 0, 1, 3)
        self.le_output_file_commentchar = QtGui.QLineEdit(self.gb_output_file)
        self.le_output_file_commentchar.setText(_fromUtf8(""))
        self.le_output_file_commentchar.setObjectName(_fromUtf8("le_output_file_commentchar"))
        self.gridLayout_8.addWidget(self.le_output_file_commentchar, 1, 3, 1, 1)
        self.tlb_output_file_path = QtGui.QToolButton(self.gb_output_file)
        self.tlb_output_file_path.setObjectName(_fromUtf8("tlb_output_file_path"))
        self.gridLayout_8.addWidget(self.tlb_output_file_path, 0, 4, 1, 1)
        self.gb_header = QtGui.QGroupBox(self.gb_output_file)
        self.gb_header.setObjectName(_fromUtf8("gb_header"))
        self.gridLayout_14 = QtGui.QGridLayout(self.gb_header)
        self.gridLayout_14.setObjectName(_fromUtf8("gridLayout_14"))
        self.ptx_header = QtGui.QPlainTextEdit(self.gb_header)
        self.ptx_header.setObjectName(_fromUtf8("ptx_header"))
        self.gridLayout_14.addWidget(self.ptx_header, 0, 0, 1, 1)
        self.gridLayout_8.addWidget(self.gb_header, 2, 0, 1, 5)
        self.lb_output_file_path = QtGui.QLabel(self.gb_output_file)
        self.lb_output_file_path.setObjectName(_fromUtf8("lb_output_file_path"))
        self.gridLayout_8.addWidget(self.lb_output_file_path, 0, 0, 1, 1)
        self.le_output_file_path = QtGui.QLineEdit(self.gb_output_file)
        self.le_output_file_path.setText(_fromUtf8(""))
        self.le_output_file_path.setObjectName(_fromUtf8("le_output_file_path"))
        self.gridLayout_8.addWidget(self.le_output_file_path, 0, 1, 1, 3)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_8.addItem(spacerItem, 1, 4, 1, 1)
        self.gridLayout_4.addWidget(self.gb_output_file, 0, 0, 1, 3)
        self.pb_save_config = QtGui.QPushButton(self.tab_output_config)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_save_config.sizePolicy().hasHeightForWidth())
        self.pb_save_config.setSizePolicy(sizePolicy)
        self.pb_save_config.setObjectName(_fromUtf8("pb_save_config"))
        self.gridLayout_4.addWidget(self.pb_save_config, 2, 0, 1, 1)
        self.pb_load_config = QtGui.QPushButton(self.tab_output_config)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_load_config.sizePolicy().hasHeightForWidth())
        self.pb_load_config.setSizePolicy(sizePolicy)
        self.pb_load_config.setObjectName(_fromUtf8("pb_load_config"))
        self.gridLayout_4.addWidget(self.pb_load_config, 2, 1, 1, 1)
        self.gb_dilatometer_test_config = QtGui.QGroupBox(self.tab_output_config)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gb_dilatometer_test_config.sizePolicy().hasHeightForWidth())
        self.gb_dilatometer_test_config.setSizePolicy(sizePolicy)
        self.gb_dilatometer_test_config.setCheckable(False)
        self.gb_dilatometer_test_config.setChecked(False)
        self.gb_dilatometer_test_config.setObjectName(_fromUtf8("gb_dilatometer_test_config"))
        self.gridLayout_3 = QtGui.QGridLayout(self.gb_dilatometer_test_config)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.lb_dilatometer_termperature_input = QtGui.QLabel(self.gb_dilatometer_test_config)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb_dilatometer_termperature_input.sizePolicy().hasHeightForWidth())
        self.lb_dilatometer_termperature_input.setSizePolicy(sizePolicy)
        self.lb_dilatometer_termperature_input.setObjectName(_fromUtf8("lb_dilatometer_termperature_input"))
        self.gridLayout_3.addWidget(self.lb_dilatometer_termperature_input, 1, 0, 1, 1)
        self.cbx_dilatometer_temperature_channel = QtGui.QComboBox(self.gb_dilatometer_test_config)
        self.cbx_dilatometer_temperature_channel.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbx_dilatometer_temperature_channel.sizePolicy().hasHeightForWidth())
        self.cbx_dilatometer_temperature_channel.setSizePolicy(sizePolicy)
        self.cbx_dilatometer_temperature_channel.setObjectName(_fromUtf8("cbx_dilatometer_temperature_channel"))
        self.gridLayout_3.addWidget(self.cbx_dilatometer_temperature_channel, 1, 2, 1, 1)
        self.cbx_dilatometer_temperature_input = QtGui.QComboBox(self.gb_dilatometer_test_config)
        self.cbx_dilatometer_temperature_input.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbx_dilatometer_temperature_input.sizePolicy().hasHeightForWidth())
        self.cbx_dilatometer_temperature_input.setSizePolicy(sizePolicy)
        self.cbx_dilatometer_temperature_input.setEditable(False)
        self.cbx_dilatometer_temperature_input.setFrame(True)
        self.cbx_dilatometer_temperature_input.setObjectName(_fromUtf8("cbx_dilatometer_temperature_input"))
        self.cbx_dilatometer_temperature_input.addItem(_fromUtf8(""))
        self.cbx_dilatometer_temperature_input.addItem(_fromUtf8(""))
        self.gridLayout_3.addWidget(self.cbx_dilatometer_temperature_input, 1, 1, 1, 1)
        self.cbx_dilatometer_lvdt_input = QtGui.QComboBox(self.gb_dilatometer_test_config)
        self.cbx_dilatometer_lvdt_input.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbx_dilatometer_lvdt_input.sizePolicy().hasHeightForWidth())
        self.cbx_dilatometer_lvdt_input.setSizePolicy(sizePolicy)
        self.cbx_dilatometer_lvdt_input.setObjectName(_fromUtf8("cbx_dilatometer_lvdt_input"))
        self.cbx_dilatometer_lvdt_input.addItem(_fromUtf8(""))
        self.cbx_dilatometer_lvdt_input.addItem(_fromUtf8(""))
        self.gridLayout_3.addWidget(self.cbx_dilatometer_lvdt_input, 2, 1, 1, 1)
        self.lb_dilatometer_lvdt_input = QtGui.QLabel(self.gb_dilatometer_test_config)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb_dilatometer_lvdt_input.sizePolicy().hasHeightForWidth())
        self.lb_dilatometer_lvdt_input.setSizePolicy(sizePolicy)
        self.lb_dilatometer_lvdt_input.setObjectName(_fromUtf8("lb_dilatometer_lvdt_input"))
        self.gridLayout_3.addWidget(self.lb_dilatometer_lvdt_input, 2, 0, 1, 1)
        self.cbx_dilatometer_lvdt_channel = QtGui.QComboBox(self.gb_dilatometer_test_config)
        self.cbx_dilatometer_lvdt_channel.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbx_dilatometer_lvdt_channel.sizePolicy().hasHeightForWidth())
        self.cbx_dilatometer_lvdt_channel.setSizePolicy(sizePolicy)
        self.cbx_dilatometer_lvdt_channel.setObjectName(_fromUtf8("cbx_dilatometer_lvdt_channel"))
        self.gridLayout_3.addWidget(self.cbx_dilatometer_lvdt_channel, 2, 2, 1, 1)
        self.sb_temperature_board_num = QtGui.QSpinBox(self.gb_dilatometer_test_config)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sb_temperature_board_num.sizePolicy().hasHeightForWidth())
        self.sb_temperature_board_num.setSizePolicy(sizePolicy)
        self.sb_temperature_board_num.setObjectName(_fromUtf8("sb_temperature_board_num"))
        self.gridLayout_3.addWidget(self.sb_temperature_board_num, 1, 3, 1, 1)
        self.sb_lvdt_board_num = QtGui.QSpinBox(self.gb_dilatometer_test_config)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sb_lvdt_board_num.sizePolicy().hasHeightForWidth())
        self.sb_lvdt_board_num.setSizePolicy(sizePolicy)
        self.sb_lvdt_board_num.setObjectName(_fromUtf8("sb_lvdt_board_num"))
        self.gridLayout_3.addWidget(self.sb_lvdt_board_num, 2, 3, 1, 1)
        self.lb_device_channel = QtGui.QLabel(self.gb_dilatometer_test_config)
        self.lb_device_channel.setObjectName(_fromUtf8("lb_device_channel"))
        self.gridLayout_3.addWidget(self.lb_device_channel, 0, 2, 1, 1)
        self.lb_ad_device = QtGui.QLabel(self.gb_dilatometer_test_config)
        self.lb_ad_device.setObjectName(_fromUtf8("lb_ad_device"))
        self.gridLayout_3.addWidget(self.lb_ad_device, 0, 1, 1, 1)
        self.lb_board_num = QtGui.QLabel(self.gb_dilatometer_test_config)
        self.lb_board_num.setObjectName(_fromUtf8("lb_board_num"))
        self.gridLayout_3.addWidget(self.lb_board_num, 0, 3, 1, 1)
        self.sb_data_per_second = QtGui.QSpinBox(self.gb_dilatometer_test_config)
        self.sb_data_per_second.setMinimum(1)
        self.sb_data_per_second.setProperty("value", 1)
        self.sb_data_per_second.setObjectName(_fromUtf8("sb_data_per_second"))
        self.gridLayout_3.addWidget(self.sb_data_per_second, 3, 1, 1, 1)
        self.dsb_lvdt_calibration_factor = QtGui.QDoubleSpinBox(self.gb_dilatometer_test_config)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dsb_lvdt_calibration_factor.sizePolicy().hasHeightForWidth())
        self.dsb_lvdt_calibration_factor.setSizePolicy(sizePolicy)
        self.dsb_lvdt_calibration_factor.setDecimals(4)
        self.dsb_lvdt_calibration_factor.setMinimum(-999999.0)
        self.dsb_lvdt_calibration_factor.setMaximum(999999.0)
        self.dsb_lvdt_calibration_factor.setProperty("value", 1.0)
        self.dsb_lvdt_calibration_factor.setObjectName(_fromUtf8("dsb_lvdt_calibration_factor"))
        self.gridLayout_3.addWidget(self.dsb_lvdt_calibration_factor, 2, 4, 1, 1)
        self.lb_data_per_second = QtGui.QLabel(self.gb_dilatometer_test_config)
        self.lb_data_per_second.setObjectName(_fromUtf8("lb_data_per_second"))
        self.gridLayout_3.addWidget(self.lb_data_per_second, 3, 0, 1, 1)
        self.lb_lvdt_calibration = QtGui.QLabel(self.gb_dilatometer_test_config)
        self.lb_lvdt_calibration.setObjectName(_fromUtf8("lb_lvdt_calibration"))
        self.gridLayout_3.addWidget(self.lb_lvdt_calibration, 0, 4, 1, 1)
        self.lb_dilatometer_termperature_input.raise_()
        self.lb_dilatometer_lvdt_input.raise_()
        self.cbx_dilatometer_temperature_input.raise_()
        self.cbx_dilatometer_lvdt_input.raise_()
        self.cbx_dilatometer_lvdt_channel.raise_()
        self.cbx_dilatometer_temperature_channel.raise_()
        self.sb_temperature_board_num.raise_()
        self.sb_lvdt_board_num.raise_()
        self.lb_ad_device.raise_()
        self.lb_device_channel.raise_()
        self.lb_board_num.raise_()
        self.sb_data_per_second.raise_()
        self.dsb_lvdt_calibration_factor.raise_()
        self.lb_data_per_second.raise_()
        self.lb_lvdt_calibration.raise_()
        self.gridLayout_4.addWidget(self.gb_dilatometer_test_config, 1, 0, 1, 3)
        spacerItem1 = QtGui.QSpacerItem(20, 46, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem1, 5, 0, 1, 2)
        self.tabmainwidget.addTab(self.tab_output_config, _fromUtf8(""))
        self.tab_plots = QtGui.QWidget()
        self.tab_plots.setObjectName(_fromUtf8("tab_plots"))
        self.gridLayout = QtGui.QGridLayout(self.tab_plots)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.gb_auxplot_1 = QtGui.QGroupBox(self.tab_plots)
        self.gb_auxplot_1.setMinimumSize(QtCore.QSize(247, 181))
        self.gb_auxplot_1.setObjectName(_fromUtf8("gb_auxplot_1"))
        self.gridLayout.addWidget(self.gb_auxplot_1, 0, 0, 2, 1)
        self.gb_time = QtGui.QGroupBox(self.tab_plots)
        self.gb_time.setMinimumSize(QtCore.QSize(201, 81))
        self.gb_time.setMaximumSize(QtCore.QSize(201, 81))
        self.gb_time.setObjectName(_fromUtf8("gb_time"))
        self.gridLayout_2 = QtGui.QGridLayout(self.gb_time)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.lcd_time_hour = QtGui.QLCDNumber(self.gb_time)
        self.lcd_time_hour.setSmallDecimalPoint(False)
        self.lcd_time_hour.setNumDigits(2)
        self.lcd_time_hour.setDigitCount(2)
        self.lcd_time_hour.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.lcd_time_hour.setProperty("value", 0.0)
        self.lcd_time_hour.setProperty("intValue", 0)
        self.lcd_time_hour.setObjectName(_fromUtf8("lcd_time_hour"))
        self.gridLayout_2.addWidget(self.lcd_time_hour, 0, 0, 1, 1)
        self.lcd_time_minute = QtGui.QLCDNumber(self.gb_time)
        self.lcd_time_minute.setNumDigits(2)
        self.lcd_time_minute.setDigitCount(2)
        self.lcd_time_minute.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.lcd_time_minute.setProperty("intValue", 0)
        self.lcd_time_minute.setObjectName(_fromUtf8("lcd_time_minute"))
        self.gridLayout_2.addWidget(self.lcd_time_minute, 0, 1, 1, 1)
        self.lcd_time_second = QtGui.QLCDNumber(self.gb_time)
        self.lcd_time_second.setNumDigits(2)
        self.lcd_time_second.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.lcd_time_second.setProperty("intValue", 0)
        self.lcd_time_second.setObjectName(_fromUtf8("lcd_time_second"))
        self.gridLayout_2.addWidget(self.lcd_time_second, 0, 2, 1, 1)
        self.gridLayout.addWidget(self.gb_time, 0, 1, 1, 1)
        self.gb_var_1 = QtGui.QGroupBox(self.tab_plots)
        self.gb_var_1.setMinimumSize(QtCore.QSize(141, 81))
        self.gb_var_1.setMaximumSize(QtCore.QSize(141, 81))
        self.gb_var_1.setObjectName(_fromUtf8("gb_var_1"))
        self.gridLayout_10 = QtGui.QGridLayout(self.gb_var_1)
        self.gridLayout_10.setObjectName(_fromUtf8("gridLayout_10"))
        self.lcd_var_1 = QtGui.QLCDNumber(self.gb_var_1)
        self.lcd_var_1.setSmallDecimalPoint(True)
        self.lcd_var_1.setNumDigits(5)
        self.lcd_var_1.setDigitCount(5)
        self.lcd_var_1.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.lcd_var_1.setProperty("value", 0.0)
        self.lcd_var_1.setProperty("intValue", 0)
        self.lcd_var_1.setObjectName(_fromUtf8("lcd_var_1"))
        self.gridLayout_10.addWidget(self.lcd_var_1, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.gb_var_1, 0, 2, 1, 1)
        self.gb_var_2 = QtGui.QGroupBox(self.tab_plots)
        self.gb_var_2.setMinimumSize(QtCore.QSize(141, 81))
        self.gb_var_2.setObjectName(_fromUtf8("gb_var_2"))
        self.gridLayout_11 = QtGui.QGridLayout(self.gb_var_2)
        self.gridLayout_11.setObjectName(_fromUtf8("gridLayout_11"))
        self.lcd_var_2 = QtGui.QLCDNumber(self.gb_var_2)
        self.lcd_var_2.setSmallDecimalPoint(True)
        self.lcd_var_2.setNumDigits(4)
        self.lcd_var_2.setDigitCount(4)
        self.lcd_var_2.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.lcd_var_2.setProperty("value", 0.0)
        self.lcd_var_2.setProperty("intValue", 0)
        self.lcd_var_2.setObjectName(_fromUtf8("lcd_var_2"))
        self.gridLayout_11.addWidget(self.lcd_var_2, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.gb_var_2, 0, 3, 1, 1)
        self.gb_mainplot = QtGui.QGroupBox(self.tab_plots)
        self.gb_mainplot.setMinimumSize(QtCore.QSize(650, 407))
        self.gb_mainplot.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.gb_mainplot.setObjectName(_fromUtf8("gb_mainplot"))
        self.gridLayout.addWidget(self.gb_mainplot, 1, 1, 3, 4)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 3, 0, 1, 1)
        self.gb_auxplot_2 = QtGui.QGroupBox(self.tab_plots)
        self.gb_auxplot_2.setMinimumSize(QtCore.QSize(247, 181))
        self.gb_auxplot_2.setObjectName(_fromUtf8("gb_auxplot_2"))
        self.gridLayout.addWidget(self.gb_auxplot_2, 2, 0, 1, 1)
        self.pb_start = QtGui.QPushButton(self.tab_plots)
        self.pb_start.setIconSize(QtCore.QSize(40, 40))
        self.pb_start.setObjectName(_fromUtf8("pb_start"))
        self.gridLayout.addWidget(self.pb_start, 4, 0, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(20, 78, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 4, 3, 3, 1)
        self.gb_scale_mainplot_controls = QtGui.QGroupBox(self.tab_plots)
        self.gb_scale_mainplot_controls.setObjectName(_fromUtf8("gb_scale_mainplot_controls"))
        self.gridLayout_24 = QtGui.QGridLayout(self.gb_scale_mainplot_controls)
        self.gridLayout_24.setObjectName(_fromUtf8("gridLayout_24"))
        self.lb_x_min = QtGui.QLabel(self.gb_scale_mainplot_controls)
        self.lb_x_min.setObjectName(_fromUtf8("lb_x_min"))
        self.gridLayout_24.addWidget(self.lb_x_min, 0, 0, 1, 1)
        self.sb_xmin = QtGui.QSpinBox(self.gb_scale_mainplot_controls)
        self.sb_xmin.setMinimum(-200)
        self.sb_xmin.setMaximum(500)
        self.sb_xmin.setProperty("value", 0)
        self.sb_xmin.setObjectName(_fromUtf8("sb_xmin"))
        self.gridLayout_24.addWidget(self.sb_xmin, 0, 1, 1, 1)
        self.lb_x_max = QtGui.QLabel(self.gb_scale_mainplot_controls)
        self.lb_x_max.setObjectName(_fromUtf8("lb_x_max"))
        self.gridLayout_24.addWidget(self.lb_x_max, 0, 3, 1, 1)
        self.sb_xmax = QtGui.QSpinBox(self.gb_scale_mainplot_controls)
        self.sb_xmax.setSuffix(_fromUtf8(""))
        self.sb_xmax.setMinimum(-200)
        self.sb_xmax.setMaximum(500)
        self.sb_xmax.setObjectName(_fromUtf8("sb_xmax"))
        self.gridLayout_24.addWidget(self.sb_xmax, 0, 4, 1, 1)
        self.lb_y_min = QtGui.QLabel(self.gb_scale_mainplot_controls)
        self.lb_y_min.setObjectName(_fromUtf8("lb_y_min"))
        self.gridLayout_24.addWidget(self.lb_y_min, 1, 0, 1, 1)
        self.lb_y_max = QtGui.QLabel(self.gb_scale_mainplot_controls)
        self.lb_y_max.setObjectName(_fromUtf8("lb_y_max"))
        self.gridLayout_24.addWidget(self.lb_y_max, 1, 3, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_24.addItem(spacerItem4, 0, 5, 1, 1)
        self.sb_ymin = QtGui.QDoubleSpinBox(self.gb_scale_mainplot_controls)
        self.sb_ymin.setDecimals(3)
        self.sb_ymin.setMinimum(-3.0)
        self.sb_ymin.setMaximum(3.0)
        self.sb_ymin.setSingleStep(0.01)
        self.sb_ymin.setProperty("value", -1.0)
        self.sb_ymin.setObjectName(_fromUtf8("sb_ymin"))
        self.gridLayout_24.addWidget(self.sb_ymin, 1, 1, 1, 1)
        self.sb_ymax = QtGui.QDoubleSpinBox(self.gb_scale_mainplot_controls)
        self.sb_ymax.setDecimals(3)
        self.sb_ymax.setMinimum(-3.0)
        self.sb_ymax.setMaximum(3.0)
        self.sb_ymax.setSingleStep(0.01)
        self.sb_ymax.setProperty("value", 1.0)
        self.sb_ymax.setObjectName(_fromUtf8("sb_ymax"))
        self.gridLayout_24.addWidget(self.sb_ymax, 1, 4, 1, 1)
        self.gridLayout.addWidget(self.gb_scale_mainplot_controls, 4, 1, 3, 2)
        self.pb_start_save_data = QtGui.QPushButton(self.tab_plots)
        self.pb_start_save_data.setEnabled(False)
        self.pb_start_save_data.setIconSize(QtCore.QSize(40, 40))
        self.pb_start_save_data.setObjectName(_fromUtf8("pb_start_save_data"))
        self.gridLayout.addWidget(self.pb_start_save_data, 5, 0, 1, 1)
        self.pb_end = QtGui.QPushButton(self.tab_plots)
        self.pb_end.setIconSize(QtCore.QSize(40, 40))
        self.pb_end.setObjectName(_fromUtf8("pb_end"))
        self.gridLayout.addWidget(self.pb_end, 6, 0, 1, 1)
        self.gb_var_3 = QtGui.QGroupBox(self.tab_plots)
        self.gb_var_3.setMinimumSize(QtCore.QSize(141, 81))
        self.gb_var_3.setMaximumSize(QtCore.QSize(141, 81))
        self.gb_var_3.setObjectName(_fromUtf8("gb_var_3"))
        self.gridLayout_12 = QtGui.QGridLayout(self.gb_var_3)
        self.gridLayout_12.setObjectName(_fromUtf8("gridLayout_12"))
        self.lcd_var_3 = QtGui.QLCDNumber(self.gb_var_3)
        self.lcd_var_3.setSmallDecimalPoint(True)
        self.lcd_var_3.setNumDigits(5)
        self.lcd_var_3.setDigitCount(5)
        self.lcd_var_3.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.lcd_var_3.setProperty("value", 0.0)
        self.lcd_var_3.setProperty("intValue", 0)
        self.lcd_var_3.setObjectName(_fromUtf8("lcd_var_3"))
        self.gridLayout_12.addWidget(self.lcd_var_3, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.gb_var_3, 0, 4, 1, 1)
        self.tabmainwidget.addTab(self.tab_plots, _fromUtf8(""))
        self.gridLayout_5.addWidget(self.tabmainwidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        self.tabmainwidget.setCurrentIndex(0)
        self.cbx_dilatometer_lvdt_input.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.gb_output_file.setTitle(_translate("MainWindow", "Archivo de Salida", None))
        self.lb_output_file_commentchar.setText(_translate("MainWindow", "Caracter de comentario", None))
        self.tlb_output_file_path.setText(_translate("MainWindow", "...", None))
        self.gb_header.setTitle(_translate("MainWindow", "Encabezado", None))
        self.lb_output_file_path.setText(_translate("MainWindow", "Ruta", None))
        self.pb_save_config.setText(_translate("MainWindow", "Save Experiment Config", None))
        self.pb_load_config.setText(_translate("MainWindow", "Load Experiment Config", None))
        self.gb_dilatometer_test_config.setTitle(_translate("MainWindow", "Canales de entrada", None))
        self.lb_dilatometer_termperature_input.setText(_translate("MainWindow", "Temperatura", None))
        self.cbx_dilatometer_temperature_input.setItemText(0, _translate("MainWindow", "Agilent Multimeter", None))
        self.cbx_dilatometer_temperature_input.setItemText(1, _translate("MainWindow", "MCC Board", None))
        self.cbx_dilatometer_lvdt_input.setItemText(0, _translate("MainWindow", "Agilent Multimeter", None))
        self.cbx_dilatometer_lvdt_input.setItemText(1, _translate("MainWindow", "MCC Board", None))
        self.lb_dilatometer_lvdt_input.setText(_translate("MainWindow", "Dilatación", None))
        self.lb_device_channel.setText(_translate("MainWindow", "Identificar Canal", None))
        self.lb_ad_device.setText(_translate("MainWindow", "Dispositivo A/D", None))
        self.lb_board_num.setText(_translate("MainWindow", "Board Num", None))
        self.lb_data_per_second.setText(_translate("MainWindow", "Datos por segundo", None))
        self.lb_lvdt_calibration.setText(_translate("MainWindow", "Factor de calibracion", None))
        self.tabmainwidget.setTabText(self.tabmainwidget.indexOf(self.tab_output_config), _translate("MainWindow", "Configuracion de Salida", None))
        self.gb_auxplot_1.setTitle(_translate("MainWindow", "Temperatura ", None))
        self.gb_time.setTitle(_translate("MainWindow", "Tiempo de ensayo", None))
        self.gb_var_1.setTitle(_translate("MainWindow", "Temperatura Cº", None))
        self.gb_var_2.setTitle(_translate("MainWindow", "Vel de temperatura Cº/min", None))
        self.gb_mainplot.setTitle(_translate("MainWindow", "Principal", None))
        self.gb_auxplot_2.setTitle(_translate("MainWindow", "Deformacion", None))
        self.pb_start.setText(_translate("MainWindow", "Comenzar", None))
        self.gb_scale_mainplot_controls.setTitle(_translate("MainWindow", "Scale Main Graph", None))
        self.lb_x_min.setText(_translate("MainWindow", "xMin", None))
        self.lb_x_max.setText(_translate("MainWindow", "xMax", None))
        self.lb_y_min.setText(_translate("MainWindow", "yMin", None))
        self.lb_y_max.setText(_translate("MainWindow", "yMax", None))
        self.pb_start_save_data.setText(_translate("MainWindow", "Iniciar registro de datos", None))
        self.pb_end.setText(_translate("MainWindow", "Finalizar", None))
        self.gb_var_3.setTitle(_translate("MainWindow", "Deformacion mm", None))
        self.tabmainwidget.setTabText(self.tabmainwidget.indexOf(self.tab_plots), _translate("MainWindow", "Graficas", None))

