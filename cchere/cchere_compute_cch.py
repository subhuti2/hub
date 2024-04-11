from datetime import datetime

def convert_to_decimal_hours(time_str):
    # Parse the time string into a datetime object
    time_obj = datetime.strptime(time_str, '%H:%M:%S')
    
    # Calculate the total hours with decimals
    decimal_hours = time_obj.hour + time_obj.minute / 60 + time_obj.second / 3600
    
    return decimal_hours

# Read data from the file
file_name0 = "T_maqianzu.txt"
with open(file_name1, 'r') as file:
    for line in file:
        # Strip any leading/trailing whitespaces and newline characters
        line = line.strip()
        # Convert the time string to decimal hours
        t0 = convert_to_decimal_hours(line)
file_name1 = "T_fengcheng.txt"
with open(file_name1, 'r') as file:
    for line in file:
        # Strip any leading/trailing whitespaces and newline characters
        line = line.strip()
        # Convert the time string to decimal hours
        t1 = convert_to_decimal_hours(line)
file_name2 = "T_caigentan.txt"
with open(file_name1, 'r') as file:
    for line in file:
        # Strip any leading/trailing whitespaces and newline characters
        line = line.strip()
        # Convert the time string to decimal hours
        t2 = convert_to_decimal_hours(line)
