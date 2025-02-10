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
                               name="Calibration",  # Block name
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

        # Calibration parameters
        self.Tsys = np.zeros(vec_len)  # System temperature (Kelvin)
        self.Gsys = np.ones(vec_len)  # System gain
        self.Tground = 300  # Ground temperature (Kelvin)
        self.Tsky = 10  # Sky temperature (Kelvin)
        self.HCR = np.ones(vec_len)  # Hot/Cold power ratio
        self.hot_spectrum = np.ones(vec_len)  # Spectrum measured in "Hot" mode
        self.cold_spectrum = np.ones(vec_len)  # Spectrum measured in "Cold" mode
        self.filtered_out = np.zeros(vec_len)  # Filtered data
        self.freq = np.fft.fftfreq(vec_len, 1 / self.sample_rate)  # Frequency axis
        self.freq += 1420e6  # Shift frequencies by 1.42 GHz

    def set_calibration_type(self, calibration_type):
        """ Updates the calibration type. """
        self.calibration_type = calibration_type
        print(self.calibration_type)

    def work(self, input_items, output_items):
        """
        Processes input data based on the selected calibration type.

        Args:
            input_items (list): List of arrays containing input signals.
            output_items (list): List of arrays to store output signals.

        Returns:
            int: Number of processed elements.
        """

        in0 = input_items[0]  # Input signal
        out0 = output_items[0]  # First output: processed data
        out1 = output_items[1]  # Second output: Tsys (System temperature)
        out2 = output_items[2]  # Third output: Gsys (System gain in dB)

        KB = 1.380649e-23  # Boltzmann constant
        C = 3e9  # Speed of light (m/s)
        delta_f = self.sample_rate / self.vec_len  # Frequency resolution

        # Copy input data for processing
        self.a = in0[0, :].copy()
        self.filtered_out0 = self.a[:]

        # Smooth spikes in the input data (optional)
        self.spike_smoothing()

        # Process data based on calibration type
        if self.calibration_type == "Hot":
            # Store the current spectrum as the "Hot" spectrum
            self.hot_spectrum[:] = self.filtered_out0

            # Compute Hot/Cold Ratio (HCR)
            self.HCR = self.hot_spectrum / self.cold_spectrum
            self.HCR[self.HCR == 1] = 2  # Prevent division by zero

            # Compute system temperature (Tsys) and gain (Gsys)
            self.Tsys = (self.Tground - self.HCR * self.Tsky) / (self.HCR - 1)
            self.Gsys = self.cold_spectrum / (self.Tsky + self.Tsys)
            self.Gsys[self.Gsys <= 0] = 1  # Avoid invalid values

        elif self.calibration_type == "Cold":
            # Store the current spectrum as the "Cold" spectrum
            self.cold_spectrum[:] = self.filtered_out0

            # Compute Hot/Cold Ratio (HCR)
            self.HCR = self.hot_spectrum / self.cold_spectrum
            self.HCR[self.HCR == 1] = 2  # Prevent division by zero

            # Compute system temperature (Tsys) and gain (Gsys)
            self.Tsys = (self.Tground - self.HCR * self.Tsky) / (self.HCR - 1)
            self.Gsys = self.cold_spectrum / (self.Tsky + self.Tsys)
            self.Gsys[self.Gsys <= 0] = 1  # Avoid invalid values

        elif self.calibration_type == "Calibrated":
            # Apply calibration to the input signal
            self.filtered_out0 = (self.filtered_out0 / self.Gsys) - self.Gsys * KB * delta_f * self.Tsys

        elif self.calibration_type == "Non_calibrated":
            # Non-calibrated mode: pass data through unchanged
            self.filtered_out0 = self.filtered_out0

        # Store results in output buffers
        out0[:] = self.filtered_out0
        out1[:] = self.Tsys  # System temperature
        out2[:] = 10 * np.log10(self.Gsys)  # System gain in dB
        return len(output_items[0])

    def spike_smoothing(self):
        """
        Smooths spikes in the input data.
        Detects extreme values and replaces them with the median of neighboring points.
        """
        #indice_max = np.argmax(self.a)  # Index of the maximum value

        # Define a threshold based on local mean intensity
        threshold = 1.2*np.mean(self.a[2541:2786])
        abovethresh_index = np.where(self.a > threshold)[0]
        #print(abovethresh_index)
        # Indices of spikes

        # Copy input data for processing
        self.filtered_out0 = self.a[:]
        #print(self.filtered_out0.shape)


        # Replace spikes with median values from neighboring points
        for index in abovethresh_index:
            lowerbound = max(1, index - 10)  # Lower limit
            upperbound = min(index + 10, self.vec_len)  # Upper limit

            # Replace the spike with the median of the surrounding values
            self.filtered_out0[index] = np.median(self.a[lowerbound:upperbound])

            # Debugging output

