from src import utils
from src import prng

def encode(pixel_data, message_data, password=""):
    """
    Hides data (String or Bytes) into pixels.
    """
    # 1. Prepare Payload: [32-bit Length] + [Data Bits]
    # utils.to_binary handles strings AND bytes (emojis safe)
    message_bits = utils.to_binary(message_data)
    
    length_val = len(message_bits)
    length_bits = format(length_val, '032b') 
    
    full_payload_bits = length_bits + message_bits
    total_bits_needed = len(full_payload_bits)
    total_pixels = len(pixel_data)

    # 2. Capacity Check
    if total_bits_needed > total_pixels:
        raise ValueError(f"Image too small. Need {total_bits_needed} pixels, have {total_pixels}.")

    # 3. Fast Scatter Generator
    scatter_gen = prng.StepGenerator(password, total_pixels)

    # 4. Embed Data
    encoded_pixels = pixel_data.copy()
    
    for i in range(total_bits_needed):
        bit = int(full_payload_bits[i])
        target_pixel_index = scatter_gen.get_index(i)
        encoded_pixels[target_pixel_index] = (encoded_pixels[target_pixel_index] & 254) | bit
        
    return encoded_pixels

def decode(pixel_data, password=""):
    """
    Extracts raw bytes from pixels.
    """
    total_pixels = len(pixel_data)
    scatter_gen = prng.StepGenerator(password, total_pixels)
    
    # 1. Extract Length
    length_bits = ""
    for i in range(32):
        target_pixel_index = scatter_gen.get_index(i)
        bit = pixel_data[target_pixel_index] & 1
        length_bits += str(bit)
        
    message_length = int(length_bits, 2)
    
    # Sanity Check
    if message_length > total_pixels or message_length < 0:
        return None # Signal failure

    # 2. Extract Body
    message_bits = ""
    for i in range(32, 32 + message_length):
        target_pixel_index = scatter_gen.get_index(i)
        bit = pixel_data[target_pixel_index] & 1
        message_bits += str(bit)
        
    # Return raw bytes (utils.from_binary returns bytes now)
    return utils.from_binary(message_bits)