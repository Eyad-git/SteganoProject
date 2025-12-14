Image-Based Text Steganography (Pro Version)

Student Name: Eyad Basem Ahmed Alsaeed Ali

Student ID: 202400153

Module: KH4017CMD – Introduction to Programming

📌 Project Overview

This application allows users to hide secret text messages inside BMP images using the Least Significant Bit (LSB) technique.

Unlike basic steganography tools, this "Pro" version implements advanced security features including Vigenère Encryption and Coordinate Randomization (Scattering), ensuring that the hidden message cannot be detected or read by standard tools.

Crucially, this entire project is built using ONLY standard Python 3. No external libraries (like NumPy, Pillow, or OpenCV) were used.

✨ Key Features

Zero External Dependencies

Built purely with Python's built-in capabilities.

Manual binary file handling (rb/wb) and bitwise operations.

Custom math-based Pseudo-Random Number Generator (LCG).


==================================================================
Extended Vigenère Encryption (Stage 1)
==================================================================

Encrypts the message before hiding it.

Uses Modulo 256 math to support all characters (Emojis, Numbers, Symbols), not just A-Z.

==================================================================
Prime-Step Scatter Randomization (Stage 2)
==================================================================


Instead of hiding bits sequentially (which leaves a visible pattern), bits are scattered across the image based on the password.

Uses a GCD-based Prime Step algorithm to visit unique pixels instantly (O(1) complexity), making it fast even for large 4K images.


Robust Architecture:

Length Headers: Uses a 32-bit header to store message size, eliminating unreliable "delimiters" (Stage 3).

Smart BMP Handling: Automatically detects header size to support both 24-bit and 32-bit BMP files.

Input Validation: Handles missing files, write permissions, and empty inputs gracefully.

📂 Project Structure

SteganographyProject/
│
├── src/
│   ├── bmp_manager.py    # Handles raw byte reading/writing of BMP files
│   ├── cipher.py         # Extended Vigenère encryption logic
│   ├── prng.py           # Custom Math Generator (Linear Congruential & Prime Step)
│   ├── steganography.py  # Core LSB logic with scattering and length headers
│   └── utils.py          # Helper functions (Text <-> Binary conversion)
│
├── main.py               # The Main User Interface (CLI)
├── tests.py              # Automated Unit Tests for all modules
└── README.md             # Project Documentation


🚀 How to Run


1. Start the Application

Run the main script to access the menu:

python main.py


2. Usage Guide

Encode:

Select an input BMP image.

Type your message or select a text file.

Enter a Password: This is used to both encrypt the text and shuffle the pixel locations.

Save the output file.

Decode:

Select the image with the hidden message.

Enter the Password: If the password is wrong, the tool will fail to find the correct pixels or decrypt the text.

3. Run Unit Tests

To verify that the encryption, PRNG, and binary logic are working correctly:

python test_suite.py


🧠 Algorithms Used

1. Extended Vigenère Cipher

Encrypted = (Original_ASCII + Key_ASCII) % 256
Decrypted = (Encrypted_ASCII - Key_ASCII) % 256


2. Prime-Step Scattering

To avoid the slow process of shuffling a list of 2 million pixels, we calculate the target pixel index mathematically:

Step = (Derived from Password)
while GCD(Step, Total_Pixels) != 1:
    Step += 1  # Ensure Step is coprime to Total to visit every pixel once

Target_Index = (Start + (i * Step)) % Total_Pixels
