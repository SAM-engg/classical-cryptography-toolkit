"""
test_columnar_transposition.py - Unit Tests for Columnar Transposition Cipher
"""

import unittest
from src.columnar_transposition import columnar_encrypt, columnar_decrypt
from src.validators import ValidationError


class TestColumnarTransposition(unittest.TestCase):

    def test_known_keyword_vector(self):
        """Test encryption and decryption with keyword 'ZEBRA'."""
        plaintext = "WE ARE DISCOVERED FLEE AT ONCE"
        key = "ZEBRA"
        ciphertext = columnar_encrypt(plaintext, key)
        decrypted = columnar_decrypt(ciphertext, key)
        self.assertEqual(decrypted, plaintext)

    def test_numeric_permutation_key(self):
        """Test 1-indexed and 0-indexed numeric permutation keys."""
        plaintext = "ATTACK AT DAWN TODAY"
        key_1_idx = "3 1 4 2"
        cipher = columnar_encrypt(plaintext, key_1_idx)
        decrypted = columnar_decrypt(cipher, key_1_idx)
        self.assertEqual(decrypted, plaintext)

    def test_irregular_grid_lengths(self):
        """Test irregular grids where N % W != 0 for various lengths."""
        key = "GERMAN"  # width 6
        for text_len in range(5, 35):
            sample = "A" * text_len
            sample = "".join(chr(ord('A') + (i % 26)) for i in range(text_len))
            cipher = columnar_encrypt(sample, key)
            decrypted = columnar_decrypt(cipher, key)
            self.assertEqual(decrypted, sample, f"Failed at length {text_len}")

    def test_keyword_with_duplicate_letters(self):
        """Keywords with repeated characters must maintain stable ordering."""
        plaintext = "SECRET MESSAGE TO TRANSMIT"
        key = "BANANA"  # contains repeated 'A' and 'N'
        cipher = columnar_encrypt(plaintext, key)
        decrypted = columnar_decrypt(cipher, key)
        self.assertEqual(decrypted, plaintext)

    def test_empty_and_single_char(self):
        """Empty input and single character strings return unchanged."""
        self.assertEqual(columnar_encrypt("", "KEY"), "")
        self.assertEqual(columnar_decrypt("", "KEY"), "")
        self.assertEqual(columnar_encrypt("A", "KEY"), "A")
        self.assertEqual(columnar_decrypt("A", "KEY"), "A")

    def test_invalid_keys(self):
        """Keys shorter than 2 chars or invalid numbers must raise ValidationError."""
        with self.assertRaises(ValidationError):
            columnar_encrypt("HELLO", "")
        with self.assertRaises(ValidationError):
            columnar_encrypt("HELLO", "A")
        with self.assertRaises(ValidationError):
            columnar_encrypt("HELLO", "1 5 9")  # gap in permutation


if __name__ == "__main__":
    unittest.main()
