"""
monoalphabetic.py - Monoalphabetic Substitution Cipher Implementation
Design and Development of a Classical Cryptography Toolkit
Course: Network Security | Class: Final Year (ECM) 2026-27

Principle:
    A monoalphabetic substitution cipher replaces each letter of the plaintext alphabet
    with a uniquely assigned letter from a 26-letter permutation alphabet.
    Unlike polyalphabetic ciphers, the mapping between a plaintext character and its
    ciphertext counterpart remains constant throughout the entire message.

Key Formats Supported:
    1. Full 26-letter key: A permutation of A-Z (e.g., "QWERTYUIOPASDFGHJKLZXCVBNM").
    2. Keyword key: A memorable word (e.g., "SECURITY"), from which the unique letters
       are placed first, followed by the remaining unused letters of the alphabet in order.

Character and Case Handling:
    - Uppercase characters map to the corresponding uppercase key character.
    - Lowercase characters map to the corresponding lowercase key character.
    - Spaces, punctuation, numbers, and symbols are preserved without modification.
"""

from src.validators import validate_text, validate_monoalphabetic_key

STANDARD_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def monoalphabetic_encrypt(plaintext: str, key: str) -> str:
    """
    Encrypt plaintext using the Monoalphabetic Substitution Cipher.
    
    Args:
        plaintext: The input text to encrypt.
        key: 26-letter substitution alphabet or keyword.
        
    Returns:
        Ciphertext string with substitutions applied.
    """
    validate_text(plaintext, allow_empty=True)
    cipher_alphabet = validate_monoalphabetic_key(key)
    
    # Build translation mappings for both uppercase and lowercase
    enc_map = {}
    for p, c in zip(STANDARD_ALPHABET, cipher_alphabet):
        enc_map[p] = c
        enc_map[p.lower()] = c.lower()
        
    result = [enc_map.get(char, char) for char in plaintext]
    return "".join(result)


def monoalphabetic_decrypt(ciphertext: str, key: str) -> str:
    """
    Decrypt ciphertext using the Monoalphabetic Substitution Cipher.
    
    Args:
        ciphertext: The input ciphertext to decrypt.
        key: 26-letter substitution alphabet or keyword used for encryption.
        
    Returns:
        Decrypted plaintext string.
    """
    validate_text(ciphertext, allow_empty=True)
    cipher_alphabet = validate_monoalphabetic_key(key)
    
    # Build reverse translation mappings
    dec_map = {}
    for p, c in zip(STANDARD_ALPHABET, cipher_alphabet):
        dec_map[c] = p
        dec_map[c.lower()] = p.lower()
        
    result = [dec_map.get(char, char) for char in ciphertext]
    return "".join(result)


def get_substitution_mapping(key: str) -> dict:
    """
    Helper function to inspect the resulting 26-letter mapping for education/display.
    """
    cipher_alphabet = validate_monoalphabetic_key(key)
    return dict(zip(STANDARD_ALPHABET, cipher_alphabet))
