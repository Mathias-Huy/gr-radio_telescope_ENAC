#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2025 Mathias Huyghe.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import numpy as np
from gnuradio import gr
from scipy.optimize import curve_fit

class Gaussian_fit(gr.sync_block):
    """
    This class defines a GNU Radio signal processing block that fits a Gaussian
    function to an input spectrum and extracts key parameters (center x0 and variance sigma^2).
    """

    def __init__(self, vec_len):
        """
        Initializes the Gaussian fitting block.

        Parameters:
        - vec_len: Length of the input spectrum vector.
        """
        gr.sync_block.__init__(self,
                               name="Gaussian_fit",  # Block name
                               in_sig=[(np.float32, vec_len)],  # Input: vector of floats
                               out_sig=[np.float32, np.float32])  # Outputs: x0 (center) and sigma^2 (variance)

    def gaussian(self, x, amplitude, x0, sigma):
        """
        Defines a Gaussian function.

        Parameters:
        - x: Input values (array)
        - amplitude: Peak amplitude of the Gaussian
        - x0: Center of the Gaussian
        - sigma: Standard deviation of the Gaussian

        Returns:
        - Computed Gaussian function values for given x
        """
        return amplitude * np.exp(-((x - x0) ** 2) / (2 * sigma ** 2))

    def work(self, input_items, output_items):
        """
        Processes the input spectrum, fits a Gaussian curve, and extracts parameters.

        Parameters:
        - input_items: List containing the input spectrum (first element)
        - output_items: List containing output arrays for x0 and sigma^2

        Returns:
        - None (results are written to output arrays)
        """
        # Input: spectrum of 4096 points
        input_data = input_items[0][0]  # Take the first input vector
        x0_output = output_items[0]  # Output for x0 (Gaussian center)
        sigma2_output = output_items[1]  # Output for sigma^2 (variance)

        # Generate indices corresponding to the data points
        x_data = np.arange(len(input_data))  # [0, 1, ..., 4095]
        y_data = input_data  # Spectral data

        try:
            # Perform Gaussian fitting with initial parameter estimates
            initial_guess = [np.max(y_data), len(x_data) / 2, 100.0]  # [Amplitude, x0, sigma]
            params, _ = curve_fit(self.gaussian, x_data, y_data, p0=initial_guess)

            # Extract fitted parameters
            _, x0_fit, sigma_fit = params

            # Compute sigma^2 (variance)
            sigma2_fit = sigma_fit ** 2

            # Write results to output arrays
            x0_output[0] = x0_fit  # x0 (Gaussian center)
            sigma2_output[0] = sigma2_fit  # sigma^2 (Gaussian variance)

            # Print fitted parameters for debugging
            print(f'X0 = {x0_output[0]}')
            print(f'sigma2 = {sigma2_output[0]}')

        except Exception as e:
            # Handle fitting errors and assign default values
            print(f"Error in Gaussian fitting: {e}")
            x0_output[0] = 0  # Default value for x0
            sigma2_output[0] = 0  # Default value for sigma^2
