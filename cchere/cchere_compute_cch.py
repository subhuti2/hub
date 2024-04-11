import os
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
from datetime import datetime
import matplotlib.pyplot as plt


def read_from_files(file_in):
    """
    Reads usernames and output tags from files.
    Returns lists of usernames and output tags if files exist and have matching line counts.
    Returns None, None if conditions are not met.
    """
    if not os.path.exists(file_in) :
        return None
    
    with open(file_in, 'r', encoding='utf-8') as fin:
        usernames = fin.readlines()

def convert_to_decimal_hours(time_str):
    # Parse the time string into a datetime object
    time_obj = datetime.strptime(time_str, '%H:%M:%S')
    
    # Calculate the total hours with decimals
    decimal_hours = time_obj.hour + time_obj.minute / 60 + time_obj.second / 3600
    
    return decimal_hours


def plot_data_dist(user_name):

    # Read data from the file
    time_stamps = []
    file_name = f'T_{user_name}.txt'
    with open(file_name, 'r') as file:
        for line in file:
            # Strip any leading/trailing whitespaces and newline characters
            line = line.strip()
            # Convert the time string to decimal hours
            decimal_hours = convert_to_decimal_hours(line)
            time_stamps.append(decimal_hours)

    # Create bins for the distribution
    num_bins = 24
    bins = [i for i in range(num_bins + 1)]

    # Plot the distribution
    plt.hist(time_stamps, bins=bins, edgecolor='black')
    plt.xlabel('Hours (est.)')
    plt.ylabel('Frequency')
    plt.title('Distribution of Time Data')
    plt.xticks([0, 6, 12, 18, 24])
    plt.grid(True)

    # Save the figure as a PNG file
    plt.savefig(f'Dist_{user_name}.png')

    # Close the plot to free up memory
    plt.close()


usernames = read_from_files('user_out0.txt')
for user_name in usernames:
    plot_data_dist(user_name)