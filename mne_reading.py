
import mne
import numpy as np
import matplotlib.pyplot as plt

# Define channel lists
eog_channels = ['EXG Channel 0', 'EXG Channel 1', 'EXG Channel 2', 
                'EXG Channel 3', 'EXG Channel 4', 'EXG Channel 5', 
                'EXG Channel 6', 'EXG Channel 7', 'EXG Channel 8', 
                'EXG Channel 9', 'EXG Channel 10', 'EXG Channel 11', 
                'EXG Channel 12', 'EXG Channel 13', 'EXG Channel 14', 
                'EXG Channel 15']
channel_types = {'EXG Channel 0': 'eog', 'EXG Channel 1': 'eog', 'EXG Channel 2': 'eog', 
                'EXG Channel 3': 'eog', 'EXG Channel 4': 'eog', 'EXG Channel 5': 'eog', 
                'EXG Channel 6': 'eog', 'EXG Channel 7': 'eog', 'EXG Channel 8': 'eog', 
                'EXG Channel 9': 'eog', 'EXG Channel 10': 'eog', 'EXG Channel 11': 'eog', 
                'EXG Channel 12': 'eog', 'EXG Channel 13': 'eog', 'EXG Channel 14': 'eog', 
                'EXG Channel 15': 'eog'}
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
info = mne.create_info(ch_names = eog_channels, sfreq=sfreq, ch_types='eog')

# Step 4: Create the Raw object
raw = mne.io.RawArray(eog_data_volts, info)
raw.set_channel_types(channel_types)


# Step 5: Filtering the data

def add_arrows(axes):
    """Add some arrows at 60 Hz and its harmonics."""
    for ax in axes:
        freqs = ax.lines[-1].get_xdata()
        psds = ax.lines[-1].get_ydata()
        for freq in (60, 120, 180, 240):
            idx = np.searchsorted(freqs, freq)
            # get ymax of a small region around the freq. of interest
            y = psds[(idx - 4) : (idx + 5)].max()
            ax.arrow(
                x=freqs[idx],
                y=y + 18,
                dx=0,
                dy=-12,
                color="red",
                width=0.1,
                head_width=3,
                length_includes_head=True,
            )

# Get the indices of the EOG channels
picks = mne.pick_channels(raw, eog_channels, excluded_channels, True)

fig = raw.compute_psd(fmax=62.5).plot(
    average=True, amplitude=False, picks=picks
)

add_arrows(fig.axes[:2])
