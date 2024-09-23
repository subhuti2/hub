import os
import re

# Define folder paths
input_folder = "C:/Users/peng_/Documents/Paradox Interactive/Victoria 3/mod/tmp/t3"
output_folder = "C:/Users/peng_/Documents/Paradox Interactive/Victoria 3/mod/tmp/t1"
to_be_merge_file = "C:/Users/peng_/Documents/Paradox Interactive/Victoria 3/mod/tmp/state_merge_list.txt"

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Regex patterns to detect state blocks, key-value pairs, and nested structures
state_block_pattern = re.compile(r'(STATE_\w+)\s*=\s*\{([^}]*)\}', re.DOTALL)
key_value_pattern = re.compile(r'(\w+)\s*=')

# Function to read the merge list from the to_be_merge file
def read_merge_list(to_be_merge_file):
    merge_map = {}
    with open(to_be_merge_file, 'r', encoding='utf-8-sig') as f:
        for line in f:
            states = line.strip().split()
            if len(states) > 1:
                main_state = states[0]
                merge_map[main_state] = states[1:]  # All states that will be merged into the first one
    return merge_map

# Function to merge states within a file content based on the merge list
def merge_states(file_content, merge_map):
    modified_content = file_content
    state_blocks = state_block_pattern.findall(file_content)

    merged_states_info = []  # To keep track of which states were merged

    # For each state block, check if it is in the merge map
    for main_state, state_content in state_blocks:
        # If the state is the target of a merge
        if main_state in merge_map:
            states_to_merge = merge_map[main_state]
            merged_states_info.append(f"states {', '.join(states_to_merge)} are merged into state {main_state}")

            # Merge logic: append content of states_to_merge into main_state's block (for simplicity, we just add their content)
            for state_to_merge in states_to_merge:
                merge_block_pattern = re.compile(rf'({state_to_merge})\s*=\s*\{{([^}}]*)\}}', re.DOTALL)
                merge_block = merge_block_pattern.search(file_content)
                if merge_block:
                    # Add the content of state_to_merge into main_state
                    state_content += "\n" + merge_block.group(2)

                    # Remove the merged state from the file content
                    modified_content = re.sub(merge_block_pattern, '', modified_content)

            # Replace the main state block with the updated content (merged)
            main_block_pattern = re.compile(rf'({main_state})\s*=\s*\{{([^}}]*)\}}', re.DOTALL)
            modified_content = re.sub(main_block_pattern, f'{main_state} = {{{state_content}}}', modified_content)

    return modified_content, merged_states_info

# Function to process files and merge states if needed
def process_files(input_folder, output_folder, merge_map):
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            input_file_path = os.path.join(input_folder, filename)
            output_file_path = os.path.join(output_folder, filename)

            # Read the input file
            with open(input_file_path, 'r', encoding='utf-8-sig') as input_file:
                file_content = input_file.read()

            # Merge states if applicable
            modified_content, merged_states_info = merge_states(file_content, merge_map)

            # Write the modified content to the output file
            with open(output_file_path, 'w', encoding='utf-8-sig') as output_file:
                output_file.write(modified_content)

            # Output merged states information
            if merged_states_info:
                print(f"Process file: {filename}:")
                for info in merged_states_info:
                    print(info)

# Main execution
merge_map = read_merge_list(to_be_merge_file)
process_files(input_folder, output_folder, merge_map)
