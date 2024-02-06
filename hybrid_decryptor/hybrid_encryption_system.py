import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

class KeyGenerator:
    @staticmethod
    def generate_keypair():
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        return private_key, public_key

    @staticmethod
    def generate_symmetric_key():
        return os.urandom(32)

class AsymmetricEncryptor:
    @staticmethod
    def encrypt(public_key, data):
        cipher_text = public_key.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return cipher_text

    @staticmethod
    def decrypt(private_key, cipher_text):
        decrypted_data = private_key.decrypt(
            cipher_text,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted_data

class SymmetricEncryptor:
    @staticmethod
    def encrypt(key, data):
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        cipher_text = encryptor.update(data) + encryptor.finalize()
        return iv + encryptor.tag + cipher_text

    @staticmethod
    def decrypt(key, cipher_text):
        iv = cipher_text[:16]
        tag = cipher_text[16:32]
        encrypted_data = cipher_text[32:]
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
        return decrypted_data

class HybridEncryptor:
    def __init__(self):
        self.key_generator = KeyGenerator()
        self.asymmetric_encryptor = AsymmetricEncryptor()
        self.symmetric_encryptor = SymmetricEncryptor()
        self.private_key, self.public_key = self.key_generator.generate_keypair()

    def encrypt(self, data):
        # Generate symmetric key
        symmetric_key = self.key_generator.generate_symmetric_key()

        # Encrypt data with symmetric key
        encrypted_data_symmetric = self.symmetric_encryptor.encrypt(symmetric_key, data)

        # Encrypt symmetric key with asymmetric key
        encrypted_symmetric_key = self.asymmetric_encryptor.encrypt(self.public_key, symmetric_key)

        return encrypted_symmetric_key, encrypted_data_symmetric

    def decrypt(self, encrypted_symmetric_key, encrypted_data_symmetric):
        # Decrypt symmetric key with asymmetric key
        decrypted_symmetric_key = self.asymmetric_encryptor.decrypt(self.private_key, encrypted_symmetric_key)

        # Decrypt data with symmetric key
        decrypted_data = self.symmetric_encryptor.decrypt(decrypted_symmetric_key, encrypted_data_symmetric)

        return decrypted_data

# Example usage:
hybrid_encryptor = HybridEncryptor()

original_data = b"Hello, this is a secret message!"

encrypted_symmetric_key, encrypted_data_symmetric = hybrid_encryptor.encrypt(original_data)
decrypted_data = hybrid_encryptor.decrypt(encrypted_symmetric_key, encrypted_data_symmetric)

print(f"Original Data: {original_data}")
print(f"Decrypted Data: {decrypted_data}")
