"""
test_caesar.py - Unit Tests for Caesar Cipher
"""

import unittest
from src.caesar import caesar_encrypt, caesar_decrypt
from src.validators import ValidationError


class TestCaesarCipher(unittest.TestCase):
    
    def test_verified_vector(self):
        """Verify the exact required sample output: NETWORK SECURITY with key 5."""
        plaintext = "NETWORK SECURITY"
        key = 5
        ciphertext = caesar_encrypt(plaintext, key)
        self.assertEqual(ciphertext, "SJYBTWP XJHZWNYD")
        
        decrypted = caesar_decrypt(ciphertext, key)
        self.assertEqual(decrypted, "NETWORK SECURITY")

    def test_standard_shifts(self):
        """Test shift 3 (traditional Caesar) and ROT13."""
        self.assertEqual(caesar_encrypt("HELLO", 3), "KHOOR")
        self.assertEqual(caesar_decrypt("KHOOR", 3), "HELLO")
        
        self.assertEqual(caesar_encrypt("HELLO", 13), "URYYB")
        self.assertEqual(caesar_decrypt("URYYB", 13), "HELLO")

    def test_identity_and_wrap(self):
        """Shift 0 and multiples of 26 must produce identical output."""
        text = "Hello World 123!"
        self.assertEqual(caesar_encrypt(text, 0), text)
        self.assertEqual(caesar_encrypt(text, 26), text)
        self.assertEqual(caesar_encrypt(text, 52), text)

    def test_negative_shift(self):
        """Negative shifts should correctly wrap modulo 26."""
        self.assertEqual(caesar_encrypt("B", -1), "A")
        self.assertEqual(caesar_encrypt("A", -1), "Z")
        self.assertEqual(caesar_decrypt("A", -1), "B")

    def test_case_and_punctuation_preservation(self):
        """Preserve uppercase, lowercase, punctuation, numbers, and newlines."""
        text = "Test, Case 123!\nNew line."
        encrypted = caesar_encrypt(text, 4)
        decrypted = caesar_decrypt(encrypted, 4)
        self.assertEqual(decrypted, text)
        self.assertIn("123!", encrypted)
        self.assertIn("\n", encrypted)

    def test_empty_and_single_char(self):
        """Test empty string and single character inputs."""
        self.assertEqual(caesar_encrypt("", 5), "")
        self.assertEqual(caesar_decrypt("", 5), "")
        self.assertEqual(caesar_encrypt("A", 1), "B")
        self.assertEqual(caesar_decrypt("B", 1), "A")

    def test_invalid_keys(self):
        """Reject malformed keys with ValidationError."""
        with self.assertRaises(ValidationError):
            caesar_encrypt("TEST", "invalid")
        with self.assertRaises(ValidationError):
            caesar_encrypt("TEST", "")
        with self.assertRaises(ValidationError):
            caesar_encrypt("TEST", None)


if __name__ == "__main__":
    unittest.main()
