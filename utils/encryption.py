"""
Legifyx Encryption Utilities
Data security and encryption for sensitive contract data
"""

import os
import base64
from pathlib import Path
from typing import Optional
import hashlib
import logging

logger = logging.getLogger(__name__)


class EncryptionService:
    """Handle encryption and decryption of sensitive data"""
    
    def __init__(self, key_file: str = None):
        self.key_file = Path(key_file) if key_file else Path.cwd() / ".encryption_key"
        self.key = self._load_or_generate_key()
    
    def _load_or_generate_key(self) -> bytes:
        """Load existing key or generate a new one"""
        if self.key_file.exists():
            with open(self.key_file, 'rb') as f:
                return f.read()
        else:
            key = self._generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
            return key
    
    def _generate_key(self) -> bytes:
        """Generate a new encryption key"""
        try:
            from cryptography.fernet import Fernet
            return Fernet.generate_key()
        except ImportError:
            # Fallback to basic key generation
            return base64.urlsafe_b64encode(os.urandom(32))
    
    def encrypt(self, data: str) -> str:
        """
        Encrypt string data
        
        Args:
            data: Plain text to encrypt
        
        Returns:
            Encrypted string (base64 encoded)
        """
        try:
            from cryptography.fernet import Fernet
            f = Fernet(self.key)
            encrypted = f.encrypt(data.encode())
            return encrypted.decode()
        except ImportError:
            # Basic XOR encryption fallback
            return self._basic_encrypt(data)
    
    def decrypt(self, encrypted_data: str) -> str:
        """
        Decrypt encrypted data
        
        Args:
            encrypted_data: Encrypted string
        
        Returns:
            Decrypted plain text
        """
        try:
            from cryptography.fernet import Fernet
            f = Fernet(self.key)
            decrypted = f.decrypt(encrypted_data.encode())
            return decrypted.decode()
        except ImportError:
            return self._basic_decrypt(encrypted_data)
    
    def _basic_encrypt(self, data: str) -> str:
        """Basic XOR encryption fallback"""
        key_bytes = self.key[:len(data.encode())] * (len(data.encode()) // len(self.key) + 1)
        encrypted = bytes(a ^ b for a, b in zip(data.encode(), key_bytes[:len(data.encode())]))
        return base64.urlsafe_b64encode(encrypted).decode()
    
    def _basic_decrypt(self, data: str) -> str:
        """Basic XOR decryption fallback"""
        decoded = base64.urlsafe_b64decode(data.encode())
        key_bytes = self.key[:len(decoded)] * (len(decoded) // len(self.key) + 1)
        decrypted = bytes(a ^ b for a, b in zip(decoded, key_bytes[:len(decoded)]))
        return decrypted.decode()
    
    def hash_file(self, file_path: str) -> str:
        """Generate SHA-256 hash of a file"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()
    
    def hash_text(self, text: str) -> str:
        """Generate SHA-256 hash of text"""
        return hashlib.sha256(text.encode()).hexdigest()
    
    def secure_delete(self, file_path: str) -> bool:
        """Securely delete a file by overwriting"""
        try:
            path = Path(file_path)
            if path.exists():
                size = path.stat().st_size
                with open(file_path, 'wb') as f:
                    f.write(os.urandom(size))
                os.remove(file_path)
                return True
            return False
        except Exception as e:
            logger.error(f"Secure delete failed: {e}")
            return False
