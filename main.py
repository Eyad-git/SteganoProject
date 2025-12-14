from src import bmp_manager
from src import Steganography

def print_menu():
    print("\n" + "="*40)
    print("      STEGANOGRAPHY MVP v1.1")
    print("="*40)
    print("1. Encode (Hide a Message)")
    print("2. Decode (Read a Message)")
    print("3. Exit")
    print("="*40)

def ensure_bmp_extension(filename):
    """
    Checks if the filename ends with .bmp. If not, adds it.
    """
    if not filename.lower().endswith('.bmp'):
        return filename + ".bmp"
    return filename

def get_valid_image():
    """
    Loops until the user enters a valid BMP filename that exists
    and can be read. Returns the path, header, and pixels.
    """
    while True:
        filename = input("Enter the BMP image filename: ")
        
        # 1. Auto-fix extension
        filename = ensure_bmp_extension(filename)
        
        # 2. Try to read the file
        print(f"Checking '{filename}'...")
        header, pixels = bmp_manager.read_bmp(filename)
        
        # 3. Validation
        if pixels is not None:
            return filename, header, pixels
        else:
            print("Please try again (or press Ctrl+C to force quit).\n")

def get_message_input():
    """
    Asks the user to either type a message manually or provide a text file.
    Returns the message string.
    """
    while True:
        choice = input("\nDo you want to type the message (T) or read from a text file (F)? [T/F]: ").strip().upper()
        
        if choice == 'T':
            # Option A: Manual Input
            return input("Enter the secret message to hide: ")
            
        elif choice == 'F':
            # Option B: File Input (Robust Loop)
            while True:
                path = input("Enter the path to the text file (e.g., message.txt): ")
                try:
                    with open(path, 'r') as f:
                        content = f.read()
                        print(f"Loaded {len(content)} characters from '{path}'.")
                        return content
                except FileNotFoundError:
                    print(f"Error: The file '{path}' was not found. Try again.")
                except Exception as e:
                    print(f"Error reading file: {e}")
                    break # Break inner loop to let user choose T or F again if needed
        else:
            print("Invalid choice. Please enter 'T' or 'F'.")

def handle_encode():
    print("\n--- ENCODE MODE ---")
    
    # 1. Get Valid Image
    input_path, header, pixels = get_valid_image()
    
    # 2. Get Message (Dual Input Method)
    message = get_message_input()
    
    # 3. Get Output Path
    output_path = input("Enter the name for the output image: ")
    output_path = ensure_bmp_extension(output_path)

    # 4. Hide Message
    print("Hiding message...")
    try:
        new_pixels = Steganography.encode(pixels, message)
        
        # 5. Save Image
        if bmp_manager.save_bmp(output_path, header, new_pixels):
            print(f"SUCCESS! Secret message hidden in '{output_path}'.")
        else:
            print("Failed to save the new image.")
            
    except ValueError as e:
        print(f"Error: {e}")

def handle_decode():
    print("\n--- DECODE MODE ---")
    
    # 1. Get Valid Image
    input_path, header, pixels = get_valid_image()

    # 2. Extract Message
    print("Scanning for hidden message...")
    secret_message = Steganography.decode(pixels)
    
    print("\n" + "-"*20)
    print(f"RESULT: {secret_message}")
    print("-"*20)

def main():
    while True:
        print_menu()
        choice = input("Enter your choice (1-3): ")
        
        if choice == '1':
            handle_encode()
        elif choice == '2':
            handle_decode()
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()