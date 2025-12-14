def read_bmp(file_path):
    """
    Reads a BMP file.
    Dynamically finds the pixel data start to support 24-bit and 32-bit files.
    Returns: (header, pixel_data) or (None, None)
    """
    try:
        with open(file_path, 'rb') as f:
            # 1. Check for 'BM' signature
            tag = f.read(2)
            if tag != b'BM':
                print(f"Error: '{file_path}' is not a valid BMP file (Missing 'BM' tag).")
                return None, None
            
            # 2. Read the Pixel Offset (The location where image data actually starts)
            # The offset is stored at byte 10, and it is 4 bytes long.
            f.seek(10)
            offset_bytes = f.read(4)
            pixel_offset = int.from_bytes(offset_bytes, byteorder='little')
            
            # 3. Read the Header (Everything up to the pixel offset)
            f.seek(0)
            header = f.read(pixel_offset)
            
            # 4. Read the Body (Everything after the header)
            body = f.read()
            pixel_data = bytearray(body)
            
            return header, pixel_data
            
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None, None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None, None

def save_bmp(file_path, header, pixel_data):
    """
    Saves a BMP file.
    """
    try:
        with open(file_path, 'wb') as f:
            f.write(header)
            f.write(pixel_data)
        return True
    except Exception as e:
        print(f"Error saving file: {e}")
        return False