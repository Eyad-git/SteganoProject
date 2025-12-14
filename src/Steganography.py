from src import utils

# The secret marker that tells us where the message ends
DELIMITER = "$t3g0"

def encode(pixel_data, message):
    """
    Hides a text message into the pixel bytes using LSB.
    """
    # 1. Add the delimiter so we know when to stop decoding later
    full_message = message + DELIMITER
    
    # 2. Convert to binary bits
    binary_message = utils.text_to_bits(full_message)
    
    # 3. Check Capacity
    # We need 1 byte of image data for every 1 bit of message
    if len(binary_message) > len(pixel_data):
        raise ValueError(f"Message is too long! Image has {len(pixel_data)} bytes, but message needs {len(binary_message)} bytes.")
    
    # 4. Hide the bits
    encoded_pixels = pixel_data.copy()
    
    for i in range(len(binary_message)):
        bit = int(binary_message[i])
        
        # Clear the last bit (LSB) of the byte using AND 254 (11111110)
        # Then set it to our message bit using OR
        encoded_pixels[i] = (encoded_pixels[i] & 254) | bit
        
    return encoded_pixels

def decode(pixel_data):
    """
    Extracts the text message from the pixel bytes.
    """
    binary_string = ""
    
    # 1. Loop through pixels and extract bits
    for byte in pixel_data:
        # Get the LSB (byte AND 1)
        binary_string += str(byte & 1)
        
        # 2. Check for delimiter every 8 bits (every character)
        if len(binary_string) % 8 == 0:
            # Convert current binary to text to check if we found the end
            current_text = utils.bits_to_text(binary_string)
            
            # If the text ends with our delimiter, stop!
            if current_text.endswith(DELIMITER):
                # Return the text WITHOUT the delimiter
                return current_text[:-len(DELIMITER)]
    
    # If we run out of pixels without finding the delimiter
    return "No hidden message found (Delimiter missing)."