"""
test_hill.py - Unit Tests for Hill Cipher (2x2 and 3x3)
"""

import unittest
from src.hill import hill_encrypt, hill_decrypt, get_hill_determinant, invert_hill_matrix
from src.validators import parse_hill_key, ValidationError


class TestHillCipher(unittest.TestCase):

    def setUp(self):
        # 2x2 key: [3, 3; 2, 5] -> det = 15 - 6 = 9. gcd(9, 26) = 1. Invertible!
        self.key_2x2 = "3 3 2 5"
        # 3x3 key: [6, 24, 1; 13, 16, 10; 20, 17, 15] -> classic textbook invertible key
        self.key_3x3 = "6 24 1 13 16 10 20 17 15"

    def test_2x2_round_trip(self):
        """Test encryption and decryption round-trip for 2x2 matrix."""
        plaintext = "HELP"
        cipher = hill_encrypt(plaintext, self.key_2x2)
        self.assertEqual(cipher, "DPLE")
        decrypted = hill_decrypt(cipher, self.key_2x2)
        self.assertEqual(decrypted, "HELP")

    def test_2x2_with_odd_padding(self):
        """Odd length text must be padded with 'X'."""
        plaintext = "CAT"
        cipher = hill_encrypt(plaintext, self.key_2x2)
        decrypted = hill_decrypt(cipher, self.key_2x2)
        self.assertEqual(decrypted, "CATX")

    def test_3x3_round_trip(self):
        """Test encryption and decryption round-trip for 3x3 matrix."""
        plaintext = "ACT"
        cipher = hill_encrypt(plaintext, self.key_3x3)
        decrypted = hill_decrypt(cipher, self.key_3x3)
        self.assertEqual(decrypted, "ACT")

    def test_matrix_parsing_keyword_format(self):
        """Test parsing alphabetic keywords for 2x2 keys."""
        # 'HILL' -> H(7), I(8), L(11), L(11) -> det = 7*11 - 8*11 = 77 - 88 = -11 = 15 mod 26.
        # gcd(15, 26) = 1. Invertible!
        matrix = parse_hill_key("HILL")
        self.assertEqual(matrix, [[7, 8], [11, 11]])
        cipher = hill_encrypt("CODE", "HILL")
        decrypted = hill_decrypt(cipher, "HILL")
        self.assertEqual(decrypted, "CODE")

    def test_reject_zero_determinant(self):
        """Singular matrix with det=0 mod 26 must be strictly rejected."""
        # [2, 4; 1, 2] -> det = 2*2 - 4*1 = 0
        with self.assertRaises(ValidationError) as ctx:
            hill_encrypt("TEST", "2 4 1 2")
        self.assertIn("determinant is 0", str(ctx.exception).lower())

    def test_reject_even_determinant_shares_factor_2(self):
        """Matrix where determinant shares factor 2 with 26 must be rejected."""
        # [2, 1; 4, 4] -> det = 8 - 4 = 4. gcd(4, 26) = 2 != 1.
        with self.assertRaises(ValidationError) as ctx:
            hill_encrypt("TEST", "2 1 4 4")
        self.assertIn("not coprime", str(ctx.exception).lower())

    def test_reject_determinant_shares_factor_13(self):
        """Matrix where determinant shares factor 13 with 26 must be rejected."""
        # Matrix with det = 13: [1, 0; 0, 13] -> det = 13.
        with self.assertRaises(ValidationError) as ctx:
            hill_encrypt("TEST", "1 0 0 13")
        self.assertIn("not coprime", str(ctx.exception).lower())

    def test_reject_malformed_dimensions(self):
        """Matrices not containing 4 or 9 elements must be rejected."""
        with self.assertRaises(ValidationError):
            hill_encrypt("TEST", "1 2 3")
        with self.assertRaises(ValidationError):
            hill_encrypt("TEST", "INVALIDKEY")

    def test_empty_input(self):
        """Empty plaintext returns empty ciphertext."""
        self.assertEqual(hill_encrypt("", self.key_2x2), "")
        self.assertEqual(hill_decrypt("", self.key_2x2), "")


if __name__ == "__main__":
    unittest.main()
