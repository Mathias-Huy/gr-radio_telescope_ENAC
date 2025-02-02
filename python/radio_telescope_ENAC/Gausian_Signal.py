#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2025 Mathias Huyghe.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import numpy as np
from gnuradio import gr

class Gausian_Signal(gr.sync_block):
    """
    This class defines a GNU Radio signal processing block that generates
    a Gaussian-modulated complex sinusoidal signal.
    """

    def __init__(self, carrier_frequency, sigma2, samp_rate, amplitude):
        """
        Initializes the Gaussian signal generator.

        Parameters:
        - carrier_frequency: Frequency of the carrier signal (Hz)
        - sigma2: Standard deviation of the Gaussian envelope
        - samp_rate: Sampling rate (samples per second)
        - amplitude: Amplitude of the signal
        """
        gr.sync_block.__init__(self,
                               name="Gausian_Signal",  # Block name
                               in_sig=[],  # No input signal
                               out_sig=[np.complex64])  # Output signal is complex

        # Store parameters as class attributes
        self.carrier_frequency = carrier_frequency
        self.sigma2 = sigma2
        self.samp_rate = samp_rate
        self.n = 0  # Sample index tracker
        self.amplitude = amplitude

    def set_sigma2(self, sigma2):
        """ Updates the standard deviation of the Gaussian envelope. """
        self.sigma2 = sigma2
        print(f'sigma2: {self.sigma2}')

    def set_amplitude(self, amplitude):
        """ Updates the amplitude of the signal. """
        self.amplitude = amplitude
        print(f'amplitude: {self.amplitude}')

    def set_carrier_frequency(self, carrier_frequency):
        """ Updates the carrier frequency of the signal. """
        self.carrier_frequency = carrier_frequency
        print(f'carrier frequency: {self.carrier_frequency}')

    def work(self, input_items, output_items):
        """
        Generates the Gaussian-modulated carrier signal.

        Parameters:
        - input_items: Not used (since this is a signal source)
        - output_items: Array where the generated signal is stored

        Returns:
        - Number of samples generated
        """
        out = output_items[0]  # Output buffer (complex values)

        n_samples = len(out)  # Number of samples to generate

        # Create a time vector centered at zero
        t = (np.arange(self.n, self.n + n_samples) - (self.n + n_samples / 2)) / self.samp_rate

        # Compute the Gaussian envelope
        gaussian_env = self.amplitude * np.exp(-t ** 2 / (2 * self.sigma2 ** 2))

        # Compute the carrier signal (complex exponential)
        carrier = np.exp(1j * 2 * np.pi * self.carrier_frequency * t)

        # Multiply the Gaussian envelope with the carrier
        out[:] = gaussian_env * carrier

        # Update the sample counter
        self.n += n_samples

        return len(output_items[0])  # Return the number of generated samples
