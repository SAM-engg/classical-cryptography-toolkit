"""
test_monoalphabetic.py - Unit Tests for Monoalphabetic Substitution Cipher
"""

import unittest
from src.monoalphabetic import monoalphabetic_encrypt, monoalphabetic_decrypt, get_substitution_mapping
from src.validators import ValidationError


class TestMonoalphabeticCipher(unittest.TestCase):

    def setUp(self):
        self.qwerty_key = "QWERTYUIOPASDFGHJKLZXCVBNM"
        self.keyword = "ZEBRAS"

    def test_full_alphabet_key_round_trip(self):
        """Test encryption and decryption with a standard 26-letter permutation key."""
        text = "The Quick Brown Fox Jumps Over 13 Lazy Dogs!"
        cipher = monoalphabetic_encrypt(text, self.qwerty_key)
        self.assertNotEqual(cipher, text)
        decrypted = monoalphabetic_decrypt(cipher, self.qwerty_key)
        self.assertEqual(decrypted, text)

    def test_keyword_derived_key_round_trip(self):
        """Test keyword-derived substitution alphabet."""
        text = "CRYPTOGRAPHY AND NETWORK SECURITY"
        cipher = monoalphabetic_encrypt(text, self.keyword)
        decrypted = monoalphabetic_decrypt(cipher, self.keyword)
        self.assertEqual(decrypted, text)

    def test_case_and_special_character_preservation(self):
        """Case, punctuation, digits, spaces, and formatting must be preserved."""
        text = "Hello, World! 2026-27\nSpecial: @#$%^&*()"
        cipher = monoalphabetic_encrypt(text, self.qwerty_key)
        self.assertEqual(monoalphabetic_decrypt(cipher, self.qwerty_key), text)
        # Check lowercase letters mapped to lowercase
        self.assertTrue(cipher[1].islower())

    def test_empty_and_single_char(self):
        """Test empty string and single character inputs."""
        self.assertEqual(monoalphabetic_encrypt("", self.qwerty_key), "")
        self.assertEqual(monoalphabetic_decrypt("", self.qwerty_key), "")
        self.assertEqual(monoalphabetic_decrypt(monoalphabetic_encrypt("A", self.qwerty_key), self.qwerty_key), "A")

    def test_duplicate_letters_in_26_char_key_rejected(self):
        """A 26-character key with duplicate letters must raise ValidationError."""
        # 26 letters but two 'A's and no 'Z'
        invalid_key = "ABCDEFGHIAJKLMNOPQRSTUVWXY"
        self.assertEqual(len(invalid_key), 26)
        with self.assertRaises(ValidationError):
            monoalphabetic_encrypt("TEST", invalid_key)

    def test_empty_key_rejected(self):
        """Empty or whitespace keys must raise ValidationError."""
        with self.assertRaises(ValidationError):
            monoalphabetic_encrypt("TEST", "")
        with self.assertRaises(ValidationError):
            monoalphabetic_encrypt("TEST", "   ")

    def test_substitution_mapping_structure(self):
        """Mapping dictionary should have 26 distinct entries."""
        mapping = get_substitution_mapping(self.qwerty_key)
        self.assertEqual(len(mapping), 26)
        self.assertEqual(len(set(mapping.values())), 26)


if __name__ == "__main__":
    unittest.main()
