import os
import re

# Define folder paths
input_folder = "C:/Users/peng_/Documents/Paradox Interactive/Victoria 3/mod/2410_vic3_vanila/map_data/t1"
output_folder = "C:/Users/peng_/Documents/Paradox Interactive/Victoria 3/mod/2410_vic3_vanila/map_data/t2"

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Regex patterns to detect state blocks, key-value pairs, and nested structures
state_block_pattern = re.compile(r'(STATE_\w+)\s*=\s*\{([^}]*)\}', re.DOTALL)  # Match each state block
key_value_pattern = re.compile(r'(\w+)\s*=')
nested_block_pattern = re.compile(r'(\w+)\s*=\s*\{')

# Function to parse and log all keys including nested ones within a state block
def parse_and_log_keys(state_name, state_content):
    lines = state_content.splitlines()
    nested_stack = []
    current_level = 0

    print(f"Parsing state: {state_name}")

    for line in lines:
        # Check for opening of a nested block (e.g., capped_resources = { )
        nested_match = nested_block_pattern.match(line)
        if nested_match:
            key = nested_match.group(1)
            print(f"{'  ' * current_level}Detected nested key: {key}")
            nested_stack.append(key)
            current_level += 1
            continue

        # Check for closing of a nested block (i.e., a closing brace `}`)
        if line.strip() == "}":
            if nested_stack:
                closed_key = nested_stack.pop()
                current_level -= 1
                print(f"{'  ' * current_level}Closed nested key: {closed_key}")
            continue

        # Detect key-value pairs (e.g., `id = 478`)
        key_value_match = key_value_pattern.match(line)
        if key_value_match:
            key = key_value_match.group(1)
            print(f"{'  ' * current_level}Detected key: {key}")

    print()  # Print a blank line for readability

# Function to detect the newline format used in the original file
def detect_newline_format(file_path):
    with open(file_path, 'rb') as f:
        content = f.read()
        if b'\r\n' in content:
            return '\r\n'  # Windows format
        else:
            return '\n'  # Linux/Unix format

# Function to process a file with multiple states and log detected keys
def process_state_file(file_content, filename):
    print(f"Processing file: {filename}\n")

    # Find all state blocks in the file (e.g., `STATE_DZUNGARIA = { ... }`)
    state_blocks = state_block_pattern.findall(file_content)

    if not state_blocks:
        print(f"Warning: No valid state blocks found in {filename}")
        return

    # Process each state block separately
    for state_name, state_content in state_blocks:
        parse_and_log_keys(state_name, state_content)

# Function to copy the input files to the output folder with the same filename and newline format
def copy_files_and_log_keys(input_folder, output_folder):
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            input_file_path = os.path.join(input_folder, filename)
            output_file_path = os.path.join(output_folder, filename)

            # Detect the newline format of the original file
            newline_format = detect_newline_format(input_file_path)

            # Read the input file
            try:
                with open(input_file_path, 'r', encoding='utf-8-sig', newline='') as input_file:
                    file_content = input_file.read()
                    # Print a message when successfully reading a file
                    print(f"Successfully read state file: {filename}")

                # Process and log all keys for multiple states in the file
                process_state_file(file_content, filename)

                # Write the content to the output file with the same filename and newline format
                with open(output_file_path, 'w', encoding='utf-8-sig', newline=newline_format) as output_file:
                    output_file.write(file_content)

                print(f"Successfully wrote state file: {filename}\n")

            except Exception as e:
                print(f"Error processing {filename}: {e}")

# Main execution to copy the files and log detected keys for multiple states
copy_files_and_log_keys(input_folder, output_folder)
