from src import utils
from src import bmp_manager

def run_tests():
    print("=== STARTING PROJECT TESTS ===\n")

    # ---------------------------------------------------------
    # STEP 1 TESTS: UTILS (Text <-> Binary)
    # ---------------------------------------------------------
    print("--- Step 1: Utils Tests ---")
    
    # Test 1.1: Encoding
    input_text = "Hi"
    expected_binary = "0100100001101001"
    actual_binary = utils.text_to_bits(input_text)
    
    if actual_binary == expected_binary:
        print(f"TEST 1.1 (Text to Binary): PASS")
    else:
        print(f"TEST 1.1 (Text to Binary): FAIL")
        print(f"  Expected: {expected_binary}")
        print(f"  Actual:   {actual_binary}")

    # Test 1.2: Decoding
    actual_text = utils.bits_to_text(expected_binary)
    if actual_text == input_text:
        print(f"TEST 1.2 (Binary to Text): PASS")
    else:
        print(f"TEST 1.2 (Binary to Text): FAIL")
        print(f"  Expected: {input_text}")
        print(f"  Actual:   {actual_text}")
    
    print("-" * 30)

    # ---------------------------------------------------------
    # STEP 2 TESTS: IMAGE HANDLER (Read/Write BMP)
    # ---------------------------------------------------------
    print("--- Step 2: Image Handler Tests ---")
    
    input_filename = "test.bmp"
    output_filename = "test_copy.bmp"

    # Test 2.1: Reading
    print(f"Reading '{input_filename}'...")
    header, pixels = bmp_manager.read_bmp(input_filename)

    if header is None or pixels is None:
        print(f"TEST 2.1 (Read BMP): FAIL - Could not read '{input_filename}'")
        print("  (Make sure 'test.bmp' is in the same folder as this script)")
        return # Stop tests if we can't read the file

    # Validate Header Size
    if len(header) == 54:
        print(f"TEST 2.1 (Read BMP - Header Size 54): PASS")
    else:
        print(f"TEST 2.1 (Read BMP): FAIL - Header size is {len(header)} bytes (Expected 54)")

    # Test 2.2: Writing
    print(f"Saving copy to '{output_filename}'...")
    success = bmp_manager.save_bmp(output_filename, header, pixels)

    if success:
        print(f"TEST 2.2 (Save BMP): PASS (File created)")
    else:
        print(f"TEST 2.2 (Save BMP): FAIL (Save function returned False)")

    # Test 2.3: Verification (Byte-by-Byte Comparison)
    # We open both files and ensure they are identical
    try:
        with open(input_filename, 'rb') as f1:
            original_data = f1.read()
        with open(output_filename, 'rb') as f2:
            new_data = f2.read()
            
        if original_data == new_data:
            print(f"TEST 2.3 (Integrity Check): PASS (Copy is identical to original)")
        else:
            print(f"TEST 2.3 (Integrity Check): FAIL (Copy differs from original)")
    except Exception as e:
        print(f"TEST 2.3 (Integrity Check): FAIL (Error opening files: {e})")

    print("\n=== ALL TESTS COMPLETE ===")

if __name__ == "__main__":
    run_tests()