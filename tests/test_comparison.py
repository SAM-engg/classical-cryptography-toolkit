"""
test_comparison.py - Unit Tests for Comparison and Benchmarking Module
"""

import unittest
from src.comparison import run_single_comparison, compare_ciphers, CIPHER_METADATA


class TestComparisonModule(unittest.TestCase):

    def test_single_comparison_success(self):
        """Test single comparison execution and metric fields."""
        res = run_single_comparison("Caesar Cipher", "TEST BENCHMARK", 3)
        self.assertEqual(res["cipher_name"], "Caesar Cipher")
        self.assertEqual(res["status"], "Success")
        self.assertTrue(res["round_trip_success"])
        self.assertGreater(res["encrypt_time_ms"], 0.0)

    def test_multi_cipher_comparison(self):
        """Test multi-cipher benchmarking execution across all supported ciphers."""
        ciphers = list(CIPHER_METADATA.keys())
        results = compare_ciphers(ciphers, "NETWORK SECURITY EXPERIMENT")
        self.assertEqual(len(results), 8)
        for r in results:
            self.assertEqual(r["status"], "Success")
            self.assertIn("encrypt_time_ms", r)
            self.assertIn("decrypt_time_ms", r)


if __name__ == "__main__":
    unittest.main()
