"""
vigenere.py - Vigenère Polyalphabetic Cipher Implementation
Design and Development of a Classical Cryptography Toolkit
Course: Network Security | Class: Final Year (ECM) 2026-27

Principle:
    The Vigenère Cipher is a polyalphabetic substitution cipher created in 1553 by
    Giovan Battista Bellaso and later misattributed to Blaise de Vigenère.
    It uses a repeating keyword to shift each letter of the plaintext by different
    amounts, flattening single-letter frequency distributions and resisting simple
    frequency analysis.

Mathematical Formulation:
    Encryption: C_i = (P_i + K_j) mod 26
    Decryption: P_i = (C_i - K_j + 26) mod 26
    where j advances (mod len(K)) only when an alphabetic character is processed.

Character and Case Handling:
    - Uppercase letters remain uppercase.
    - Lowercase letters remain lowercase.
    - Spaces, punctuation, numbers, and symbols are preserved without modification,
      and do not consume a letter from the keystream.
"""

from src.validators import validate_text, validate_vigenere_key


def vigenere_encrypt(plaintext: str, key: str) -> str:
    """
    Encrypt plaintext using the Vigenère Cipher.
    
    Args:
        plaintext: The input text to encrypt.
        key: Alphabetic keyword.
        
    Returns:
        Encrypted ciphertext with case and punctuation preserved.
    """
    validate_text(plaintext, allow_empty=True)
    clean_key = validate_vigenere_key(key)
    
    key_len = len(clean_key)
    result = []
    k_idx = 0
    
    for char in plaintext:
        if 'A' <= char <= 'Z':
            shift = ord(clean_key[k_idx % key_len]) - ord('A')
            enc_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            result.append(enc_char)
            k_idx += 1
        elif 'a' <= char <= 'z':
            shift = ord(clean_key[k_idx % key_len]) - ord('A')
            enc_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            result.append(enc_char)
            k_idx += 1
        else:
            result.append(char)
            
    return "".join(result)


def vigenere_decrypt(ciphertext: str, key: str) -> str:
    """
    Decrypt ciphertext using the Vigenère Cipher.
    
    Args:
        ciphertext: The input ciphertext to decrypt.
        key: Alphabetic keyword used during encryption.
        
    Returns:
        Decrypted plaintext.
    """
    validate_text(ciphertext, allow_empty=True)
    clean_key = validate_vigenere_key(key)
    
    key_len = len(clean_key)
    result = []
    k_idx = 0
    
    for char in ciphertext:
        if 'A' <= char <= 'Z':
            shift = ord(clean_key[k_idx % key_len]) - ord('A')
            dec_char = chr((ord(char) - ord('A') - shift + 26) % 26 + ord('A'))
            result.append(dec_char)
            k_idx += 1
        elif 'a' <= char <= 'z':
            shift = ord(clean_key[k_idx % key_len]) - ord('A')
            dec_char = chr((ord(char) - ord('a') - shift + 26) % 26 + ord('a'))
            result.append(dec_char)
            k_idx += 1
        else:
            result.append(char)
            
    return "".join(result)
