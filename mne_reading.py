# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 16:32:54 2024

@author: ismai
"""

import mne

eog_channels = ['EXG Channel 0', 'EXG Channel 1', 'EXG Channel 2', 
            'EXG Channel 3', 'EXG Channel 4', 'EXG Channel 5', 
            'EXG Channel 6', 'EXG Channel 7', 'EXG Channel 8', 
            'EXG Channel 9', 'EXG Channel 10', 'EXG Channel 11', 
            'EXG Channel 12', 'EXG Channel 13', 'EXG Channel 14', 
            'EXG Channel 15']
excluded_channels = ['Accel Channel 0', 'Accel Channel 1', 'Accel Channel 2', 
                     'Other', 'Other', 'Other', 'Other', 'Other', 'Other', 
                     'Other', 'Analog Channel 0', 'Analog Channel 1', 'Analog Channel 2']
data = mne.io.read_raw_bdf("OpenBCI-RAW-NEW-HELMET-2024-02-09_16-49-28.bdf", eog=eog_channels, misc=None, stim_channel='auto', exclude=(excluded_channels), infer_types=False, include=None, preload=False, units=None, encoding='utf8', *, verbose=None)