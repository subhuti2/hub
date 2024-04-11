import os
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
from datetime import datetime
import matplotlib.pyplot as plt

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

def plot_data_dist(user_name):
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

    num_bins = 24
    bins = [i for i in range(num_bins + 1)]

    plt.hist(time_stamps, bins=bins, edgecolor='black')
    plt.xlabel('Hours (est.)')
    plt.ylabel('Frequency')
    plt.title('Distribution of Time Data')
    plt.xticks([0, 6, 12, 18, 24])
    plt.grid(True)

    plt.savefig(f'Dist_{user_name}.png')
    plt.close()

usernames = read_from_files('user_out0.txt')

if usernames is not None:
    for user_name in usernames:
        plot_data_dist(user_name)
else:
    print("Usernames file not found or other error.")
