#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Spectromètre
# GNU Radio version: 3.10.11.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import blocks
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import radio_telescope_ENAC
import numpy as np
import osmosdr
import time
import sip
import threading



class test(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Spectromètre", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Spectromètre")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "test")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.lenght_vec = lenght_vec = 4096
        self.sinc_sample_locations = sinc_sample_locations = np.arange(-np.pi*4/2.0, np.pi*4/2.0, np.pi/lenght_vec)
        self.sinc = sinc = np.sinc(sinc_sample_locations/np.pi)
        self.vec_length = vec_length = 4096
        self.variable_qtgui_chooser_0 = variable_qtgui_chooser_0 = 0
        self.samp_rate = samp_rate = 2.5e6
        self.qtgui_chooser_1 = qtgui_chooser_1 = 'hamming'
        self.qt_chooser_0 = qt_chooser_0 = "Hot"
        self.nb_integration = nb_integration = 25
        self.freq = freq = 1420e6
        self.custom_window = custom_window = sinc*np.hamming(4*lenght_vec)
        self.Delay = Delay = 4096
        self.CN0_dB = CN0_dB = 100
        self.Amplitude = Amplitude = 0.001

        ##################################################
        # Blocks
        ##################################################

        self.qtgui_tab_widget_1 = Qt.QTabWidget()
        self.qtgui_tab_widget_1_widget_0 = Qt.QWidget()
        self.qtgui_tab_widget_1_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.qtgui_tab_widget_1_widget_0)
        self.qtgui_tab_widget_1_grid_layout_0 = Qt.QGridLayout()
        self.qtgui_tab_widget_1_layout_0.addLayout(self.qtgui_tab_widget_1_grid_layout_0)
        self.qtgui_tab_widget_1.addTab(self.qtgui_tab_widget_1_widget_0, 'Spectre')
        self.qtgui_tab_widget_1_widget_1 = Qt.QWidget()
        self.qtgui_tab_widget_1_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.qtgui_tab_widget_1_widget_1)
        self.qtgui_tab_widget_1_grid_layout_1 = Qt.QGridLayout()
        self.qtgui_tab_widget_1_layout_1.addLayout(self.qtgui_tab_widget_1_grid_layout_1)
        self.qtgui_tab_widget_1.addTab(self.qtgui_tab_widget_1_widget_1, 'Etat Système')
        self.top_layout.addWidget(self.qtgui_tab_widget_1)
        # Create the options list
        self._qtgui_chooser_1_options = ['hanning', 'hamming', 'blackman_harris']
        # Create the labels list
        self._qtgui_chooser_1_labels = ['Hanning', 'Hamming', 'Blackman Harris']
        # Create the combo box
        self._qtgui_chooser_1_tool_bar = Qt.QToolBar(self)
        self._qtgui_chooser_1_tool_bar.addWidget(Qt.QLabel("Window" + ": "))
        self._qtgui_chooser_1_combo_box = Qt.QComboBox()
        self._qtgui_chooser_1_tool_bar.addWidget(self._qtgui_chooser_1_combo_box)
        for _label in self._qtgui_chooser_1_labels: self._qtgui_chooser_1_combo_box.addItem(_label)
        self._qtgui_chooser_1_callback = lambda i: Qt.QMetaObject.invokeMethod(self._qtgui_chooser_1_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._qtgui_chooser_1_options.index(i)))
        self._qtgui_chooser_1_callback(self.qtgui_chooser_1)
        self._qtgui_chooser_1_combo_box.currentIndexChanged.connect(
            lambda i: self.set_qtgui_chooser_1(self._qtgui_chooser_1_options[i]))
        # Create the radio buttons
        self.qtgui_tab_widget_1_layout_0.addWidget(self._qtgui_chooser_1_tool_bar)
        # Create the options list
        self._qt_chooser_0_options = ['Hot', 'Cold', 'Caibrated', 'Non_calibrated']
        # Create the labels list
        self._qt_chooser_0_labels = ['Hot', 'Cold', 'Calibrated', 'Non Calibrated']
        # Create the combo box
        # Create the radio buttons
        self._qt_chooser_0_group_box = Qt.QGroupBox("Calibration Type " + ": ")
        self._qt_chooser_0_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._qt_chooser_0_button_group = variable_chooser_button_group()
        self._qt_chooser_0_group_box.setLayout(self._qt_chooser_0_box)
        for i, _label in enumerate(self._qt_chooser_0_labels):
            radio_button = Qt.QRadioButton(_label)
            self._qt_chooser_0_box.addWidget(radio_button)
            self._qt_chooser_0_button_group.addButton(radio_button, i)
        self._qt_chooser_0_callback = lambda i: Qt.QMetaObject.invokeMethod(self._qt_chooser_0_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._qt_chooser_0_options.index(i)))
        self._qt_chooser_0_callback(self.qt_chooser_0)
        self._qt_chooser_0_button_group.buttonClicked[int].connect(
            lambda i: self.set_qt_chooser_0(self._qt_chooser_0_options[i]))
        self.qtgui_tab_widget_1_layout_0.addWidget(self._qt_chooser_0_group_box)
        self._nb_integration_range = qtgui.Range(1, 50, 1, 25, 200)
        self._nb_integration_win = qtgui.RangeWidget(self._nb_integration_range, self.set_nb_integration, "'nb_integration'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.qtgui_tab_widget_1_layout_0.addWidget(self._nb_integration_win)
        # Create the options list
        self._variable_qtgui_chooser_0_options = [0, 1, 2]
        # Create the labels list
        self._variable_qtgui_chooser_0_labels = ['0', '1', '2']
        # Create the combo box
        self._variable_qtgui_chooser_0_tool_bar = Qt.QToolBar(self)
        self._variable_qtgui_chooser_0_tool_bar.addWidget(Qt.QLabel("'variable_qtgui_chooser_0'" + ": "))
        self._variable_qtgui_chooser_0_combo_box = Qt.QComboBox()
        self._variable_qtgui_chooser_0_tool_bar.addWidget(self._variable_qtgui_chooser_0_combo_box)
        for _label in self._variable_qtgui_chooser_0_labels: self._variable_qtgui_chooser_0_combo_box.addItem(_label)
        self._variable_qtgui_chooser_0_callback = lambda i: Qt.QMetaObject.invokeMethod(self._variable_qtgui_chooser_0_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._variable_qtgui_chooser_0_options.index(i)))
        self._variable_qtgui_chooser_0_callback(self.variable_qtgui_chooser_0)
        self._variable_qtgui_chooser_0_combo_box.currentIndexChanged.connect(
            lambda i: self.set_variable_qtgui_chooser_0(self._variable_qtgui_chooser_0_options[i]))
        # Create the radio buttons
        self.qtgui_tab_widget_1_layout_0.addWidget(self._variable_qtgui_chooser_0_tool_bar)
        self.rtlsdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + ""
        )
        self.rtlsdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(freq, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(10, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna('', 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
        self.radio_telescope_ENAC_PFB_0 = radio_telescope_ENAC.PFB(4096,qtgui_chooser_1,4)
        self.radio_telescope_ENAC_Integration_0_0 = radio_telescope_ENAC.Integration(4096,nb_integration)
        self.radio_telescope_ENAC_Calibration_0 = radio_telescope_ENAC.Calibration(qt_chooser_0, 4096, int(samp_rate))
        self.qtgui_vector_sink_f_0_1_3_0 = qtgui.vector_sink_f(
            4096,
            0,
            1,
            "x-Axis",
            "y-Axis",
            "Gsys",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0_1_3_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0_1_3_0.set_y_axis((-140), 10)
        self.qtgui_vector_sink_f_0_1_3_0.enable_autoscale(False)
        self.qtgui_vector_sink_f_0_1_3_0.enable_grid(False)
        self.qtgui_vector_sink_f_0_1_3_0.set_x_axis_units("")
        self.qtgui_vector_sink_f_0_1_3_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0_1_3_0.set_ref_level(0)


        labels = ['PFB ', 'FFT', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["green", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0_1_3_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_1_3_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_1_3_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_1_3_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_1_3_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_1_3_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_1_3_0.qwidget(), Qt.QWidget)
        self.qtgui_tab_widget_1_layout_1.addWidget(self._qtgui_vector_sink_f_0_1_3_0_win)
        self.qtgui_vector_sink_f_0_1_3 = qtgui.vector_sink_f(
            4096,
            0,
            1,
            "x-Axis",
            "y-Axis",
            "Tsys",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0_1_3.set_update_time(0.10)
        self.qtgui_vector_sink_f_0_1_3.set_y_axis((-140), 10)
        self.qtgui_vector_sink_f_0_1_3.enable_autoscale(False)
        self.qtgui_vector_sink_f_0_1_3.enable_grid(False)
        self.qtgui_vector_sink_f_0_1_3.set_x_axis_units("")
        self.qtgui_vector_sink_f_0_1_3.set_y_axis_units("")
        self.qtgui_vector_sink_f_0_1_3.set_ref_level(0)


        labels = ['PFB ', 'FFT', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["green", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0_1_3.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_1_3.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_1_3.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_1_3.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_1_3.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_1_3_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_1_3.qwidget(), Qt.QWidget)
        self.qtgui_tab_widget_1_layout_1.addWidget(self._qtgui_vector_sink_f_0_1_3_win)
        self.qtgui_vector_sink_f_0_0_1 = qtgui.vector_sink_f(
            vec_length,
            ((freq - samp_rate/2)/1e6),
            ((samp_rate/vec_length)/1e6),
            "Frequency (MHz)",
            "Signal",
            "Spectrum",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0_0_1.set_update_time(0.10)
        self.qtgui_vector_sink_f_0_0_1.set_y_axis((-140), 10)
        self.qtgui_vector_sink_f_0_0_1.enable_autoscale(True)
        self.qtgui_vector_sink_f_0_0_1.enable_grid(True)
        self.qtgui_vector_sink_f_0_0_1.set_x_axis_units("MHz")
        self.qtgui_vector_sink_f_0_0_1.set_y_axis_units("")
        self.qtgui_vector_sink_f_0_0_1.set_ref_level(0)


        labels = ['Spectrum', '', '', '', '',
            '', '', '', '', '']
        widths = [2, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_0_1.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_0_1.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_0_1.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_0_1_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_0_1.qwidget(), Qt.QWidget)
        self.qtgui_tab_widget_1_layout_0.addWidget(self._qtgui_vector_sink_f_0_0_1_win)
        self.fft_vxx_0 = fft.fft_vcc(4096, True, window.rectangular(4096), True, 1)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, 4096)
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(10, 4096, 0)
        self.blocks_multiply_const_xx_0 = blocks.multiply_const_cc(1/lenght_vec, lenght_vec)
        self.blocks_integrate_xx_0_0_0 = blocks.integrate_ff(16, vec_length)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(4096)
        self._CN0_dB_range = qtgui.Range(-100, 100, 1, 100, 200)
        self._CN0_dB_win = qtgui.RangeWidget(self._CN0_dB_range, self.set_CN0_dB, "'CN0_dB'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.qtgui_tab_widget_1_layout_0.addWidget(self._CN0_dB_win)
        self._Amplitude_range = qtgui.Range(0.001, 1, 0.001, 0.001, 200)
        self._Amplitude_win = qtgui.RangeWidget(self._Amplitude_range, self.set_Amplitude, "'Amplitude'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._Amplitude_win)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_integrate_xx_0_0_0, 0))
        self.connect((self.blocks_integrate_xx_0_0_0, 0), (self.radio_telescope_ENAC_Integration_0_0, 0))
        self.connect((self.blocks_multiply_const_xx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.qtgui_vector_sink_f_0_0_1, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.radio_telescope_ENAC_PFB_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_multiply_const_xx_0, 0))
        self.connect((self.radio_telescope_ENAC_Calibration_0, 0), (self.blocks_nlog10_ff_0, 0))
        self.connect((self.radio_telescope_ENAC_Calibration_0, 1), (self.qtgui_vector_sink_f_0_1_3, 0))
        self.connect((self.radio_telescope_ENAC_Calibration_0, 2), (self.qtgui_vector_sink_f_0_1_3_0, 0))
        self.connect((self.radio_telescope_ENAC_Integration_0_0, 0), (self.radio_telescope_ENAC_Calibration_0, 0))
        self.connect((self.radio_telescope_ENAC_PFB_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.blocks_stream_to_vector_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "test")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_lenght_vec(self):
        return self.lenght_vec

    def set_lenght_vec(self, lenght_vec):
        self.lenght_vec = lenght_vec
        self.set_custom_window(self.sinc*np.hamming(4*self.lenght_vec))
        self.set_sinc_sample_locations(np.arange(-np.pi*4/2.0, np.pi*4/2.0, np.pi/self.lenght_vec))
        self.blocks_multiply_const_xx_0.set_k(1/self.lenght_vec)

    def get_sinc_sample_locations(self):
        return self.sinc_sample_locations

    def set_sinc_sample_locations(self, sinc_sample_locations):
        self.sinc_sample_locations = sinc_sample_locations
        self.set_sinc(np.sinc(self.sinc_sample_locations/np.pi))

    def get_sinc(self):
        return self.sinc

    def set_sinc(self, sinc):
        self.sinc = sinc
        self.set_custom_window(self.sinc*np.hamming(4*self.lenght_vec))
        self.set_sinc(np.sinc(self.sinc_sample_locations/np.pi))

    def get_vec_length(self):
        return self.vec_length

    def set_vec_length(self, vec_length):
        self.vec_length = vec_length
        self.qtgui_vector_sink_f_0_0_1.set_x_axis(((self.freq - self.samp_rate/2)/1e6), ((self.samp_rate/self.vec_length)/1e6))

    def get_variable_qtgui_chooser_0(self):
        return self.variable_qtgui_chooser_0

    def set_variable_qtgui_chooser_0(self, variable_qtgui_chooser_0):
        self.variable_qtgui_chooser_0 = variable_qtgui_chooser_0
        self._variable_qtgui_chooser_0_callback(self.variable_qtgui_chooser_0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_vector_sink_f_0_0_1.set_x_axis(((self.freq - self.samp_rate/2)/1e6), ((self.samp_rate/self.vec_length)/1e6))
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)

    def get_qtgui_chooser_1(self):
        return self.qtgui_chooser_1

    def set_qtgui_chooser_1(self, qtgui_chooser_1):
        self.qtgui_chooser_1 = qtgui_chooser_1
        self._qtgui_chooser_1_callback(self.qtgui_chooser_1)
        self.radio_telescope_ENAC_PFB_0.set_window_type(self.qtgui_chooser_1)

    def get_qt_chooser_0(self):
        return self.qt_chooser_0

    def set_qt_chooser_0(self, qt_chooser_0):
        self.qt_chooser_0 = qt_chooser_0
        self._qt_chooser_0_callback(self.qt_chooser_0)
        self.radio_telescope_ENAC_Calibration_0.set_calibration_type(self.qt_chooser_0)

    def get_nb_integration(self):
        return self.nb_integration

    def set_nb_integration(self, nb_integration):
        self.nb_integration = nb_integration
        self.radio_telescope_ENAC_Integration_0_0.set_integration_number(self.nb_integration)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.qtgui_vector_sink_f_0_0_1.set_x_axis(((self.freq - self.samp_rate/2)/1e6), ((self.samp_rate/self.vec_length)/1e6))
        self.rtlsdr_source_0.set_center_freq(self.freq, 0)

    def get_custom_window(self):
        return self.custom_window

    def set_custom_window(self, custom_window):
        self.custom_window = custom_window

    def get_Delay(self):
        return self.Delay

    def set_Delay(self, Delay):
        self.Delay = Delay

    def get_CN0_dB(self):
        return self.CN0_dB

    def set_CN0_dB(self, CN0_dB):
        self.CN0_dB = CN0_dB

    def get_Amplitude(self):
        return self.Amplitude

    def set_Amplitude(self, Amplitude):
        self.Amplitude = Amplitude




def main(top_block_cls=test, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()
    tb.flowgraph_started.set()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
