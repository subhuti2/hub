import requests
import re
import datetime
from bs4 import BeautifulSoup
from urllib.parse import quote

# Record the start time
start_time = datetime.datetime.now()
print(f"Program started at: {start_time}")

# Ask the user for the username
raw_username = input("Please enter the username: ")

# URL-encode the username
encoded_username = quote(raw_username)

# Use the encoded username in the URL
url = f'https://talkcc.net/user/{encoded_username}/所有帖/'

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Assuming you have your BeautifulSoup object named `soup`

# To get the value from the <input> element:
input_tag = soup.find('input', {'name': 'p', 'type': 'text'})
if input_tag:
    number_pages = int(input_tag.get('value'))  # Convert to integer
    print("Number of pages:", number_pages)
else:
    print("Number of pages information not found.")

# Initialize lists to store dates and times
x_dates = []
x_times = []

for i in range(1, number_pages + 1):

    # Corrected URL interpolation using f-string and the encoded username inside the loop
    the_url = f'https://talkcc.net/user/{encoded_username}/所有帖/{i}'

    response = requests.get(the_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Adjust the selector to match the HTML structure of your target web page
    timestamp_elements = soup.select('.s_FlexSB small')

    # Loop through each element and split the text into date and time
    for element in timestamp_elements:

        timestamp_text = element.text.strip()
        # Assuming the format is consistent as 'YYYY-MM-DD HH:MM:SS'
        date_part, time_part = timestamp_text.split(' ')
        
        # Append the separated parts to their respective lists
        x_dates.append(date_part)
        x_times.append(time_part)


# Sanitize raw_username for use in filenames
safe_username = re.sub('[^a-zA-Z0-9\n\.]', '_', raw_username)

# Write dates and times to files (assuming x_dates and x_times are populated)
with open(f'{safe_username}_date.txt', 'w', encoding='ascii') as date_file, \
     open(f'{safe_username}_time.txt', 'w', encoding='ascii') as time_file:
    for date in x_dates:
        date_file.write(date + '\n')
    for time in x_times:
        time_file.write(time + '\n')


# Record the end time
end_time = datetime.datetime.now()
print(f"Program ended at: {end_time}")

# Calculate and print the time cost
time_cost = end_time - start_time
print(f"Total time cost to run the program: {time_cost}")