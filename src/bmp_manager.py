def read_bmp(file_path):
    """
    Reads a BMP file.
    Returns:
        header (bytes): The first 54 bytes (Standard BMP header).
        pixel_data (bytearray): The rest of the file (mutable pixel data).
    """
    try:
        with open(file_path, 'rb') as f:
            # The standard BMP header is 54 bytes. 
            # We must preserve this exactly so the image remains valid.
            header = f.read(54)
            
            # Read the rest of the file (the pixels)
            body = f.read()
            
            # Convert body to a bytearray so we can modify it later
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
    Saves a BMP file by combining the header and the pixel data.
    """
    try:
        with open(file_path, 'wb') as f:
            f.write(header)
            f.write(pixel_data)
        return True
    except Exception as e:
        print(f"Error saving file: {e}")
        return False