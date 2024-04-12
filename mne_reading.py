# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 16:32:54 2024

@author: ismai
"""

import mne
import matplotlib.pyplot as plt

# Define channel lists
eog_channels = ['EXG Channel 0', 'EXG Channel 1', 'EXG Channel 2', 
                'EXG Channel 3', 'EXG Channel 4', 'EXG Channel 5', 
                'EXG Channel 6', 'EXG Channel 7', 'EXG Channel 8', 
                'EXG Channel 9', 'EXG Channel 10', 'EXG Channel 11', 
                'EXG Channel 12', 'EXG Channel 13', 'EXG Channel 14', 
                'EXG Channel 15']
excluded_channels = ['Sample Index','Accel Channel 0', 'Accel Channel 1', 'Accel Channel 2', 
                     'Other', 'Other', 'Other', 'Other', 'Other', 'Other', 
                     'Other', 'Analog Channel 0', 'Analog Channel 1', 'Analog Channel 2', 'Timestamp', 'Other', 'Timestamp (Forma']

# Load BDF file
data = mne.io.read_raw_bdf("OpenBCI-RAW-NEW-HELMET-2024-02-09_16-49-28.bdf", 
                            eog=eog_channels, misc=None, stim_channel='auto', 
                            exclude=excluded_channels, infer_types=False, 
                            preload=True, verbose=None)

# Step 2: Convert EEG data from microvolts to volts
eog_data_volts = data.get_data() / 1e6  # Convert from μV to V

# Step 3: Create MNE Info object
sfreq = data.info['sfreq']  # Sampling frequency
info = mne.create_info(ch_names=eog_channels, sfreq=sfreq, ch_types='eog')

# Step 4: Create the Raw object
raw = mne.io.RawArray(eog_data_volts, info)

# Plot the EEG data
plt.figure(figsize=(15, 7))
for i in range(len(eog_channels)):
    plt.subplot(len(eog_channels), 1, i+1)
    plt.plot(eog_data_volts[i, :1000])  # Plotting only the first 1000 samples
    plt.title(f'Channel {eog_channels[i]}')
    plt.tight_layout()
plt.show()