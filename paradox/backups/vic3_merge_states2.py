# -*- coding: utf-8 -*-
"""
Updated Parser using Regular Expressions

@author: peng_
"""

import re
import chardet  # You may need to install this package

def read_file(filepath):
    """Read the file and return its content."""
    with open(filepath, 'rb') as f:
        raw_data = f.read()
    # Detect encoding
    result = chardet.detect(raw_data)
    encoding = result['encoding']
    # Decode the content
    text = raw_data.decode(encoding)
    return text

def parse(text):
    """Parse the entire text and return the resulting data structure."""
    tokens = tokenize(text)
    data, _ = parse_tokens(tokens)
    return data

def tokenize(text):
    """Convert the text into a list of tokens."""
    # Remove comments
    text = re.sub(r'#.*', '', text)
    # Token patterns
    token_pattern = r'''
        ".*?"           |  # Quoted strings
        [\{\}]          |  # Braces
        =               |  # Equals
        \S+               # Other non-whitespace sequences
    '''
    tokens = re.findall(token_pattern, text, re.VERBOSE | re.DOTALL)
    tokens = [token.strip() for token in tokens if token.strip()]
    return tokens

def parse_tokens(tokens, index=0):
    """Parse tokens starting from index."""
    data = {}
    items = []
    keys_order = []
    while index < len(tokens):
        token = tokens[index]
        if token == '}':
            index += 1
            break
        elif token == '{':
            # Should not encounter '{' here without a key
            raise ValueError(f"Unexpected '{{' at position {index}")
        elif token == '=':
            # Should not encounter '=' without a key
            raise ValueError(f"Unexpected '=' at position {index}")
        else:
            # Next token should be '=' or '{' or another key/value
            if index + 1 < len(tokens) and tokens[index + 1] == '=':
                key = token
                index += 2  # Skip key and '='
                value, index = parse_value(tokens, index)
                keys_order.append((key, value))
            else:
                # It's an item in a list
                items.append(token)
                index += 1
    if items and not keys_order:
        return items, index
    else:
        return {'__pairs__': keys_order, '__items__': items}, index

def parse_value(tokens, index):
    """Parse a value starting from index."""
    token = tokens[index]
    if token == '{':
        index += 1  # Skip '{'
        value, index = parse_tokens(tokens, index)
        return value, index
    else:
        # Single value
        index += 1
        # Remove quotes if present
        value = token.strip('"')
        return value, index

def dict_to_text(data, indent=0):
    """Convert the data structure back into text format."""
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

# Main execution
if __name__ == "__main__":
    # File paths
    input_file = 'C:/Users/peng_/Documents/Paradox Interactive/Victoria 3/mod/2410_vic3_vanila/common/history/states/00_states.txt'
    output_file = 'C:/Users/peng_/Documents/Paradox Interactive/Victoria 3/mod/2410_vic3_vanila/common/history/states/01_states.txt'

    # Read the text file
    text_content = read_file(input_file)

    # Parse the text content
    parsed_data = parse(text_content)

    # Clean the 'owned_provinces' values
    clean_owned_provinces_values(parsed_data)

    # Convert the dictionary back to text
    text_output = dict_to_text(parsed_data)

    # Write the text output to a file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(text_output)
