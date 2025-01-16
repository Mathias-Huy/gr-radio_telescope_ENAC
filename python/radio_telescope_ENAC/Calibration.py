#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Mathias Huyghe.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy as np
from gnuradio import gr


class Calibration(gr.sync_block):
    """
    GNURadio block for signal calibration.
    Supports multiple calibration modes: 'Hot', 'Cold', 'Calibrated', and 'Non_calibrated'.
    """

    def __init__(self, calibration_type, vec_len, sample_rate):
        """
        Initializes the block with calibration parameters.

        Args:
            calibration_type (str): Type of calibration ('Hot', 'Cold', 'Calibrated', 'Non_calibrated').
            vec_len (int): Length of input/output vectors.
            sample_rate (float): Sampling rate of the signal.
        """
        gr.sync_block.__init__(self,
                               name="Calibration",
                               in_sig=[(np.float32, vec_len)],  # Input: vector of float32
                               out_sig=[(np.float32, vec_len),  # First output port
                                (np.float32, vec_len),  # Second output port
                                (np.float32, vec_len)])  # Three outputs: vectors of float32

        # Validate that the calibration type is supported
        assert calibration_type in ['Hot', 'Cold', 'Calibrated', 'Non_calibrated'], \
            f"Invalid calibration type: {calibration_type}"

        # Initialize class attributes
        self.calibration_type = calibration_type
        self.vec_len = vec_len
        self.sample_rate = sample_rate


        # Calibration variables
        self.Tsys = np.zeros(vec_len)  # System temperature (K)
        self.Gsys = np.ones(vec_len)  # System gain
        self.Tground = 300  # Ground temperature (K)
        self.Tsky = 10  # Sky temperature (K)
        self.HCR = np.ones(vec_len)  # Hot/Cold power ratio
        self.hot_spectrum = np.ones(vec_len)  # Spectrum measured in "Hot" mode
        self.cold_spectrum = np.ones(vec_len)  # Spectrum measured in "Cold" mode
        self.filtered_out = np.zeros(vec_len)  # Filtered data
        self.freq = np.fft.fftfreq(vec_len, 1/self.sample_rate)
        self.freq += 1420e9

    def set_calibration_type(self, calibration_type):
        self.calibration_type = calibration_type
        print(self.calibration_type)




    def work(self, input_items, output_items):
        """
        Main method for processing data based on the calibration type.

        Args:
            input_items (list): List of arrays containing input signals.
            output_items (list): List of arrays to store output signals.

        Returns:
            int: Number of processed elements.
        """

        in0 = input_items[0]  # Input signal
        out0 = output_items[0]  # First output: processed data
        out1 = output_items[1]  # Second output: Tsys
        out2 = output_items[2]  # Third output: Gsys in dB

        KB = 1.380649e-23
        C = 3e9
        delta_f = self.sample_rate / self.vec_len


        # Copy input data for processing
        self.a = in0[0, :].copy()
        self.filtered_out0 = self.a[:]

        # Smooth spikes in the input data
        # self.spike_smoothing()

        # Process data based on calibration type
        if self.calibration_type == "Hot":
            self.hot_spectrum[:] = self.filtered_out0
            # Compute calibration parameters
            self.HCR = self.hot_spectrum / self.cold_spectrum
            self.HCR[self.HCR == 1] = 2  # Prevent division by zero
            self.Tsys = (self.Tground - self.HCR * self.Tsky) / (self.HCR - 1)
            self.Gsys = self.cold_spectrum / (self.Tsky + self.Tsys)
            self.Gsys[self.Gsys <= 0] = 1  # Avoid invalid values



        elif self.calibration_type == "Cold":
            self.cold_spectrum[:] = self.filtered_out0
            # Compute calibration parameters (similar to "Hot")
            self.HCR = self.hot_spectrum / self.cold_spectrum
            self.HCR[self.HCR == 1] = 2
            self.Tsys = (self.Tground - self.HCR * self.Tsky) / (self.HCR - 1)
            self.Gsys = self.cold_spectrum / (self.Tsky + self.Tsys)
            self.Gsys[self.Gsys <= 0] = 1

        elif self.calibration_type == "Calibrated":
            self.filtered_out0 = (self.filtered_out0 * C**2)/(2 * KB * self.freq**2) # Rayleigh-Jeans Formula


        elif self.calibration_type == "Non_calibrated":
            # Non-calibrated mode: pass data through unchanged
            self.filtered_out0 = (self.filtered_out0 / (KB * delta_f))

        out0[:] = self.filtered_out0
        out1 = self.Tsys  # System temperature
        out2 = 10 * np.log10(self.Gsys)  # System gain in dB
        return len(output_items[0])

    def spike_smoothing(self):
        """
        Smooth spikes in the input data.
        Replace values exceeding a threshold with the median of neighboring points.
        """
        indice_max = np.argmax(self.a)
        print(indice_max)
        # Detect spikes: threshold based on the mean of data within a specific range
        threshold = 1.2 * np.mean(self.a[indice_max-100:indice_max+100])
        abovethresh_index = np.where(self.a > threshold)[0]


        # Copy input data for processing
        self.filtered_out0 = self.a[:]
        print(f'Taile de filtered out 0 {self.filtered_out0.shape}')

        # Replace spikes with the median of neighboring points
        for index in abovethresh_index:
            lowerbound = max(1, index - 10)  # Lower limit
            upperbound = min(index + 10, self.vec_len)  # Upper limit

            # Replace spikes with median of +/- k_spike surrounding points. For data near edges, the range is reduced to fit array parameters.
            self.filtered_out0[abovethresh_index[index]] = np.median(self.a[lowerbound:upperbound])
            print(f'Indice: {abovethresh_index[index]}')
            print(f'Borne inferieur: {lowerbound}')
            print(f'Borne Super: {upperbound}')
