#utility functions for the tool
"""
utils.py

This module contains helper functions for converting data between
text (string) and binary (bitstream) formats.
"""

def text_to_bits(text):
    """
    Converts a text string into a string of bits (0s and 1s).
    
    Args:
        text (str): The secret message to encode.
        
    Returns:
        str: A string of bits (e.g., "01000001" for 'A').
    """
    # 1. Iterate over each character in the text.
    # 2. ord(char) gets the ASCII integer value.
    # 3. format(value, '08b') converts it to an 8-bit binary string.
    # 4. join combines them all into one long string.
    bits = ''.join(format(ord(char), '08b') for char in text)
    return bits

def bits_to_text(bits):
    """
    Converts a string of bits (0s and 1s) back into text.
    
    Args:
        bits (str): The bitstream to decode.
        
    Returns:
        str: The reconstructed text message.
    """
    chars = []
    
    # Iterate over the bitstring in chunks of 8 (since 1 char = 8 bits)
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        
        # Only process if we have a full 8-bit byte
        if len(byte) == 8:
            # int(byte, 2) converts binary string to integer
            # chr(val) converts integer to character
            chars.append(chr(int(byte, 2)))
            
    return ''.join(chars)