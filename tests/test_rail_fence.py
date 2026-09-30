"""
test_rail_fence.py - Unit Tests for Rail Fence Cipher
"""

import unittest
from src.rail_fence import rail_fence_encrypt, rail_fence_decrypt
from src.validators import ValidationError


class TestRailFenceCipher(unittest.TestCase):

    def test_classic_known_vector(self):
        """Test classic standard vector: DEFEND THE EAST WALL with 3 rails."""
        plaintext = "DEFEND THE EAST WALL"
        rails = 3
        # Rail 0: D . . . N . . . H . . . A . . . W . . . E -> DNHAWE
        # Rail 1: . E . E . D . T . E . E . S .   . A . L . -> EEDTEES AL
        # Rail 2: . . F . . .   . . .   . . . T . . . L . . -> F  TL
        ciphertext = rail_fence_encrypt(plaintext, rails)
        self.assertEqual(ciphertext, "DNHAWEEDTEES ALF  TL")
        decrypted = rail_fence_decrypt(ciphertext, rails)
        self.assertEqual(decrypted, plaintext)

    def test_multiple_rail_depths_round_trip(self):
        """Round trip for depths 2, 3, 4, 5 on varying texts."""
        text = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
        for r in [2, 3, 4, 5, 7, 10]:
            cipher = rail_fence_encrypt(text, r)
            decrypted = rail_fence_decrypt(cipher, r)
            self.assertEqual(decrypted, text, f"Failed for rail count {r}")

    def test_rails_greater_than_text_length(self):
        """When rails >= text length, text remains unchanged."""
        text = "SHORT"
        self.assertEqual(rail_fence_encrypt(text, 10), text)
        self.assertEqual(rail_fence_decrypt(text, 10), text)

    def test_single_char_and_empty(self):
        """Empty input and single characters return immediately."""
        self.assertEqual(rail_fence_encrypt("", 3), "")
        self.assertEqual(rail_fence_decrypt("", 3), "")
        self.assertEqual(rail_fence_encrypt("A", 3), "A")
        self.assertEqual(rail_fence_decrypt("A", 3), "A")

    def test_invalid_rail_keys(self):
        """Rails < 2 or non-integers must raise ValidationError."""
        with self.assertRaises(ValidationError):
            rail_fence_encrypt("HELLO", 1)
        with self.assertRaises(ValidationError):
            rail_fence_encrypt("HELLO", 0)
        with self.assertRaises(ValidationError):
            rail_fence_encrypt("HELLO", "abc")


if __name__ == "__main__":
    unittest.main()
