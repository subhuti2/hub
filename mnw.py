# # # # # # # # # # # # # # # # # # 
# # # Access raw data¶
# # # # # # # # # # # # # # # # # # 

#prepare the environment
import mne
mne.set_log_level('WARNING')
%pylab inline
data_path = '/Users/wang/mne/sample_data/MNE-sample-data/MEG/sample/'

#load the sample data and check
raw_fname = data_path + '/sample_audvis_filt-0-40_raw.fif'
raw = mne.io.Raw(raw_fname)
print(raw)
start, stop = raw.time_as_index([100, 115])  # 100 s to 115 s data segment
data, times = raw[:, start:stop]
picks = mne.pick_types(raw.info, meg='mag', exclude=[])
data, times = raw[picks[:10], start:stop]

#plot this piece of data
import pylab as pl
pl.plot(times, data.T)
pl.xlabel('time (s)')
pl.ylabel('MEG data (T)')

#save data
picks = mne.pick_types(raw.info, meg=True, eeg=False, stim=True, exclude=[])
raw.save('sample_audvis_meg_raw.fif', tmin=0, tmax=150, picks=picks)

# # # # # # # # # # # # # # # # # # 
# # # Define and read epochs¶
# # # # # # # # # # # # # # # # # # 

# check data with certain events
events = mne.find_events(raw, stim_channel='STI 014')
print(events[:5])
event_id = dict(aud_l=1, aud_r=2)  # event trigger and conditions
tmin = -0.2  # start of each epoch (200ms before the trigger)
tmax = 0.5  # end of each epoch (500ms after the trigger)

raw.info['bads'] = ['MEG 2443', 'EEG 053']
print(raw.info['bads'])

picks = mne.pick_types(raw.info, meg=True, eeg=True, eog=True, stim=False, exclude=raw.info['bads'])
mag_picks = mne.pick_types(raw.info, meg='mag', eog=True, exclude=raw.info['bads'])
grad_picks = mne.pick_types(raw.info, meg='grad', eog=True, exclude=raw.info['bads'])

baseline = (None, 0)  # means from the first instant to t = 0
reject = dict(grad=4000e-13, mag=4e-12, eog=150e-6)

epochs = mne.Epochs(raw, events, event_id, tmin, tmax, proj=True, picks=picks, baseline=baseline, preload=False, reject=reject, verbose='WARNING')
print(epochs)

epochs_data = epochs['aud_l'].get_data()
print(epochs_data.shape)

from scipy import io
io.savemat('epochs_data.mat', dict(epochs_data=epochs_data), oned_as='row')

epochs.save('sample-epo.fif')

evoked = epochs['aud_l'].average()
print(evoked)

max_in_each_epoch = [e.max() for e in epochs['aud_l']]
print(max_in_each_epoch[:4])

c_path = '/Users/wang/mne/tmp_data/'
evoked_fname = data_path + 'sample_audvis-ave.fif'
# evoked1 = mne.fiff.Evoked(evoked_fname, setno=1, baseline=(None, 0), proj=True)
evoked1 = mne.Evoked(evoked_fname, condition=0, proj=True)  #baseline=(None, 0) was not applicable
evoked2 = mne.Evoked(evoked_fname, condition=1, proj=True)  
evoked3 = mne.Evoked(evoked_fname, condition='Left visual', proj=True)  

# contrast = evoked1 - evoked2    #unsupported operand type(s) for -: 'Evoked' and 'Evoked'

# # # # # # # # # # # # # # # # # # 
# # # Time-Frequency: Induced power and phase-locking values¶
# # # # # # # # # # # # # # # # # # 

import numpy as np
n_cycles = 2  # number of cycles in Morlet wavelet
frequencies = np.arange(7, 30, 3)  # frequencies of interest
Fs = raw.info['sfreq']  # sampling in Hz
times = epochs.times

from mne.time_frequency import EpochsTFR
power, phase_lock = EpochsTFR(epochs_data, Fs=Fs, frequencies=frequencies, n_cycles=2, n_jobs=1)

# baseline corrections with ratio
power /= np.mean(power[:, :, times < 0], axis=2)[:, :, None]
