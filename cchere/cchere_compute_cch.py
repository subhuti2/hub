import os
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

def read_from_files(file_in):
    """
    Reads usernames from a file.
    Returns a list of usernames if the file exists.
    Returns None if the file does not exist.
    """
    if not os.path.exists(file_in):
        return None
    
    with open(file_in, 'r', encoding='utf-8') as fin:
        # Strip newlines and return usernames list
        return [line.strip() for line in fin.readlines()]

def convert_to_decimal_hours(time_str):
    time_obj = datetime.strptime(time_str, '%H:%M:%S')
    decimal_hours = time_obj.hour + time_obj.minute / 60 + time_obj.second / 3600
    return decimal_hours

def read_time_stamps(user_name):
    file_name = f'T_{user_name}.txt'
    
    # Check if the file exists
    if not os.path.exists(file_name):
        print(f"File {file_name} not found.")
        return

    time_stamps = []
    with open(file_name, 'r') as file:
        for line in file:
            line = line.strip()
            decimal_hours = convert_to_decimal_hours(line)
            time_stamps.append(decimal_hours)

    return time_stamps


def compute_cross_correlation(timestamps1, timestamps2, bin_size, max_lag):
    """
    Compute the cross-correlation histogram (CCH) between two sets of timestamps.
    
    Parameters:
    - timestamps1: numpy array of timestamps for the first series
    - timestamps2: numpy array of timestamps for the second series
    - bin_size: the size of bins for the histogram, in the same time unit as the timestamps
    - max_lag: the maximum lag to consider for cross-correlation, in the same time unit
    
    Returns:
    - cch_bins: the centers of bins in the histogram
    - cch_counts: the count of timestamp differences in each bin
    """
    # Calculate all pairwise differences between timestamps
    time_diffs = np.subtract.outer(timestamps1, timestamps2).flatten()
    
    # Filter out differences that are beyond the max lag
    valid_diffs = time_diffs[(time_diffs >= -max_lag) & (time_diffs <= max_lag)]
    
    # Histogram the valid differences to get the cross-correlation histogram
    cch_counts, edges = np.histogram(valid_diffs, bins=np.arange(-max_lag, max_lag + bin_size, bin_size))
    
    # Calculate the bin centers from the edges
    cch_bins = (edges[:-1] + edges[1:]) / 2
    
    return cch_bins, cch_counts

# Example usage
timestamps1 = np.array([0.1, 0.2, 0.5, 1.0, 1.5]) # Example timestamp data in seconds
timestamps2 = np.array([0.15, 0.45, 0.9, 1.4]) # Another set of timestamp data
bin_size = 0.1 # Bin size in seconds
max_lag = 1.0 # Maximum lag to consider in seconds

cch_bins, cch_counts = compute_cross_correlation(timestamps1, timestamps2, bin_size, max_lag)

print("CCH Bins:", cch_bins)
print("CCH Counts:", cch_counts)

usernames = read_from_files('user_out0.txt')

if usernames is not None:
    for user_name in usernames:
        plot_data_dist(user_name)
else:
    print("Usernames file not found or other error.")
