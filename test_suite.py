from src import utils
from src import bmp_manager
from src import Steganography
from src import cipher
from src import prng

def run_tests():
    print("=== STARTING PROJECT TESTS (FINAL PRO VERSION) ===\n")

    # ---------------------------------------------------------
    # STEP 1: UTILS (UTF-8 & Binary)
    # ---------------------------------------------------------
    print("--- Step 1: Utils (Emoji & Bytes) ---")
    
    # 1.1 Simple Text
    if utils.to_binary("A") == "01000001":
        print("TEST 1.1: PASS (Text to Binary)")
    else:
        print("TEST 1.1: FAIL")

    # 1.2 Emoji Round Trip
    emoji_text = "Hi 😀"
    binary_data = utils.to_binary(emoji_text)
    # Convert back to bytes, then decode utf-8
    restored_bytes = utils.from_binary(binary_data)
    if restored_bytes.decode('utf-8') == emoji_text:
        print("TEST 1.2: PASS (Emoji Roundtrip)")
    else:
        print(f"TEST 1.2: FAIL (Got: {restored_bytes})")
    print("-" * 30)

    # ---------------------------------------------------------
    # STEP 2: CIPHER (Vigenère on Bytes)
    # ---------------------------------------------------------
    print("--- Step 2: Cipher (Encryption) ---")
    
    secret = "Secret 🤫"
    password = "Key"
    
    # Encrypt (Returns Bytes)
    enc_bytes = cipher.vigenere_encrypt(secret, password)
    
    # Decrypt (Returns Bytes)
    dec_bytes = cipher.vigenere_decrypt(enc_bytes, password)
    
    if dec_bytes.decode('utf-8') == secret:
        print("TEST 2.1: PASS (Encrypt -> Decrypt Success)")
    else:
        print("TEST 2.1: FAIL")
        
    # Wrong Password Check
    bad_dec = cipher.vigenere_decrypt(enc_bytes, "Wrong")
    if bad_dec.decode('utf-8', errors='ignore') != secret:
        print("TEST 2.2: PASS (Wrong password scrambled data)")
    else:
        print("TEST 2.2: FAIL (Wrong password worked?!)")
    print("-" * 30)

    # ---------------------------------------------------------
    # STEP 3: PRNG (Fast Step Generator)
    # ---------------------------------------------------------
    print("--- Step 3: Fast Scatter Generator ---")
    
    total_pixels = 1000
    gen1 = prng.StepGenerator("pass1", total_pixels)
    gen2 = prng.StepGenerator("pass1", total_pixels)
    gen3 = prng.StepGenerator("pass2", total_pixels)
    
    # Consistency
    if gen1.get_index(0) == gen2.get_index(0):
        print("TEST 3.1: PASS (Same password = Same start)")
    else:
        print("TEST 3.1: FAIL")

    # Scattering (Diff passwords = Diff start)
    if gen1.get_index(0) != gen3.get_index(0):
        print("TEST 3.2: PASS (Diff password = Diff start)")
    else:
        print("TEST 3.2: FAIL")
        
    # Unique Steps (Index 0 != Index 1)
    if gen1.get_index(0) != gen1.get_index(1):
        print("TEST 3.3: PASS (Step logic moves forward)")
    else:
        print("TEST 3.3: FAIL")
    print("-" * 30)

    # ---------------------------------------------------------
    # STEP 4: STEGANOGRAPHY (Integration)
    # ---------------------------------------------------------
    print("--- Step 4: Steganography (Full Flow) ---")
    
    # Create fake image data (5000 bytes)
    mock_pixels = bytearray(b'\x00' * 5000)
    
    # Test Data
    msg = "Cyber Security 🚀"
    stego_pass = "MySafePass"
    
    # 1. Encode
    # Note: encode expects 'bytes' for the message if encrypting manually, 
    # but our stego.encode handles strings via utils.to_binary too.
    encoded_pixels = Steganography.encode(mock_pixels, msg, stego_pass)
    
    # 2. Decode Correctly
    decoded_bytes = Steganography.decode(encoded_pixels, stego_pass)
    
    if decoded_bytes and decoded_bytes.decode('utf-8') == msg:
        print("TEST 4.1: PASS (Encode -> Decode Success)")
    else:
        print(f"TEST 4.1: FAIL (Got: {decoded_bytes})")

    # 3. Decode Wrong Password
    # This should fail checksum or return garbage
    decoded_wrong = Steganography.decode(encoded_pixels, "Wrong")
    
    if decoded_wrong is None or decoded_wrong.decode('utf-8', errors='ignore') != msg:
        print("TEST 4.2: PASS (Wrong password fails security)")
    else:
        print("TEST 4.2: FAIL (Wrong password worked!)")

    print("-" * 30)
    print("\n=== ALL TESTS COMPLETE ===")

if __name__ == "__main__":
    run_tests()