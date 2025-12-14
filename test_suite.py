from src import utils
from src import bmp_manager
from src import Steganography

def run_tests():
    print("=== STARTING PROJECT TESTS (MVP) ===\n")

    # --- Step 1: Utils ---
    print("--- Step 1: Utils Tests ---")
    if utils.text_to_bits("A") == "01000001":
        print("TEST 1.1: PASS")
    else:
        print("TEST 1.1: FAIL")

    if utils.bits_to_text("01000001") == "A":
        print("TEST 1.2: PASS")
    else:
        print("TEST 1.2: FAIL")
    print("-" * 30)

    # --- Step 2: BMP Manager ---
    print("--- Step 2: BMP Manager Tests ---")
    test_image_path = "test.bmp"
    
    # We attempt to read. If file is missing, read_bmp prints error and returns None.
    header, pixels = bmp_manager.read_bmp(test_image_path)
    
    if header is None:
        print("TEST 2.1: FAIL - Could not read 'test.bmp'. Ensure it is in this folder.")
        return # Stop tests

    print(f"TEST 2.1: PASS (Read {len(pixels)} bytes)")
    print("-" * 30)

    # --- Step 3: Steganography ---
    print("--- Step 3: Steganography Tests ---")
    
    secret_message = "Hello World!"
    output_image_path = "test_stego.bmp"
    
    print(f"Hiding: '{secret_message}'")

    try:
        # A. ENCODE
        new_pixels = Steganography.encode(pixels, secret_message)
        
        if bmp_manager.save_bmp(output_image_path, header, new_pixels):
            print(f"Saved to '{output_image_path}'.")
        else:
            print("Failed to save image.")
            return

        # B. DECODE
        # Read the NEW file back to ensure it worked
        new_header, encoded_pixels_read = bmp_manager.read_bmp(output_image_path)
        
        if new_header is None:
             print("TEST 3.1: FAIL (Could not read back the saved file)")
             return

        decoded_message = Steganography.decode(encoded_pixels_read)
        print(f"Decoded: '{decoded_message}'")
        
        # C. VERIFY
        if decoded_message == secret_message:
            print("TEST 3.1: PASS (Success!)")
        else:
            print("TEST 3.1: FAIL (Message mismatch)")
            
    except ValueError as e:
        print(f"TEST 3.1: FAIL (Capacity Error: {e})")
    except Exception as e:
        print(f"TEST 3.1: FAIL (Error: {e})")

    print("\n=== ALL TESTS COMPLETE ===")

if __name__ == "__main__":
    run_tests()