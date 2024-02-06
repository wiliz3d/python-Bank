# Hybrid Encryption System

## Overview

This project demonstrates a hybrid encryption system using Python and the `cryptography` library. The system combines both symmetric and asymmetric encryption for secure data transmission.

## File Structure

- `hybrid_encryption.py`: The main Python script containing classes for KeyGenerator, AsymmetricEncryptor, SymmetricEncryptor, and HybridEncryptor.

## Classes

### `KeyGenerator`

- `generate_keypair()`: Generates an RSA key pair for asymmetric encryption.
- `generate_symmetric_key()`: Generates a random symmetric key for symmetric encryption.

### `AsymmetricEncryptor`

- `encrypt(public_key, data)`: Encrypts data using the RSA public key.
- `decrypt(private_key, cipher_text)`: Decrypts data using the RSA private key.

### `SymmetricEncryptor`

- `encrypt(key, data)`: Encrypts data using the AES-GCM symmetric key.
- `decrypt(key, cipher_text)`: Decrypts data using the AES-GCM symmetric key.

### `HybridEncryptor`

- `encrypt(data)`: Generates key pairs, encrypts data with symmetric key and asymmetric key, and returns the encrypted data.
- `decrypt(encrypted_symmetric_key, encrypted_data_symmetric)`: Decrypts the symmetric key with the asymmetric key and uses it to decrypt the data.

## Example Usage

```python
# Example usage:
hybrid_encryptor = HybridEncryptor()

original_data = b"Hello, this is a secret message!"

encrypted_symmetric_key, encrypted_data_symmetric = hybrid_encryptor.encrypt(original_data)
decrypted_data = hybrid_encryptor.decrypt(encrypted_symmetric_key, encrypted_data_symmetric)

print(f"Original Data: {original_data}")
print(f"Decrypted Data: {decrypted_data}")
