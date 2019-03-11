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