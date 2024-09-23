# -*- coding: utf-8 -*-
"""
Created on Sat Jul  6 12:55:31 2024

@author: peng_
"""

import codecs
import re
import os

# Specify the path to the directory
directory_path =  r'C:\Users\peng_\Documents\Paradox Interactive\Crusader Kings III\mod\2466_AGOT\common\script_values'

# Specify the full paths for the input and output files
input_file = os.path.join(directory_path, '00_agot_men_at_arms_values.txt')
output_file = os.path.join(directory_path, '00_agot_men_at_arms_values1.txt')

# Open the input file with UTF-8-BOM encoding
with codecs.open(input_file, 'r', encoding='utf-8-sig') as infile:
    lines = infile.readlines()

# Prepare the output lines
output_lines = []

# Regular expression to match lines in the format some_string = some_number
line_pattern = re.compile(r'^(\s*\S+)\s*=\s*(\d+\.\d+|\d+)\s*$')

# Process each line
for line in lines:
    # Strip the line to remove leading/trailing whitespace
    stripped_line = line.strip()
    
    # Check if the line is a comment or blank
    if stripped_line.startswith('#') or not stripped_line:
        output_lines.append(line)
    else:
        # Check if the line matches the pattern some_string = some_number
        match = line_pattern.match(stripped_line)
        if match:
            some_string = match.group(1)
            some_number = match.group(2)
            new_line = f"{some_string} = @[the_factor * {some_number}]\n"
            output_lines.append(new_line)
        else:
            # If the line does not match the pattern, copy it as is
            output_lines.append(line)

# Write the output lines to the output file with UTF-8-BOM encoding
with codecs.open(output_file, 'w', encoding='utf-8-sig') as outfile:
    outfile.writelines(output_lines)

print(f"File '{output_file}' has been created with the modified content.")
