from src import bmp_manager
from src import Steganography
from src import cipher

def print_menu():
    print("\n" + "="*50)
    print("      STEGANOGRAPHY PRO (Emoji Support)")
    print("="*50)
    print("1. Encode (Hide a Message)")
    print("2. Decode (Read a Message)")
    print("3. Exit")
    print("="*50)

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
        choice = input("\nType message (T) or Read file (F)? [T/F]: ").strip().upper()
        if choice == 'T':
            msg = input("Enter the secret message: ")
            if msg: return msg
            print("Message cannot be empty.")
        elif choice == 'F':
            path = input("Enter file path: ")
            try:
                # 'rb' is safer for files, but 'r' utf-8 is fine for text
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if content: 
                        print(f"Loaded {len(content)} chars.")
                        return content
                    print("File is empty.")
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("Invalid choice.")

def handle_encode():
    print("\n--- ENCODE MODE ---")
    input_path, header, pixels = get_valid_image()
    
    # Get Message (String with Emojis)
    message = get_message_input()

    # Get Password
    password = input("Enter Password: ")

    # 1. Encrypt (Output is BYTES)
    if password:
        print("Encrypting...")
        # Convert string to bytes automatically inside cipher
        payload_bytes = cipher.vigenere_encrypt(message, password)
    else:
        # Convert string to bytes (UTF-8) manually if no encryption
        payload_bytes = message.encode('utf-8')

    # 2. Embed
    print("Scattering bits...")
    try:
        new_pixels = Steganography.encode(pixels, payload_bytes, password)
        
        while True:
            output_path = input("Enter output filename: ")
            output_path = ensure_bmp_extension(output_path)
            if bmp_manager.save_bmp(output_path, header, new_pixels):
                print(f"SUCCESS! Saved to '{output_path}'.")
                break
            else:
                print("Write failed.")
    except ValueError as e:
        print(f"[ERROR] {e}")

def handle_decode():
    print("\n--- DECODE MODE ---")
    input_path, header, pixels = get_valid_image()
    
    password = input("Enter Password: ")
    
    print("Extracting...")
    try:
        # Returns BYTES
        extracted_bytes = Steganography.decode(pixels, password)
        
        if extracted_bytes is None:
            print("[ERROR] Decoding failed. Wrong password or invalid image.")
            return

        # Decrypt (Takes BYTES -> Returns BYTES)
        if password:
            print("Decrypting...")
            final_bytes = cipher.vigenere_decrypt(extracted_bytes, password)
        else:
            final_bytes = extracted_bytes
            
        # Final Step: Convert Bytes -> Text (UTF-8) to show Emojis
        try:
            final_message = final_bytes.decode('utf-8')
            print("\n" + "-"*30)
            print(f"RESULT: {final_message}")
            print("-"*30)
        except UnicodeDecodeError:
            print("\n[WARNING] Message extracted, but it contains binary data (not text).")
            print(f"Raw Bytes: {final_bytes}")

    except Exception as e:
        print(f"Error: {e}")

def main():
    while True:
        print_menu()
        choice = input("Enter your choice (1-3): ")
        if choice == '1': handle_encode()
        elif choice == '2': handle_decode()
        elif choice == '3': break
        else: print("Invalid choice.")

if __name__ == "__main__":
    main()