"""
test_file_operations.py - Unit Tests for File Operations Module
"""

import unittest
import os
import tempfile
from src.file_operations import read_text_file, write_text_file, process_file_cipher, FileOperationError


class TestFileOperations(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.sample_path = os.path.join(self.test_dir.name, "sample.txt")
        with open(self.sample_path, "w", encoding="utf-8") as f:
            f.write("NETWORK SECURITY PROJECT\nTesting file encryption and UTF-8 handling.")

    def tearDown(self):
        self.test_dir.cleanup()

    def test_read_and_write_file(self):
        """Test reading and writing normal text files."""
        content, meta = read_text_file(self.sample_path)
        self.assertIn("NETWORK SECURITY", content)
        self.assertEqual(meta["filename"], "sample.txt")

        out_path = os.path.join(self.test_dir.name, "output.txt")
        written_count = write_text_file(out_path, content)
        self.assertEqual(written_count, len(content))
        self.assertTrue(os.path.exists(out_path))

    def test_empty_file_rejected(self):
        """Empty files should raise FileOperationError."""
        empty_path = os.path.join(self.test_dir.name, "empty.txt")
        open(empty_path, "w").close()
        with self.assertRaises(FileOperationError):
            read_text_file(empty_path)

    def test_missing_file_rejected(self):
        """Non-existent file should raise FileOperationError."""
        with self.assertRaises(FileOperationError):
            read_text_file(os.path.join(self.test_dir.name, "nonexistent.txt"))

    def test_process_file_cipher_encrypt_decrypt(self):
        """Test encryption and decryption of file content across ciphers."""
        content, _ = read_text_file(self.sample_path)
        cipher, _ = process_file_cipher(content, "Caesar Cipher", 5, mode="encrypt")
        decrypted, _ = process_file_cipher(cipher, "Caesar Cipher", 5, mode="decrypt")
        self.assertEqual(decrypted, content)


if __name__ == "__main__":
    unittest.main()
