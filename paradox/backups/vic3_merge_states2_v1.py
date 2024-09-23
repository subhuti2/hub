import re

# Step 1: Read the state blocks from the file
def read_text(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        lines = file.readlines()

    # Remove comments (anything after '#') and strip whitespaces
    cleaned_lines = []
    for line in lines:
        line = re.sub(r'#.*', '', line).strip()
        if line:
            cleaned_lines.append(line)
    return ' '.join(cleaned_lines)


# Step 2: parse the text string into dictionary
def parse_string_to_dict(input_string):
    """Main function to parse the input string and handle nested dictionaries."""
    input_string = input_string.strip()

    result_dict = {}
    i = 0
    length = len(input_string)

    while i < length:
        while i < length and input_string[i].isspace():
            i += 1  # Skip any whitespace

        key_start = i
        while i < length and not input_string[i].isspace() and input_string[i] != '=':
            i += 1
        key = input_string[key_start:i].strip()

        if not key:
            break  # End if no key is found

        while i < length and input_string[i].isspace():
            i += 1

        if i < length and input_string[i] == '=':
            i += 1
        else:
            raise ValueError(f"Expected '=' after key '{key}'")

        while i < length and input_string[i].isspace():
            i += 1

        # If value starts with '{', handle it as a list or nested block
        if i < length and input_string[i] == '{':
            value_start = i
            value_end = find_matching_brace(input_string, i)  # Find matching closing brace
            nested_block = input_string[value_start+1:value_end].strip()  # Content inside {}

            # Check if it's a list of words (like owned_provinces)
            if '=' not in nested_block and '{' not in nested_block:
                # Split the content by whitespace into a list of words
                value_list = nested_block.split()

                # Assign the list of values to the key
                result_dict[key] = value_list
            else:
                # Recursively process the nested dictionary
                nested_dict = parse_string_to_dict(nested_block)

                # Append the dictionary to the key if it exists
                if key in result_dict:
                    if isinstance(result_dict[key], list):
                        result_dict[key].append(nested_dict)
                    else:
                        result_dict[key] = [result_dict[key], nested_dict]
                else:
                    result_dict[key] = nested_dict

            i = value_end + 1
        else:
            value_start = i
            while i < length and not input_string[i].isspace():
                i += 1
            value = input_string[value_start:i].strip()

            # Handle repeated keys (like add_homeland)
            if key in result_dict:
                if isinstance(result_dict[key], list):
                    result_dict[key].append(value)
                else:
                    result_dict[key] = [result_dict[key], value]
            else:
                result_dict[key] = value

    return result_dict


def find_matching_brace(s, start_index):
    """Helper function to find the index of the matching closing brace for the first opening brace."""
    open_braces = 0
    for i in range(start_index, len(s)):
        if s[i] == '{':
            open_braces += 1
        elif s[i] == '}':
            open_braces -= 1
            if open_braces == 0:
                return i
    raise ValueError("No matching closing brace found.")
    
def collect_owned_provinces(parsed_dict):
    # Initialize an empty list to collect owned_provinces
    all_owned_provinces = []
    
    # Navigate to the 'STATES' section of the dictionary
    states_dict = parsed_dict.get('STATES', {})
    
    # Iterate over all the states (e.g., 's:STATE_NEBRASKA', 's:STATE_XYZ', etc.)
    for state_key, state_value in states_dict.items():
        # print(state_key)
        # Ensure the state has a 'create_state' field and it is a list
        create_state_list = state_value.get('create_state', [])
        
        print(state_key)
       # Iterate over all create_state entries (which should be dictionaries)
        for create_state in create_state_list:
            if isinstance(create_state, dict):  # Ensure it's a dictionary
                # Collect 'owned_provinces' if it exists in this create_state entry
                owned_provinces = create_state.get('owned_provinces', [])
                print(len(owned_provinces))
                # Extend the all_owned_provinces list with the collected owned_provinces
                all_owned_provinces.extend(owned_provinces)
    
    return all_owned_provinces

def find_province_differences(parsed_dict1, parsed_dict2):
    # Use the function to collect all owned provinces from both parsed_dicts
    all_provinces1 = collect_owned_provinces(parsed_dict1)
    all_provinces2 = collect_owned_provinces(parsed_dict2)

    # Convert the lists to sets for efficient set operations (duplicates removed)
    set_provinces1 = set(all_provinces1)
    set_provinces2 = set(all_provinces2)

    # Find provinces in parsed_dict1 but not in parsed_dict2
    diff_1_to_2 = set_provinces1 - set_provinces2

    # Find provinces in parsed_dict2 but not in parsed_dict1
    diff_2_to_1 = set_provinces2 - set_provinces1

    # Find common provinces between the two
    common_provinces = set_provinces1 & set_provinces2

    # Return the sorted differences and common provinces
    return {
        "provinces_in_1_not_in_2": sorted(diff_1_to_2),
        "provinces_in_2_not_in_1": sorted(diff_2_to_1),
        "common_provinces": sorted(common_provinces)
    }

# Example usage
input_file = 'C:/Users/peng_/Documents/Paradox Interactive/Victoria 3/mod/2410_vic3_vanila/common/history/states/00_states.txt'  
output_file = 'C:/Users/peng_/Documents/Paradox Interactive/Victoria 3/mod/2410_vic3_vanila/common/history/states/01_states.txt'  

# Read and parse the state file
input_string1 = read_text(input_file)
parsed_dict1 = parse_string_to_dict(input_string1)

input_string2 = read_text(output_file)
parsed_dict2 = parse_string_to_dict(input_string2)
   

# # Example usage
result = find_province_differences(parsed_dict1, parsed_dict2)
print("Provinces in dict1 but not in dict2:", result["provinces_in_1_not_in_2"])
print("Provinces in dict2 but not in dict1:", result["provinces_in_2_not_in_1"])
#print("Common provinces:", result["common_provinces"])
    
    

