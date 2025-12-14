from src import bmp_manager
from src import Steganography

# The delimiter used in steganography.py
DELIMITER = "$t3g0"

def print_menu():
    print("\n" + "="*40)
    print("      STEGANOGRAPHY MVP v1.3 (Final)")
    print("="*40)
    print("1. Encode (Hide a Message)")
    print("2. Decode (Read a Message)")
    print("3. Exit")
    print("="*40)

def ensure_bmp_extension(filename):
    if not filename.lower().endswith('.bmp'):
        return filename + ".bmp"
    return filename

def get_valid_image():
    while True:
        filename = input("Enter the BMP image filename: ")
        filename = ensure_bmp_extension(filename)
        
        print(f"Checking '{filename}'...")
        header, pixels = bmp_manager.read_bmp(filename)
        
        if pixels is not None:
            return filename, header, pixels
        else:
            print("Please try again.\n")

def get_message_input():
    while True:
        choice = input("\nDo you want to type the message (T) or read from a text file (F)? [T/F]: ").strip().upper()
        
        content = ""
        if choice == 'T':
            content = input("Enter the secret message to hide: ")
            
        elif choice == 'F':
            while True:
                path = input("Enter the path to the text file (e.g., message.txt): ")
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        print(f"Loaded {len(content)} characters.")
                        break # File read success
                except FileNotFoundError:
                    print(f"Error: File '{path}' not found.")
                except Exception as e:
                    print(f"Error reading file: {e}")
                    # Allow user to go back to T/F menu if stuck
                    break 
        else:
            print("Invalid choice.")
            continue # Skip validation below and restart loop

        # --- EDGE CASE CHECKS ---
        
        # 1. Empty Message Check
        if not content:
            print("Error: Message cannot be empty. Please try again.")
            continue
            
        # 2. Delimiter Conflict Check
        if DELIMITER in content:
            print(f"Error: Your message contains the restricted sequence '{DELIMITER}'.")
            print("This sequence is used internally as a separator. Please remove it from your message.")
            continue

        return content

def handle_encode():
    print("\n--- ENCODE MODE ---")
    
    # 1. Get Valid Image
    input_path, header, pixels = get_valid_image()
    
    # 2. Get Message (Loops until valid chars, no delimiter, not empty)
    while True:
        message = get_message_input()
        try:
            # Dry run to check if message contains non-ASCII characters
            from src import utils 
            utils.text_to_bits(message + DELIMITER) 
            break # Message is good!
        except ValueError as e:
            print(f"\n[INPUT ERROR]: {e}")
            print("Please enter a message without special symbols/emojis.")

    # 3. Save Output
    print("Hiding message...")
    try:
        new_pixels = Steganography.encode(pixels, message)
        
        while True:
            output_path = input("Enter the name for the output image: ")
            output_path = ensure_bmp_extension(output_path)
            
            if bmp_manager.save_bmp(output_path, header, new_pixels):
                print(f"SUCCESS! Secret message hidden in '{output_path}'.")
                break
            else:
                print(f"[WRITE ERROR]: Could not save to '{output_path}'. Check permissions or try a different name.")
            
    except ValueError as e:
        print(f"\n[CAPACITY ERROR]: {e}")
        print("Your message is too long for this image. Try a larger image or shorter message.")

def handle_decode():
    print("\n--- DECODE MODE ---")
    input_path, header, pixels = get_valid_image()

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
            print("Invalid choice.")

if __name__ == "__main__":
    main()