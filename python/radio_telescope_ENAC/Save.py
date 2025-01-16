#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2025 Mathias Huyghe.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import pickle
from datetime import datetime
import numpy as np
from gnuradio import gr


class Save(gr.sync_block):
    """
    A GNU Radio block that saves data to a binary file,
    with the option to start/stop recording based on input toggle.
    """

    def __init__(self, vec_len, azimuth, elevation, toggle, samp_rate):
        # Initialize the block with necessary parameters
        gr.sync_block.__init__(self,
                               name="Save",  # Name of the block
                               in_sig=[(np.float32, vec_len)],  # Input signal type (vector of float32)
                               out_sig=None)  # No output signal
        self.vec_len = vec_len
        self.azimuth = azimuth
        self.elevation = elevation
        self.toggle = toggle  # Toggle to control start/stop of recording
        self.samp_rate = samp_rate  # Sampling rate
        self.filename = None  # Filename for saving data
        self.file = None  # File object for writing data
        self.buffer = []  # Temporary buffer to store incoming data
        # Calculate the frequency range of the FFT based on input vector length and sample rate
        freq = 1420e6 + np.fft.fftfreq(vec_len, 1 / self.samp_rate)
        # Indices corresponding to frequencies in a specific range
        self.indx = np.where((freq > 1415e6) & (freq < 1425e6))[0]

    def start_stop_recording(self, toggle):
        """
        Start or stop recording based on the 'toggle' argument.
        When recording starts, a new file is created with a timestamp and azimuth/elevation.
        When recording stops, the file is closed.
        """
        self.toggle = toggle
        if toggle:  # If toggle is True, start recording
            # Generate a filename based on the current date and time, azimuth, elevation, and sample rate
            current_time = datetime.now()
            date_str = current_time.strftime("%Y-%m-%d_%H-%M-%S")
            azimuth_str = f"{self.azimuth:.2f}"
            elevation_str = f"{self.elevation:.2f}"
            self.filename = f"data_{date_str}_az{azimuth_str}_el{elevation_str}_rate{self.samp_rate}.bin"
            # Open the file for binary writing
            self.file = open(self.filename, "wb")
        else:  # If toggle is False, stop recording and close the file
            if self.file and not self.file.closed:
                self.file.close()

    def set_azimuth_elevation(self, azimuth, elevation):
        """
        Change the azimuth and elevation, stop and start recording with the new values.
        """
        self.start_stop_recording(False)  # Stop recording first
        self.azimuth = azimuth
        self.elevation = elevation
        self.start_stop_recording(True)  # Restart recording with the new azimuth/elevation

    def work(self, input_items, output_items):
        """
        The main work function that processes the input data and saves it to the file.
        The data corresponding to the specified frequency indices is written to the buffer and then saved to file.
        """
        in0 = input_items[0]  # Get the input signal
        print(in0.shape)

        # Add the selected data (based on frequency indices) to the buffer

        self.buffer.extend(in0[:,self.indx])

        # Save the data in the buffer to the file and then clear the buffer
        if self.file and not self.file.closed:
            pickle.dump(self.buffer, self.file)  # Save the buffer to the file
            self.buffer = []  # Clear the buffer after saving the data

        return 1  # Return the length of the output items (not used here)
