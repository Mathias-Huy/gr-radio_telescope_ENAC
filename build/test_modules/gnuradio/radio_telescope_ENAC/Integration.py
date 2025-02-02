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
    GNU Radio block for vector integration.
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
                                decim=nb_integration)  # Decimation factor

        # Store the vector length and integration count
        self.vec_len = vec_len
        self.nb_integration = max(1, nb_integration)  # Ensure at least 1 to prevent division by zero
        self.iteration = 0  # Counter for tracking integration steps
        self.set_relative_rate(1.0 / self.nb_integration)  # Adjust relative rate for decimation

        # Preallocate an array to store accumulated results
        self.integrate_result = np.zeros(vec_len, dtype=np.float32)

    def set_integration_number(self, nb_integration):
        """
        Dynamically updates the number of integration iterations.

        Args:
            nb_integration (int): New number of iterations for integration.
        """
        self.nb_integration = max(1, nb_integration)  # Prevent zero division
        self.set_relative_rate(1.0 / self.nb_integration)

    def work(self, input_items, output_items):
        """
        Main method for processing data.

        Args:
            input_items (list): List of input arrays. Shape: (N, vec_len).
            output_items (list): List of output arrays. Shape: (1, vec_len).

        Returns:
            int: Number of output vectors produced (either 1 or 0).
        """
        in0 = input_items[0]  # Input signal array: shape (N, vec_len)
        out = output_items[0]  # Output signal array: shape (1, vec_len)

        # Accumulate input data over multiple iterations
        np.add(self.integrate_result, np.sum(in0, axis=0), out=self.integrate_result)

        # Update iteration count based on input size
        self.iteration += in0.shape[0]

        # Check if we have accumulated enough data to output a result
        if self.iteration >= self.nb_integration:
            # Compute the average by dividing by the number of iterations
            out[:] = self.integrate_result / self.nb_integration

            # Reset the accumulator and iteration counter
            self.integrate_result.fill(0)
            self.iteration = 0

            return 1  # Successfully produced one output vector
        else:
            return 0  # Not enough data yet, no output
