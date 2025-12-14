def to_binary(data):
    """
    Converts input (String or Bytes) into a string of bits.
    Handles Emojis automatically by encoding to UTF-8 bytes first.
    """
    if isinstance(data, str):
        # Convert text/emojis to raw bytes (UTF-8)
        data = data.encode('utf-8')
    
    # Convert every byte to 8 bits
    return "".join(format(b, '08b') for b in data)

def from_binary(binary_string):
    """
    Converts binary string back into raw bytes.
    (We do not decode to text here yet, because the bytes might be encrypted!)
    """
    byte_array = bytearray()
    for i in range(0, len(binary_string), 8):
        # Slice 8 bits
        byte_chunk = binary_string[i:i+8]
        if len(byte_chunk) < 8:
            break
        # Convert to integer byte
        byte_array.append(int(byte_chunk, 2))
        
    return bytes(byte_array)