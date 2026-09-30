"""
test_one_time_pad.py - Unit Tests for One-Time Pad
"""

import unittest
from src.one_time_pad import otp_encrypt, otp_decrypt, generate_otp_key
from src.validators import ValidationError


class TestOneTimePad(unittest.TestCase):

    def test_auto_key_generation_and_round_trip(self):
        """Auto-generated key must have exact alphabetic length and round-trip successfully."""
        plaintext = "TOP SECRET INFORMATION"
        cipher, key_used = otp_encrypt(plaintext)
        
        alpha_count = sum(1 for c in plaintext if c.isalpha())
        self.assertEqual(len(key_used), alpha_count)
        self.assertTrue(key_used.isalpha() and key_used.isupper())
        
        decrypted = otp_decrypt(cipher, key_used)
        self.assertEqual(decrypted, plaintext)

    def test_explicit_key_encryption_and_decryption(self):
        """Test with manually supplied valid key."""
        plaintext = "HELLO"
        key = "XMCKL"
        cipher, key_used = otp_encrypt(plaintext, key)
        self.assertEqual(key_used, key)
        decrypted = otp_decrypt(cipher, key)
        self.assertEqual(decrypted, plaintext)

    def test_key_length_mismatch_raises_error(self):
        """Keys shorter or longer than the alphabetic letter count must raise ValidationError."""
        plaintext = "HELLO"  # 5 letters
        with self.assertRaises(ValidationError) as ctx1:
            otp_encrypt(plaintext, "KEY")  # 3 letters (too short)
        self.assertIn("mismatch", str(ctx1.exception).lower())
        
        with self.assertRaises(ValidationError) as ctx2:
            otp_encrypt(plaintext, "TOOLONGKEY")  # 10 letters (too long)
        self.assertIn("mismatch", str(ctx2.exception).lower())

    def test_preservation_of_spaces_and_symbols(self):
        """Spaces, punctuation, numbers are preserved."""
        plaintext = "Plan A: Execute at 09:00!"
        cipher, key = otp_encrypt(plaintext)
        decrypted = otp_decrypt(cipher, key)
        self.assertEqual(decrypted, plaintext)
        self.assertIn("09:00!", cipher)

    def test_empty_input(self):
        """Empty text returns empty string and empty key."""
        cipher, key = otp_encrypt("")
        self.assertEqual(cipher, "")
        self.assertEqual(key, "")
        self.assertEqual(otp_decrypt("", ""), "")


if __name__ == "__main__":
    unittest.main()
