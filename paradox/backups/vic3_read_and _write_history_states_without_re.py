# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 11:47:58 2024

@author: peng_
"""

def skip_whitespace_and_comments(text, index):
    """Skip over whitespace and comments starting with '#'."""
    length = len(text)
    while index < length:
        c = text[index]
        if c in ' \t\n\r':
            index += 1
        elif c == '#':
            # Skip to end of line
            while index < length and text[index] != '\n':
                index += 1
        else:
            break
    return index

def parse_word(text, index):
    """Parse a word starting at index, handling quoted strings."""
    index = skip_whitespace_and_comments(text, index)
    length = len(text)
    if index >= length:
        return '', index
    c = text[index]
    if c == '"':
        # Parse a quoted string
        index += 1  # skip opening quote
        start = index
        while index < length and text[index] != '"':
            index += 1
        word = text[start:index]
        index += 1  # skip closing quote
    else:
        # Parse an unquoted word
        start = index
        while index < length:
            c = text[index]
            if c in ' \t\n\r={}':
                break
            else:
                index += 1
        word = text[start:index]
    return word, index

def parse_value(text, index):
    """Parse a value starting at index."""
    index = skip_whitespace_and_comments(text, index)
    length = len(text)
    if index >= length:
        return None, index
    c = text[index]
    if c == '{':
        # Parse everything inside the braces
        index += 1  # skip '{'
        value, index = parse_block(text, index)
        return value, index
    else:
        # Parse the next word as the value
        value, index = parse_word(text, index)
        return value, index

def parse_block(text, index):
    """Parse a block starting at index."""
    items = []
    keys_order = []  # To maintain the order and handle multiple keys
    length = len(text)
    while index < length:
        index = skip_whitespace_and_comments(text, index)
        if index >= length:
            break
        c = text[index]
        if c == '}':
            index += 1  # consume '}'
            break
        # Parse word
        word, index = parse_word(text, index)
        index = skip_whitespace_and_comments(text, index)
        if index < length and text[index] == '=':
            # It's a key-value pair
            index += 1  # skip '='
            # Parse value
            value, index = parse_value(text, index)
            # Store key and value
            keys_order.append((word, value))
        else:
            # It's a word in a list
            items.append(word)
    # Return both the result dict and the list of key-value pairs
    if items and not keys_order:
        # Only items in the block
        return items, index
    else:
        # Return the key-value pairs and items
        return {'__pairs__': keys_order, '__items__': items}, index

def parse(text):
    """Parse the entire text and return the resulting dictionary."""
    index = 0
    result, index = parse_block(text, index)
    return result

def dict_to_text(data, indent=0):
    """Convert the dictionary back into text format."""
    indent_str = '\t' * indent
    result = []
    if isinstance(data, dict):
        items = data.get('__items__', [])
        pairs = data.get('__pairs__', [])
        # Output items in the list
        for item in items:
            result.append(f"{indent_str}{item}")
        # Output key-value pairs in order
        for key, value in pairs:
            if isinstance(value, dict) or isinstance(value, list):
                if key == 'owned_provinces' and isinstance(value, list):
                    # For 'owned_provinces', output the list items on one line
                    items_str = ' '.join(value)
                    result.append(f"{indent_str}{key} = {{ {items_str} }}")
                else:
                    result.append(f"{indent_str}{key} = {{")
                    result.append(dict_to_text(value, indent + 1))
                    result.append(f"{indent_str}}}")
            else:
                result.append(f"{indent_str}{key} = {value}")
    elif isinstance(data, list):
        # Check if all items are strings
        if all(isinstance(item, str) for item in data):
            # Output the list on the same line within braces
            items_str = ' '.join(data)
            result.append(f"{indent_str}{items_str}")
        else:
            # Output each item
            for item in data:
                result.append(dict_to_text(item, indent))
    else:
        # Write single value
        result.append(f"{indent_str}{data}")
    return '\n'.join(result)

def clean_owned_provinces_values(data):
    """Recursively process the data to clean the values of 'owned_provinces' keys."""
    if isinstance(data, dict):
        items = data.get('__items__', [])
        pairs = data.get('__pairs__', [])
        # Process key-value pairs
        for idx, (key, value) in enumerate(pairs):
            if key == 'owned_provinces':
                # Clean the values in the list
                if isinstance(value, list):
                    new_value = []
                    for item in value:
                        # Remove quotes from the item if present
                        item = item.strip('"')
                        new_value.append(item)
                    pairs[idx] = (key, new_value)
                else:
                    # Handle case where value is a single string
                    item = value.strip('"')
                    pairs[idx] = (key, item)
            else:
                # Recursively process the value
                clean_owned_provinces_values(value)
    elif isinstance(data, list):
        for item in data:
            clean_owned_provinces_values(item)

# File paths
input_file = 'C:/Users/peng_/Documents/Paradox Interactive/Victoria 3/mod/2410_vic3_vanila/common/history/states/00_states.txt'
output_file = 'C:/Users/peng_/Documents/Paradox Interactive/Victoria 3/mod/2410_vic3_vanila/common/history/states/01_states.txt'

# Read the text file
with open(input_file, 'r', encoding='utf-8-sig') as file:
    text_content = file.read()

# Parse the text content
parsed_data = parse(text_content)

# Clean the 'owned_provinces' values
clean_owned_provinces_values(parsed_data)

# Convert the dictionary back to text
text_output = dict_to_text(parsed_data)

# Write the text output to a file
with open(output_file, 'w', encoding='utf-8-sig') as file:
    file.write(text_output)
