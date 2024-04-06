# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import mne
import os
import os.path as opo
import numpy as np

# Step 1: Read the data
data = pd.read_csv('OpenBCI-RAW-NEW-HELMET-2024-02-09_16-49-28.txt', delimiter=',', skiprows=4)

# Extract the EEG data and timestamps
eeg_channels = [' EXG Channel 0', ' EXG Channel 1', ' EXG Channel 2', 
                ' EXG Channel 3', ' EXG Channel 4', ' EXG Channel 5', 
                ' EXG Channel 6', ' EXG Channel 7']
eeg_data = data[eeg_channels].values.T  # Transpose to have channels as rows
timestamps = pd.to_datetime(data[' Timestamp (Formatted)'])
t = (timestamps - timestamps[0]).dt.total_seconds().values

# Step 2: Scale the data from microvolts to volts
eeg_data_volts = eeg_data / 1e6  # Convert from μV to V

# Step 3: Create the MNE Info object
sfreq = 250  # The sampling frequency of your EEG data
info = mne.create_info(ch_names=eeg_channels, sfreq=sfreq, ch_types='eeg')

# Step 4: Create the Raw object
raw = mne.io.RawArray(eeg_data_volts, info)
raw.load_data()



import matplotlib.pyplot as plt

# Assuming 'eeg_data' is your data array in volts
plt.figure(figsize=(15, 7))
for i in range(8):
    plt.subplot(8, 1, i+1)
    plt.plot(eeg_data[i, :1000])  # Plotting only the first 1000 samples
    plt.title(f'Channel {i}')
    plt.tight_layout()
plt.show()

