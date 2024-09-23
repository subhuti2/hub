import os
import re

# # Regex to match all provinces (strings starting with "x") inside quotes, even across multiple lines
# province_pattern = re.compile(r'"(x\w+)"')

# # Function to check for duplicate provinces in a file
# def check_duplicate_provinces(file_path):
#     with open(file_path, 'r', encoding='utf-8-sig') as f:
#         file_content = f.read()

#     # Dictionary to track which state each province belongs to and to detect duplicates
#     province_to_state = {}
#     duplicates = {}

#     # Find all state blocks in the file
#     state_blocks = re.findall(r'(STATE_\w+)\s*=\s*\{([^}]*)\}', file_content, re.DOTALL)

#     # Loop through each state block and extract the provinces
#     for state_name, state_content in state_blocks:
#         # Extract all provinces for this state (matching strings that start with 'x')
#         provinces = province_pattern.findall(state_content)

#         # Check for duplicates within and across states
#         seen_in_state = set()  # Track provinces seen within this state
#         for province in provinces:
#             # Check if province is already seen within the same state
#             if province in seen_in_state:
#                 # Duplicate within the same state
#                 if province not in duplicates:
#                     duplicates[province] = []
#                 duplicates[province].append(f"{state_name} (within state)")
#             else:
#                 seen_in_state.add(province)

#             # Check if province is seen across different states
#             if province in province_to_state and province_to_state[province] != state_name:
#                 if province not in duplicates:
#                     duplicates[province] = []
#                 duplicates[province].append(f"{state_name} (and also in {province_to_state[province]})")
#             else:
#                 province_to_state[province] = state_name

#     # Output duplicate provinces
#     if duplicates:
#         print(f"Duplicate provinces found in file: {file_path}")
#         for province, locations in duplicates.items():
#             print(f"Province {province} is duplicated in: {', '.join(locations)}")
#     else:
#         print(f"No duplicate provinces found in file: {file_path}")

# # Example usage
# file_path = "C:/Users/peng_/Documents/Paradox Interactive/Victoria 3/mod/2410_vic3_vanila/map_data/t2/11_east_asia.txt"
# check_duplicate_provinces(file_path)

# Regex to match all provinces (strings starting with "x") inside quotes, even across multiple lines
province_pattern = re.compile(r'"(x\w+)"')

# Function to extract all provinces from a folder
def extract_provinces_from_folder(folder_path):
    all_provinces = set()  # To store unique provinces

    # Loop through all .txt files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                file_content = f.read()

            # Find all provinces in the file (matching strings that start with 'x')
            provinces = province_pattern.findall(file_content)
            all_provinces.update(provinces)  # Add provinces to the set (ensures uniqueness)

    return all_provinces

# Function to compare provinces between two folders
def compare_folders(folder1, folder2):
    # Extract provinces from both folders
    provinces_folder1 = extract_provinces_from_folder(folder1)
    provinces_folder2 = extract_provinces_from_folder(folder2)

    # Provinces unique to each folder
    unique_to_folder1 = provinces_folder1 - provinces_folder2
    unique_to_folder2 = provinces_folder2 - provinces_folder1

    # Number of provinces in each folder
    print(f"Number of provinces in {folder1}: {len(provinces_folder1)}")
    print(f"Number of provinces in {folder2}: {len(provinces_folder2)}")

    # Report unique provinces
    if unique_to_folder1:
        print(f"\nProvinces unique to {folder1}:")
        for province in unique_to_folder1:
            print(province)
    else:
        print(f"\nNo unique provinces in {folder1} compared to {folder2}.")

    if unique_to_folder2:
        print(f"\nProvinces unique to {folder2}:")
        for province in unique_to_folder2:
            print(province)
    else:
        print(f"\nNo unique provinces in {folder2} compared to {folder1}.")

# Example usage
folder1 = "C:/Users/peng_/Documents/Paradox Interactive/Victoria 3/mod/2410_vic3_vanila/map_data/t3"
folder2 = "C:/Games/Victoria III/game/map_data/state_regions"
compare_folders(folder1, folder2)
