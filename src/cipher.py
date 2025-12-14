def vigenere_encrypt(data, key):
    """
    Encrypts BYTES using Vigenere.
    Works for text, emojis, or even files.
    """
    # Safety: Ensure we are working with bytes
    if isinstance(data, str):
        data = data.encode('utf-8')
        
    if not key:
        return data

    # Convert key to bytes too
    key_bytes = key.encode('utf-8')
    encrypted = bytearray()
    key_len = len(key_bytes)

    for i, byte_val in enumerate(data):
        # Get key byte
        k = key_bytes[i % key_len]
        # Math on bytes (0-255)
        enc_val = (byte_val + k) % 256
        encrypted.append(enc_val)

    return bytes(encrypted)

def vigenere_decrypt(data, key):
    """
    Decrypts BYTES using Vigenere.
    """
    if not key:
        return data

    key_bytes = key.encode('utf-8')
    decrypted = bytearray()
    key_len = len(key_bytes)

    for i, byte_val in enumerate(data):
        k = key_bytes[i % key_len]
        # Reverse math
        dec_val = (byte_val - k) % 256
        decrypted.append(dec_val)

    return bytes(decrypted)