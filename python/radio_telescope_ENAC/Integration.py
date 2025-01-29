#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2025 Mathias Huyghe.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import numpy as np
from gnuradio import gr


class Integration(gr.decim_block):
    """
    GNURadio block for vector integration.
    Accumulates input data over a specified number of iterations
    and outputs the averaged result.
    """

    def __init__(self, vec_len, nb_integration):
        """
        Initializes the Integration block with vector size and integration parameters.

        Args:
            vec_len (int): Length of input and output vectors.
            nb_integration (int): Number of iterations for integration.
        """
        gr.decim_block.__init__(self,
                                name="Integration",  # Name of the block
                                in_sig=[(np.float32, int(vec_len))],  # Input: vector of float32
                                out_sig=[(np.float32, int(vec_len))],  # Output: vector of float32
                                decim=nb_integration)  # Decimation factor based on the number of iterations

        # Initialize class attributes
        self.vec_len = vec_len  # Length of the input/output vectors
        self.nb_integration = nb_integration  # Number of iterations to integrate
        self.iteration = 0  # Counter for tracking the current integration iteration
        self.set_relative_rate(1.0 / nb_integration)  # Adjust the relative rate based on decimation
        self.integrate_result = np.zeros(vec_len)  # Array to store accumulated results

    def set_integration_number(self, nb_integration):
        """
        Dynamically updates the number of integration iterations.

        Args:
            nb_integration (int): New number of iterations for integration.
        """
        self.nb_integration = nb_integration
        self.set_relative_rate(1.0 / nb_integration)  # Update the relative rate to match the new decimation

    def work(self, input_items, output_items):
        """
        Main method for processing data.

        Args:
            input_items (list): List of input arrays. Expected shape: (nb_integration, vec_len).
            output_items (list): List of output arrays. Expected shape: (1, vec_len).

        Returns:
            int: Number of output vectors produced (1 in this case).
        """
        in0 = input_items[0]  # Shape: (nb_integration, vec_len)
        out = output_items[0]  # Shape: (1, vec_len)

        # Accumulate input data
        self.integrate_result += np.sum(in0, axis=0)  # Sum across rows (axis=0)

        # Increment the iteration counter by the number of rows in input
        self.iteration += in0.shape[0]

        if self.iteration >= self.nb_integration:
            # Compute the averaged result
            out[:] = self.integrate_result / self.nb_integration  # Normalize the accumulated result

            # Reset the accumulator and iteration counter
            self.integrate_result.fill(0)
            self.iteration = 0
        else:
            # If not enough data yet, output zeros
            out[:] = np.zeros(self.vec_len)

        # Return 1 because we're producing one output vector
        return 1
