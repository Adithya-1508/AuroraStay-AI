from cryptography.fernet import Fernet


class EncryptionService:
    """Provides AES symmetric encryption for database fields and sensitive data."""

    def __init__(self, key: bytes | None = None) -> None:
        # Generate dynamic key if not provided (fallback)
        self._key = key or Fernet.generate_key()
        self._cipher = Fernet(self._key)

    def encrypt_string(self, plaintext: str) -> str:
        """Encrypts a string and returns a base64 encoded token string."""
        if not plaintext:
            return ""
        encrypted_bytes = self._cipher.encrypt(plaintext.encode())
        return encrypted_bytes.decode()

    def decrypt_string(self, ciphertext: str) -> str:
        """Decrypts a base64 encoded token and returns the raw string."""
        if not ciphertext:
            return ""
        decrypted_bytes = self._cipher.decrypt(ciphertext.encode())
        return decrypted_bytes.decode()
