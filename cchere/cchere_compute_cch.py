import os
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

def load_timestamps(filename):
    """
    Load timestamps from a given file, convert them from 'hh:mm:ss' to decimal hours.
    
    Parameters:
    - filename: str, the name of the file containing timestamps.
    
    Returns:
    - numpy array of timestamps converted to decimal hours.
    """
    with open(f'T_{filename}.txt', 'r') as file:
        timestamps = []
        for line in file:
            time_str = line.strip()
            # Convert the time string to a datetime object
            time_obj = datetime.strptime(time_str, '%H:%M:%S')
            # Calculate the total hours as decimal
            decimal_hours = time_obj.hour + time_obj.minute / 60 + time_obj.second / 3600
            timestamps.append(decimal_hours)
    return np.array(timestamps)

def compute_normalized_cch(timestamps1, timestamps2, bin_size, max_lag):
    bins = np.arange(-max_lag, max_lag + bin_size, bin_size)
    time_diffs = np.subtract.outer(timestamps1, timestamps2).flatten()
    cch_raw, _ = np.histogram(time_diffs, bins=bins)
    geometric_mean = np.sqrt(len(timestamps1) * len(timestamps2))
    cch_normalized = cch_raw / geometric_mean
    cch_bins = (bins[:-1] + bins[1:]) / 2
    return cch_bins, cch_normalized

def plot_and_save_cch(cch_bins, cch_normalized, filename1, filename2):
    plt.figure()
    plt.bar(cch_bins, cch_normalized, width=bin_size, edgecolor='black')
    plt.xlabel('Time Lag')
    plt.ylabel('Normalized CCH')
    plt.title(f'CCH: {filename1} vs {filename2}')
    plt.grid(True)
    
    # Generate a timestamped filename for the plot
    timestamp_str = datetime.now().strftime("%Y%m%d-%H%M%S")
    plt_filename = f'CCH_{filename1}_vs_{filename2}_{timestamp_str}.png'
    
    # Remove characters that might be problematic for filenames
    plt_filename = plt_filename.replace('.txt', '').replace(':', '_')

    plt.savefig(plt_filename)
    plt.close()

# Example usage
bin_size = 1  # Adjust as necessary
max_lag = 24  # Adjust as necessary

with open('cch1.txt', 'r') as file1, open('cch2.txt', 'r') as file2:
    filenames1 = file1.readlines()
    filenames2 = file2.readlines()

if len(filenames1) != len(filenames2):
    raise ValueError("The files cch1.txt and cch2.txt have a different number of lines.")

for filename1, filename2 in zip(filenames1, filenames2):
    timestamps1 = load_timestamps(filename1.strip())
    timestamps2 = load_timestamps(filename2.strip())
    
    cch_bins, cch_normalized = compute_normalized_cch(timestamps1, timestamps2, bin_size, max_lag)
    
    plot_and_save_cch(cch_bins, cch_normalized, filename1.strip(), filename2.strip())
