def text_to_bits(text):
    """
    Converts a string of text into a string of bits (0s and 1s).
    Validates that characters are within the 8-bit range (0-255).
    """
    binary_string = ""
    for char in text:
        if ord(char) > 255:
            # Side Case Handled: Non-supported character
            raise ValueError(f"Character '{char}' is not supported. Only standard text (ASCII/Latin-1) is allowed.")
            
        binary_char = format(ord(char), '08b')
        binary_string += binary_char
    return binary_string

def bits_to_text(binary_string):
    """
    Converts a string of bits (0s and 1s) back into text.
    """
    text_string = ""
    for i in range(0, len(binary_string), 8):
        byte = binary_string[i:i+8]
        
        # Side Case Handled: Incomplete byte at the end
        if len(byte) < 8:
            break
            
        char_code = int(byte, 2)
        text_string += chr(char_code)
    return text_string