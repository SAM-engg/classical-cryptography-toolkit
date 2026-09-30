"""
test_playfair.py - Unit Tests for Playfair Cipher
"""

import unittest
from src.playfair import (
    generate_playfair_matrix,
    prepare_playfair_text,
    playfair_encrypt,
    playfair_decrypt
)
from src.validators import ValidationError


class TestPlayfairCipher(unittest.TestCase):

    def setUp(self):
        self.key = "MONARCHY"

    def test_matrix_generation(self):
        """Matrix must be 5x5, contain 25 letters, and omit 'J'."""
        matrix, pos = generate_playfair_matrix(self.key)
        self.assertEqual(len(matrix), 5)
        for row in matrix:
            self.assertEqual(len(row), 5)
            self.assertNotIn('J', row)
            
        all_chars = [c for row in matrix for c in row]
        self.assertEqual(len(set(all_chars)), 25)
        self.assertEqual(pos['J'], pos['I'])

    def test_repeated_letters_filler_insertion(self):
        """Repeated letters in a digraph must be split with filler 'X'."""
        # "BALLOON" has 'LL' -> should become [('B','A'), ('L','X'), ('L','O'), ('O','N')]
        digraphs = prepare_playfair_text("BALLOON")
        self.assertEqual(digraphs, [('B', 'A'), ('L', 'X'), ('L', 'O'), ('O', 'N')])

    def test_odd_length_padding(self):
        """Odd length text must pad the final letter with 'X'."""
        digraphs = prepare_playfair_text("CAT")
        self.assertEqual(digraphs, [('C', 'A'), ('T', 'X')])

    def test_repeated_x_uses_q_filler(self):
        """If repeated letter is 'X', the filler character must be 'Q'."""
        digraphs = prepare_playfair_text("XX")
        self.assertEqual(digraphs, [('X', 'Q'), ('X', 'Z')])

    def test_playfair_round_trip(self):
        """Encryption followed by decryption must recover normalized digraphs."""
        plaintext = "INSTRUMENTS"
        cipher = playfair_encrypt(plaintext, self.key)
        decrypted = playfair_decrypt(cipher, self.key)
        # In Playfair, J becomes I and INSTRUMENTS (11 chars) pads to 12 chars (INSTRUMENTSX)
        self.assertTrue(decrypted.startswith("INSTRUMENTS"))

    def test_playfair_spaces_and_case(self):
        """Playfair strips non-alphabetic characters and handles mixed case."""
        cipher1 = playfair_encrypt("hello world", self.key)
        cipher2 = playfair_encrypt("HELLOWORLD", self.key)
        self.assertEqual(cipher1, cipher2)

    def test_empty_input(self):
        """Empty plaintext should return empty ciphertext."""
        self.assertEqual(playfair_encrypt("", self.key), "")
        self.assertEqual(playfair_decrypt("", self.key), "")

    def test_empty_or_invalid_key(self):
        """Empty or non-alphabetic keys should be rejected."""
        with self.assertRaises(ValidationError):
            playfair_encrypt("HELLO", "")
        with self.assertRaises(ValidationError):
            playfair_encrypt("HELLO", "12345")


if __name__ == "__main__":
    unittest.main()
