"""
test_vigenere.py - Unit Tests for Vigenère Cipher
"""

import unittest
from src.vigenere import vigenere_encrypt, vigenere_decrypt
from src.validators import ValidationError


class TestVigenereCipher(unittest.TestCase):

    def test_known_test_vector(self):
        """Test classic standard known test vector."""
        plaintext = "ATTACKATDAWN"
        key = "LEMON"
        # A+L=L, T+E=X, T+M=F, A+O=O, C+N=P, K+L=V, A+E=E, T+M=F, D+O=R, A+N=N, W+L=H, N+E=R
        expected = "LXFOPVEFRNHR"
        ciphertext = vigenere_encrypt(plaintext, key)
        self.assertEqual(ciphertext, expected)
        self.assertEqual(vigenere_decrypt(ciphertext, key), plaintext)

    def test_case_and_punctuation_preservation(self):
        """Keystream must only advance for alphabetic letters, preserving punctuation."""
        plaintext = "Attack at Dawn! 123"
        key = "lemon"
        cipher = vigenere_encrypt(plaintext, key)
        # Spaces, '!' and '123' must be in the exact same positions
        self.assertEqual(cipher[6], " ")
        self.assertEqual(cipher[9], " ")
        self.assertTrue(cipher.endswith("! 123"))
        self.assertEqual(vigenere_decrypt(cipher, key), plaintext)

    def test_single_letter_key_equivalent_to_caesar(self):
        """A single-character key 'D' (shift 3) must match Caesar shift 3."""
        from src.caesar import caesar_encrypt
        text = "NETWORK SECURITY"
        self.assertEqual(vigenere_encrypt(text, "D"), caesar_encrypt(text, 3))

    def test_empty_input(self):
        """Empty text returns empty string."""
        self.assertEqual(vigenere_encrypt("", "KEY"), "")
        self.assertEqual(vigenere_decrypt("", "KEY"), "")

    def test_invalid_keys(self):
        """Empty or non-alphabetic keys must raise ValidationError."""
        with self.assertRaises(ValidationError):
            vigenere_encrypt("HELLO", "")
        with self.assertRaises(ValidationError):
            vigenere_encrypt("HELLO", "12345")


if __name__ == "__main__":
    unittest.main()
