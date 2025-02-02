#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Mathias Huyghe.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import numpy as np
from gnuradio import gr


class PFB(gr.sync_block):
    """
    Polyphase Filter Bank (PFB) implementation.

    Args:
        vec_len (int): Length of the input vector.
        window (str): Window type ('hanning', 'hamming', 'blackman_harris').
        num_taps (int): Number of taps in the filter.
    """

    def __init__(self, vec_len, window, num_taps):
        """
        Initialize the Polyphase Filter Bank block.

        Args:
            vec_len (int): Length of the input vector.
            window (str): Window type ('hanning', 'hamming', 'blackman_harris').
            num_taps (int): Number of taps in the filter.
        """
        # Ensure valid input parameters
        assert num_taps > 0, "Number of taps must be positive."
        assert vec_len % num_taps == 0, "vec_len must be divisible by num_taps."

        self.vec_len = vec_len
        self.num_taps = num_taps
        self.band_taps = vec_len
        self.memory = [np.zeros(self.vec_len) for _ in range(self.num_taps)]

        # Define block I/O: One input and one output of complex64 type
        gr.sync_block.__init__(
            self,
            name="PFB",
            in_sig=[(np.complex64, vec_len)],  # Input signal type (complex64, vec_len)
            out_sig=[(np.complex64, vec_len)],  # Output signal type (complex64, vec_len)
        )

        # Generate filter coefficients based on window type
        x = np.linspace(-num_taps / 2.0, num_taps / 2.0, num_taps * vec_len, endpoint=False)
        y = np.sinc(x)

        if window == "hanning":
            self.filter = y * np.hanning(len(x))
        elif window == "hamming":
            self.filter = y * np.hamming(len(x))
        elif window == "blackman_harris":
            self.filter = y * self.blackman_harris(len(x))
        else:
            raise ValueError(f"Unsupported window type: {window}")

    def switch_memory(self, data):
        """
        Update memory to store the new data in the first position.

        Args:
            data (np.ndarray): New input data to be stored in memory.
        """
        self.memory.pop()  # Remove the last memory item
        self.memory.insert(0, data)  # Insert new data at the beginning

    def set_window_type(self, window):
        """
        Change the window type and update filter coefficients.

        Args:
            window (str): Window type ('hanning', 'hamming', 'blackman_harris').
        """
        x = np.arange(-np.pi*4/2.0, np.pi*4/2.0, np.pi/self.vec_len)
        y = np.sinc(x/np.pi)

        # Set filter coefficients based on selected window
        if window == "hanning":
            self.filter = y * np.hanning(len(x))
        elif window == "hamming":
            self.filter = y * np.hamming(len(x))
        elif window == "blackman_harris":
            self.filter = y * self.blackman_harris(len(x))
        else:
            raise ValueError(f"Unsupported window type: {window}")

    def work(self, input_items, output_items):
        """
        Process input samples using the polyphase filter bank and produce filtered output.

        Args:
            input_items: List of input arrays (input buffer).
            output_items: List of output arrays (output buffer).

        Returns:
            int: Number of output samples (filtered).
        """
        # Retrieve input signal
        in0 = input_items[0]
        out0 = output_items[0]
        num_channels = in0.shape[0]  # Number of channels in the input signal
        self.filtered_signal = np.zeros((num_channels, self.vec_len), dtype=np.complex64)

        # Apply polyphase filtering to each input channel
        for channel in range(num_channels):
            segment = in0[channel, :]
            self.switch_memory(segment)  # Update memory with the current segment

            # Apply filter to the current segment for each phase of the polyphase filter bank
            for phase in range(self.num_taps):
                start = phase * self.band_taps
                end = (phase + 1) * self.band_taps

                # Accumulate the filtered result for the current channel
                self.filtered_signal[channel] += self.memory[phase] * self.filter[start:end]

        # Assign the filtered signal as the output
        out0[:] = self.filtered_signal

        return len(out0)  # Return the number of output samples

    @staticmethod
    def blackman_harris(N):
        """
        Generate a Blackman-Harris window of size N.

        Args:
            N (int): Length of the window.

        Returns:
            np.ndarray: Blackman-Harris window coefficients.
        """
        n = np.arange(N)
        a0 = 0.35875
        a1 = 0.48829
        a2 = 0.14128
        a3 = 0.01168
        # Calculate the Blackman-Harris window coefficients
        return (
                a0
                - a1 * np.cos(2 * np.pi * n / (N - 1))
                + a2 * np.cos(4 * np.pi * n / (N - 1))
                - a3 * np.cos(6 * np.pi * n / (N - 1))
        )
