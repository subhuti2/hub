# pytest4.py
# -*- coding: utf-8 -*-
"""
Modified on Fri Sep 13 12:59:27 2024

@author: peng_

This is a script to test paradox play
"""

# # 002 test read in state file and merge and then write again
import paradox_text_utils as pt

# Example usage
input_file = 'C:/Users/peng_/Documents/Paradox Interactive/Victoria 3/mod/2410_vic3_vanila/common/history/states/00_states.txt'  
output_file = 'C:/Users/peng_/Documents/Paradox Interactive/Victoria 3/mod/2410_vic3_vanila/common/history/states/01_states.txt'  

# Step 1: Remove comments and newlines
processed_text = pt.remove_comments_and_newlines(input_file)

# Step 2: Parse the text
parsed_data = pt.parse_text(processed_text)

# Step 3: Write the parsed data back to the output file
pt.dict_to_text(parsed_data, output_file)

# Remove comments and parse both files
processed_text1 = pt.remove_comments_and_newlines(input_file)
processed_text2 = pt.remove_comments_and_newlines(output_file)

parsed_data1 = pt.parse_text(processed_text1)
parsed_data2 = pt.parse_text(processed_text2)

# Collect the owned_provinces from both parsed data
owned_provinces_list1 = pt.collect_owned_provinces(parsed_data1)
owned_provinces_list2 = pt.collect_owned_provinces(parsed_data2)

# Compare the two lists and write the differences to a file
output_diff_file = 'path/to/output_differences.txt'
compare_owned_provinces_lists(owned_provinces_list1, owned_provinces_list2, output_diff_file)

print(f"Differences written to {output_diff_file}")



# print(f"Output written to {output_file}")

# import os
# import pprint  # Import pprint module
# import paradox_text_utils as pt

# # Example usage
# input_file = 'C:/Users/peng_/Documents/Paradox Interactive/Victoria 3/mod/2410_vic3_vanila/common/history/states/00_states.txt'  
# output_file = 'C:/Users/peng_/Documents/Paradox Interactive/Victoria 3/mod/2410_vic3_vanila/common/history/states/01_states.txt'  

# processed_text = pt.remove_comments_and_newlines(input_file)

# parsed_data = pt.parse_text(processed_text)

# parsed_data = pt.clean_owned_provinces_values(parsed_data)

# output_text = pt.dict_to_text(parsed_data)

# with open(output_file, 'w', encoding='utf-8-sig') as file:
#     file.write(output_text)
    
  
# pairs = parsed_data.get('__pairs__', [])
# keys = [key for key, _ in pairs]
# print("Top-level keys:", keys)

# # After parsing the text
# parsed_data = pt.parse_text(processed_text)

# # Helper function to get value by key
# def get_value_from_pairs(pairs, target_key):
#     for key, value in pairs:
#         if key == target_key:
#             return value
#     return None  # or raise an exception

# # Access 'STATES' value
# pairs = parsed_data.get('__pairs__', [])
# states_value = get_value_from_pairs(pairs, 'STATES')

# if states_value is not None:
#     print("Successfully accessed 'STATES' value.")
#     # You can now work with states_value
# else:
#     print("'STATES' key not found in parsed_data.")

# # Step 2: Parse the text
# parsed_data = pt.parse_text(processed_text)

# # Check the parsed data
# print("Parsed Data:")
# pprint.pprint(parsed_data)

    
# # Check the content of parsed_data
# pprint.pprint(parsed_data)


# output_text = pt.dict_to_text(parsed_data)
# with open(output_file, 'w', encoding='utf-8') as file:
#  file.write(output_text)
 
# os.system('cls')
# os.system('clear')    
    
# 001 :     unknow test
# import sys
# import os

# # Add the directory where vic3_read_state_file.py is located
# sys.path.append("C:/Users/peng_/git/hub/paradox")

# # Import the function from vic3_read_state_file.py
# from vic3_read_state import vic3_read_state

# # Example usage of the function
# file_path = "C:/Users/peng_/Documents/Paradox Interactive/Victoria 3/mod/tmp/t3/11_east_asia.txt"

# blocks = vic3_read_state(file_path)

# # Print the result
# for block in blocks:
#     print("Block start")
#     print(block)
#     print("Block end\n")


