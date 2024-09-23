# paradox_text_utils.py
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 12:59:27 2024

@author: peng_

This is a group of functions to manuplate paradox files
"""
import re

def remove_comments_and_newlines(file_path):
    """
    Reads a text file, removes comments (starting with '#' and everything after it on the same line),
    and replaces newlines with spaces.

    Args:
        file_path (str): The path to the input text file.

    Returns:
        str: The processed text with comments removed and newlines replaced with spaces.
    """
    processed_lines = []
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        for line in file:
            # Remove comments (everything after '#')
            line_without_comment = line.split('#', 1)[0]
            # Strip leading and trailing whitespace
            line_without_comment = line_without_comment.strip()
            if line_without_comment:
                processed_lines.append(line_without_comment)
    # Replace newlines with spaces
    processed_text = ' '.join(processed_lines)
    return processed_text

def tokenize(text):
    """
    Splits the text into words and special tokens {, }, = using regular expressions.

    Args:
        text (str): The text to tokenize.

    Returns:
        list: A list of tokens.
    """
    # Split the text while keeping {, }, = as separate tokens
    token_pattern = r'([{}=])|\S+'
    
    # Find all tokens based on the pattern
    tokens = re.findall(token_pattern, text)
    
    # Flatten the list of tuples returned by re.findall
    tokens = [token for group in tokens for token in group if token]
    
    return tokens

def parse_tokens(tokens, index=0):
    """
    Recursively parses tokens starting from index.

    Args:
        tokens (list): The list of tokens.
        index (int): The current index in the tokens list.

    Returns:
        tuple: A tuple containing the parsed data and the new index.
    """
    data = {}
    keys_order = []
    while index < len(tokens):
        token = tokens[index]
        
        if token == '}':
            index += 1
            break
        
        elif token == '{':
            raise ValueError(f"Unexpected '{{' at position {index}")
        
        elif token == '=':
            raise ValueError(f"Unexpected '=' at position {index}")
        
        else:
            # We have a key
            key = token
            index += 1  # Move to the next token
            
            if index < len(tokens) and tokens[index] == '=':
                # It's a key-value pair
                index += 1  # Skip '='
                if index < len(tokens):
                    value_token = tokens[index]
                    if value_token == '{':
                        index += 1  # Skip '{'
                        # Check if the block contains '='
                        has_equals = any(t == '=' for t in tokens[index:tokens.index('}', index)])
                        
                        if has_equals:
                            # Parse as a nested block (i.e., key-value pairs)
                            value, index = parse_tokens(tokens, index)
                        else:
                            # Parse as a list of values
                            value = []
                            while tokens[index] != '}':
                                value.append(tokens[index].strip('"'))
                                index += 1
                            index += 1  # Skip '}'
                    else:
                        # It's a single value
                        value = value_token.strip('"')
                        index += 1
                    keys_order.append((key, value))
            else:
                # It's a list item
                keys_order.append((key, None))
    
    return {'__pairs__': keys_order}, index


def parse_text(text):
    """
    Parses the processed text into a nested data structure.

    Args:
        text (str): The processed text to parse.

    Returns:
        dict: The parsed data structure.
    """
    tokens = tokenize(text)
    parsed_data, _ = parse_tokens(tokens)
    return parsed_data


def dict_to_text(data, filename, indent=0):
    """
    Converts the data structure back into text format and writes it to a file.

    Args:
        data (dict or list): The parsed data structure.
        filename (str): The name of the file to write the data to.
        indent (int): The current level of indentation (used for nested structures).

    Returns:
        None: Writes directly to the file.
    """
    indent_str = '\t' * indent  # Use tabs for indentation
    result = []
    
    # Check if data is a dictionary
    if isinstance(data, dict):
        pairs = data.get('__pairs__', [])
        for key, value in pairs:
            # If value is a list (e.g., owned_provinces)
            if isinstance(value, list):
                result.append(f"{indent_str}{key} = {{")
                values_str = ' '.join(value)  # Join all values in the list on a single line
                result.append(f"{indent_str}\t{values_str}")
                result.append(f"{indent_str}}}")
            # If value is another nested dictionary
            elif isinstance(value, dict):
                result.append(f"{indent_str}{key} = {{")
                result.append(dict_to_text_string(value, indent + 1))
                result.append(f"{indent_str}}}")
            # If value is a simple key-value pair
            else:
                result.append(f"{indent_str}{key} = {value}")
    
    # Check if data is a list (for handling blocks of items)
    elif isinstance(data, list):
        values_str = ' '.join(data)
        result.append(f"{indent_str}{values_str}")
    
    with open(filename, 'w', encoding='utf-8-sig') as f:
        f.write('\n'.join(result))


def dict_to_text_string(data, indent=0):
    """
    Converts the data structure into a formatted text string.

    Args:
        data (dict or list): The parsed data structure.
        indent (int): The current level of indentation (used for nested structures).

    Returns:
        str: The formatted text as a string.
    """
    indent_str = '\t' * indent  # Use tabs for indentation
    result = []
    
    # Check if data is a dictionary
    if isinstance(data, dict):
        pairs = data.get('__pairs__', [])
        for key, value in pairs:
            # If value is a list (e.g., owned_provinces)
            if isinstance(value, list):
                result.append(f"{indent_str}{key} = {{")
                values_str = ' '.join(value)  # Join all values in the list on a single line
                result.append(f"{indent_str}\t{values_str}")
                result.append(f"{indent_str}}}")
            # If value is another nested dictionary
            elif isinstance(value, dict):
                result.append(f"{indent_str}{key} = {{")
                result.append(dict_to_text_string(value, indent + 1))
                result.append(f"{indent_str}}}")
            # If value is a simple key-value pair
            else:
                result.append(f"{indent_str}{key} = {value}")
    
    # Check if data is a list (for handling blocks of items)
    elif isinstance(data, list):
        values_str = ' '.join(data)
        result.append(f"{indent_str}{values_str}")
    
    return '\n'.join(result)

def collect_owned_provinces(data):
    """
    Recursively collects all values of 'owned_provinces' from different levels of a nested dictionary.
    Removes the quotes, validates each value, and sorts them.

    Args:
        data (dict or list): The nested dictionary or list to search.

    Returns:
        list: A sorted list of owned_provinces values.
    
    Raises:
        ValueError: If any element does not follow the 'xhhhhhh' format.
    """
    owned_provinces = []

    def validate_and_collect(values):
        """Helper function to validate and collect province values."""
        hex_pattern = re.compile(r'x[0-9A-F]{6}$')  # Regular expression for 'xhhhhhh' format
        
        for value in values:
            # Remove any surrounding quotes
            value = value.strip('"')
            # Validate the value format
            if not hex_pattern.match(value):
                raise ValueError(f"Invalid owned_province value: {value}")
            owned_provinces.append(value)

    # Recursive search function
    def search(data):
        if isinstance(data, dict):
            for key, value in data.get('__pairs__', []):
                if key == 'owned_provinces' and isinstance(value, list):
                    validate_and_collect(value)
                elif isinstance(value, dict):
                    search(value)
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    search(item)

    # Start the recursive search
    search(data)
    
    # Return the sorted list
    return sorted(owned_provinces)

def collect_owned_provinces(data):
    """
    Recursively collects all values of 'owned_provinces' from different levels of a nested dictionary.
    Removes the quotes, validates each value, and sorts them.

    Args:
        data (dict or list): The nested dictionary or list to search.

    Returns:
        list: A sorted list of owned_provinces values.
    
    Raises:
        ValueError: If any element does not follow the 'xhhhhhh' format with case-insensitive hex characters.
    """
    owned_provinces = []

    def validate_and_collect(values):
        """Helper function to validate and collect province values."""
        hex_pattern = re.compile(r'x[0-9a-fA-F]{6}$')  # Regular expression for 'xhhhhhh' format with case-insensitive hex
        
        for value in values:
            # Remove any surrounding quotes
            value = value.strip('"')