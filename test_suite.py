# test_suite.py - Root folder
# Run with: python test_suite.py

# --- IMPORTS ---
from src.utils import text_to_bits, bits_to_text
# --- HELPER FUNCTION ---
def run_test_case(test_id, func_name, input_val, actual_output, expected_output):
    """
    Prints the test details in the requested format: Input -> Function -> Output
    """
    print(f"--- TEST {test_id} ---")
    # Show Input (truncated if too long for display)
    print(f"Input: {input_val}")
    
    # Show Function Name
    print(f"Function: {func_name}")
    
    # Show the Actual Output
    print(f"Output: {actual_output}")
    
    # Check Result
    if actual_output == expected_output:
        print("Result: Pass")
        print("")
        return True
    else:
        print("Result: Fail")
        print(f"Expected: {expected_output}")
        print("")
        return False

print("========================================")
print("       STEGANOGRAPHY TEST SUITE         ")
print("========================================")

# ==========================================
# STEP 1: UTILS MODULE TESTS
# ==========================================
print("\n=== STEP 1: Utils (Text <-> Binary) ===")

# Test 1: text_to_bits
input_1 = "A"
output_1 = text_to_bits(input_1)
expected_1 = "01000001" # ASCII 65
run_test_case(1, "text_to_bits", input_1, output_1, expected_1)

# Test 2: bits_to_text
input_2 = "01000001"
output_2 = bits_to_text(input_2)
expected_2 = "A"
run_test_case(2, "bits_to_text", input_2, output_2, expected_2)

# Test 3: text_to_bits (Multiple characters)
input_3 = "Hi"
output_3 = text_to_bits(input_3)
expected_3 = "0100100001101001" # H=72, i=105
run_test_case(3, "text_to_bits", input_3, output_3, expected_3)
