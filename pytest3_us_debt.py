#!/usr/bin/env python3

import requests
import zipfile
import io
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

# URL of the online zip file
url = 'https://fiscaldata.treasury.gov/static-data/downloads/zip/c90212ec30bcf5e9fd2d2dff262ea56fa65aa7f5dbe8067ee7894d75ba591099/HstDebt_17900101_20230930.zip'

# Download the zip file
response = requests.get(url)
zip_content = zipfile.ZipFile(io.BytesIO(response.content))

# Extract the zip file in the current directory
zip_content.extractall()

# Assuming there is a CSV file in the zip, load it
df = pd.read_csv('HstDebt_17900101_20230930.csv')
print(df.head())

debt_hist = df.iloc[:, 1]  # ':' means all rows, '0' is the first column index
year_id = df.iloc[:, 3]  # ':' means all rows, '0' is the first column index

# Calculate differences divided by the next element for all but the last element
debt_add_per_year = (debt_hist - debt_hist.shift(-1)) / debt_hist.shift(-1) * 100  # Convert to percentage
# Set the last element to 0 because there's no next element to compare with
debt_add_per_year.iloc[-1] = 0

# # # # Prepare data for line segments
# # # points = np.array([year_id, debt_add_per_year]).T.reshape(-1, 1, 2)
# # # segments = np.concatenate([points[:-1], points[1:]], axis=1)

# # # # Create a LineCollection
# # # lc = LineCollection(segments, cmap='coolwarm', norm=plt.Normalize(0, 100))
# # # lc.set_array(debt_add_per_year[:-1])  # Color mapping based on debt increase rate
# # # lc.set_linewidth(2)

# # # fig, ax = plt.subplots()
# # # ax.add_collection(lc)
# # # ax.autoscale()
# # # ax.margins(0.1)

# # # ax.set_xlabel('Year')
# # # ax.set_ylabel('Debt Increase Rate (%)')
# # # ax.set_title("Yearly Debt Increase Rate")
# # # ax.legend([lc], ['Debt Increase Rate'], loc='upper left')

# # # # Set the x-axis limits to focus on 1930 to 2000
# # # ax.set_xlim(1780, 2030)

# # # plt.show()


# Plotting
fig, ax = plt.subplots()  # Create a figure and an axes.
ax.plot(year_id, debt_add_per_year, linewidth=1, label='Debt Increase')  # Plot some data on the axes.
#ax.set_xlabel('Year', fontsize=12)  # Add an x-label to the axes.
#ax.set_ylabel('Debt Increase Rate(%)', fontsize=12)  # Add a y-label to the axes.
ax.set_title("Yearly Debt Increase Rate (%)", fontsize=12)  # Add a title to the axes.

# Limit the range of the x-axis
#ax.set_xlim(1930, 2000)

# Add a horizontal line at y=0 in black
ax.axhline(y=0, color='black', linewidth=1)

# # Add vertical lines in red
# ax.axvline(x=1917, color='red', linewidth=1, label='WW I')
# ax.axvline(x=1941, color='green', linewidth=1, label='WW II')

# # Add text description near the vertical line
# ax.text(1917, ax.get_ylim()[1] * 0.95, 'First World War', horizontalalignment='right', color='red')

# Add vertical lines in color for events
ax.axvline(x=1812, color='#FF0077', linewidth=0.5, label='Britain 1812')
ax.axvline(x=1837, color='#00FFFF', linewidth=0.5, label='Jackson')
ax.axvline(x=1861, color='#FF00FF', linewidth=0.5, label='Civil war')
#ax.axvline(x=1865, color='#FF00FF', linewidth=0.5, label='Civil war')
#ax.axvline(x=1898, color='#00FFFF', linewidth=0.5, label='Spanish war')
ax.axvline(x=1917, color='#FF0000', linewidth=0.5, label='WW I')
#ax.axvline(x=1918, color='#FF0000', linewidth=0.5, label='WW I')
ax.axvline(x=1941, color='#00FF00', linewidth=0.5, label='WW II')
#ax.axvline(x=1945, color='#00FF00', linewidth=0.5, label='WW II')
#ax.axvline(x=1981, color='#FF0077', linewidth=0.5, label='Reagan in')
#ax.axvline(x=2001, color='#FF3333', linewidth=0.5, label='Bush2 in')

ax.legend(fontsize=6)  # Add a legend.

# Export the figure to a PNG file
plt.savefig('US_Debt_Increase_Rate.png', dpi=300)  # Save the figure to a file named 'plot.png' with 300 DPI

plt.show()  # Show the plot


