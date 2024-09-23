import os
import re

# Function to read the state merge list and create a dictionary for replacements
def read_merge_list(merge_list_file):
    print(f"Attempting to read the merge list from: {merge_list_file}")
    replacements = {}
    try:
        with open(merge_list_file, 'r', encoding='utf-8-sig') as f:
            for line in f:
                states = line.strip().split()
                if len(states) > 1:
                    base_state = states[0]
                    for state in states[1:]:
                        replacements[state] = base_state
                        print(f"Mapping: Replace {state} with {base_state}")
        print(f"Total replacements loaded: {len(replacements)}")
    except FileNotFoundError:
        print(f"ERROR: Merge list file '{merge_list_file}' not found.")
    except Exception as e:
        print(f"ERROR reading merge list: {e}")
    return replacements

# Function to process and replace state names in the content
def replace_states_in_file(file_content, replacements):
    pattern = re.compile(r"STATE_\w+")  # Regular expression to match STATE_XXX
    def replace_match(match):
        state_name = match.group(0)
        new_state = replacements.get(state_name, state_name)  # Replace if found
        if new_state != state_name:
            print(f"Replacing {state_name} with {new_state}")
        return new_state
    return pattern.sub(replace_match, file_content)

# Function to process all files in a folder
def process_files(input_folder, output_folder, replacements):
    print(f"Processing files in folder: {input_folder}")
    if not os.path.exists(input_folder):
        print(f"ERROR: Input folder '{input_folder}' not found.")
        return

    os.makedirs(output_folder, exist_ok=True)  # Ensure output folder exists

    found_files = False  # Track if any .txt files are found
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.txt'):
            found_files = True
            input_file_path = os.path.join(input_folder, file_name)
            output_file_path = os.path.join(output_folder, file_name)

            print(f"Processing file: {input_file_path}")
            try:
                with open(input_file_path, 'r', encoding='utf-8-sig') as f:
                    file_content = f.read()
            except Exception as e:
                print(f"ERROR reading file '{input_file_path}': {e}")
                continue

            # Replace states in the file content
            updated_content = replace_states_in_file(file_content, replacements)

            # Save the modified content to the output folder
            try:
                with open(output_file_path, 'w', encoding='utf-8-sig') as f:
                    f.write(updated_content)
                print(f"File saved: {output_file_path}")
            except Exception as e:
                print(f"ERROR writing file '{output_file_path}': {e}")

    if not found_files:
        print(f"No .txt files found in folder: {input_folder}")

# Main function
def main():
    print("Starting script...")

    merge_list_file = "C:/Users/peng_/Documents/Paradox Interactive/Victoria 3/mod/tmp/state_merge_list.txt"
    input_folder = "C:/Users/peng_/Documents/Paradox Interactive/Victoria 3/mod/2410_vic3_vanila/common/history/pops"
    output_folder = "C:/Users/peng_/Documents/Paradox Interactive/Victoria 3/mod/tmp/t1"
  
    print("Reading merge list...")
    replacements = read_merge_list(merge_list_file)
    
    print("Processing files...")
    process_files(input_folder, output_folder, replacements)

    print("Script complete.")

# Execute the main function
if __name__ == "__main__":
    main()
