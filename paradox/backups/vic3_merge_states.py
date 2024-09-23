import re
import os

def read_state(file_path):
    # Read the file with the correct encoding (utf-8-sig handles BOM)
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        lines = file.readlines()

    # Remove comments (anything after '#') and strip whitespaces
    cleaned_lines = []
    for line in lines:
        line = re.sub(r'#.*', '', line).strip()
        if line:
            cleaned_lines.append(line)

    blocks = []
    current_block = []

    for line in cleaned_lines:
        if line.startswith('STATE_'):
            if current_block:
                blocks.append(' '.join(current_block))
            current_block = [line]
        else:
            current_block.append(line)

    if current_block:
        blocks.append(' '.join(current_block))

    return blocks

def parse_block(block):
    result = {}

    # Step 1: Extract the state name
    state_name_match = re.match(r"STATE_(\w+)", block)
    if state_name_match:
        state_name = state_name_match.group(1)
        result['state_name'] = state_name
    
    # Step 2: Remove the state name prefix and trim
    block = re.sub(r"STATE_\w+\s*=\s*\{", "", block).strip().rstrip('}')
    
    # Step 3: Regex to match key-value pairs, including nested braces
    pattern = re.compile(r'(\w+)\s*=\s*({.*?}|\d+|"[^"]*")')
    
    # The keys that should be treated as lists of values
    list_keys = ['provinces', 'arable_resources', 'traits', 'impassable', 'prime_land']

    pos = 0
    while pos < len(block):
        match = pattern.match(block, pos)
        if match:
            key, value = match.groups()
            if value.startswith('{') and value.endswith('}'):
                # Handle nested lists like provinces, arable_resources, traits, impassable, prime_land
                if key in list_keys:
                    # Treat as a list of values for specific keys
                    value = parse_list_block(value)
                else:
                    # Treat other nested braces as key-value pairs (like capped_resources)
                    value = parse_nested_block(value)
            elif value.startswith('"') and value.endswith('"'):
                # Remove the quotes for string values
                value = value.strip('"')
            else:
                # Convert numeric values
                value = int(value)

            # Add the key-value pair to the result dictionary
            result[key] = value

            # Move the position forward
            pos = match.end()
        else:
            pos += 1

    return result

def parse_list_block(block):
    """Parses a block like { "value1" "value2" "value3" } into a list."""
    # Remove the outer braces and split by spaces, keeping quoted strings
    values = re.findall(r'"(.*?)"', block)
    return values

def parse_nested_block(nested_block):
    """Parses nested key-value pairs in a block like capped_resources = { key1 = value1 key2 = value2 }."""
    # Remove the outer braces
    nested_block = nested_block.strip('{}').strip()

    # Dictionary to store the parsed key-value pairs
    nested_dict = {}

    # Use the same pattern to match nested key-value pairs
    pattern = re.compile(r'(\w+)\s*=\s*(\d+|"[^"]*")')
    pos = 0
    while pos < len(nested_block):
        match = pattern.match(nested_block, pos)
        if match:
            key, value = match.groups()
            if value.startswith('"') and value.endswith('"'):
                value = value.strip('"')
            else:
                value = int(value)

            nested_dict[key] = value
            pos = match.end()
        else:
            pos += 1

    return nested_dict

def write_results_to_file(results, file_path):
    def format_value(value, indent_level):
        """Formats the value for output, handling dictionaries, lists, and simple values."""
        indent = '    ' * indent_level
        if isinstance(value, dict):
            # If the value is a dictionary, recursively format it
            formatted = '{\n'
            for k, v in value.items():
                formatted += f"{indent}    {k} = {format_value(v, indent_level + 1)}\n"
            formatted += f"{indent}}}"
            return formatted
        elif isinstance(value, list):
            # If the value is a list, output it inside braces with items separated by spaces
            return '{ ' + ' '.join(f'"{item}"' for item in value) + ' }'
        elif isinstance(value, str):
            # If the value is a string, output it inside quotes
            return f'"{value}"'
        else:
            # For numeric values, just return the value
            return str(value)

    with open(file_path, 'w', encoding='utf-8') as file:
        for state in results:
            # Print the state name and opening brace
            file.write(f"STATE_{state['state_name']} = {{\n")
            
            # Loop over each key in the state dictionary (excluding 'state_name')
            for key, value in state.items():
                if key != 'state_name':
                    file.write(f"    {key} = {format_value(value, 1)}\n")
            
            # Close the state's block
            file.write("}\n\n")


def merge_states(states, merge_group):
    def log_removal(removed_items, key, A, B):
        for item in removed_items:
            print(f"{item} is removed due to duplication when merging {B} into {A} for key {key}")

    def merge_provinces_or_list(A, B, key):
        # Pool the values of A and B, remove duplicates, and sort in descending order
        merged_values = list(set(A.get(key, []) + B.get(key, [])))
        removed_values = list(set(A.get(key, [])) & set(B.get(key, [])))  # Duplicates
        merged_values.sort(reverse=True)
        
        # Log duplicate removals
        if removed_values:
            log_removal(removed_values, key, A['state_name'], B['state_name'])
        
        A[key] = merged_values

    def merge_capped_resources(A, B):
        # Merge the capped_resources by summing values for duplicate sub-keys
        capped_A = A.get('capped_resources', {})
        capped_B = B.get('capped_resources', {})
        
        for sub_key, sub_value_B in capped_B.items():
            if sub_key in capped_A:
                capped_A[sub_key] += sub_value_B  # Sum if duplicated
            else:
                capped_A[sub_key] = sub_value_B  # Copy if unique
            
        A['capped_resources'] = capped_A

    # Merge the states in the group
    base_state = merge_group[0]
    for state_name in merge_group[1:]:
        # A is the base state and B is the state to be merged into A
        A = states[base_state]
        B = states[state_name]
        
        # Merge provinces and lists
        merge_provinces_or_list(A, B, 'provinces')
        merge_provinces_or_list(A, B, 'arable_resources')
        merge_provinces_or_list(A, B, 'traits')
        merge_provinces_or_list(A, B, 'impassable')
        merge_provinces_or_list(A, B, 'prime_land')
        
        # Sum arable_land values
        A['arable_land'] = A.get('arable_land', 0) + B.get('arable_land', 0)
        
        # Merge capped_resources
        merge_capped_resources(A, B)
        
        # Copy other unique keys from B to A
        for key, value_B in B.items():
            if key not in A and key != 'state_name':  # Avoid copying state_name again
                A[key] = value_B
        
        # After merging B into A, remove B from the states dictionary
        del states[state_name]

    return states


# Example usage of the function for processing multiple files in a folder
merge_list_file = "C:/Users/peng_/Documents/Paradox Interactive/Victoria 3/mod/tmp/state_merge_list.txt"
input_folder = "C:/Users/peng_/Documents/Paradox Interactive/Victoria 3/mod/tmp/t3/"
output_folder = "C:/Users/peng_/Documents/Paradox Interactive/Victoria 3/mod/tmp/t2/"

# List all .txt files in the input folder
for file_name in os.listdir(input_folder):
    if file_name.endswith(".txt"):
        file_path = os.path.join(input_folder, file_name)
        output_file_path = os.path.join(output_folder, file_name)
        
        print(f"Processing file: {file_path}")

        # Read and parse the states
        blocks = read_state(file_path)
        results = [parse_block(block) for block in blocks]

        # Convert results list into a dictionary where keys are state names for easy lookup
        states = {f"STATE_{state['state_name']}": state for state in results}

        # Check if the file contains states that need to be merged
        with open(merge_list_file, 'r', encoding='utf-8-sig') as f:
            merge_groups = [line.strip().split() for line in f.readlines()]

        merge_required = False

        # Filter only the relevant merge groups (states in the current file)
        relevant_merge_groups = [group for group in merge_groups if all(state in states for state in group)]

        if relevant_merge_groups:
            merge_required = True
            for group in relevant_merge_groups:
                print(f"Found complete merge group in {file_path}: {group}")
                
                # Merge the states according to the filtered group
                merged_states = merge_states(states, group)  # Pass only the relevant group
                
                # Write the merged states to the output folder
                # Convert merged_states back to a list of state dictionaries
                write_results_to_file(list(merged_states.values()), output_file_path)
        else:
            print(f"No merge required for file: {file_path}")

print("Processing complete.")
