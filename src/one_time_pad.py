"""
one_time_pad.py - One-Time Pad (Vernam Cipher) Implementation
Design and Development of a Classical Cryptography Toolkit
Course: Network Security | Class: Final Year (ECM) 2026-27

Principle:
    Invented by Gilbert Vernam in 1917 and mathematically proven unbreakable by
    Claude Shannon in 1949, the One-Time Pad (OTP) offers Information-Theoretic
    Security (perfect secrecy) under four mandatory physical requirements:
    1. Key must be truly uniformly random (high entropy, CSPRNG).
    2. Key must be at least as long as the plaintext message.
    3. Key must be kept strictly secret by sender and receiver.
    4. Key must be used ONCE and NEVER reused (two-time pad vulnerability enables
       frequency-based crib dragging: C1 - C2 = P1 - P2).

Implementation Details:
    - Classical alphabet modulo-26 scheme: C_i = (P_i + K_i) mod 26.
    - Generates cryptographically secure keys using Python's `secrets` module.
    - Preserves spaces and punctuation, aligning one key character per alphabetic character.
    - Enforces exact key length: len(key) must match alphabetic character count.
"""

import secrets
from typing import Tuple
from src.validators import validate_text, validate_one_time_pad_key, ValidationError


ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def generate_otp_key(length: int) -> str:
    """
    Generate a cryptographically secure random key of specified length using secrets.
    
    Args:
        length: Number of random A-Z characters required.
        
    Returns:
        Uppercase string of random A-Z letters.
    """
    if length <= 0:
        return ""
    return "".join(secrets.choice(ALPHABET) for _ in range(length))


def count_alphabetic_characters(text: str) -> int:
    """Count number of alphabetic letters in string."""
    return sum(1 for c in text if c.isalpha())


def otp_encrypt(plaintext: str, key: str = None) -> Tuple[str, str]:
    """
    Encrypt plaintext using the classical alphabet-based One-Time Pad.
    
    Args:
        plaintext: The input text to encrypt.
        key: Key string. If None or empty, a secure random key of exact length is generated.
        
    Returns:
        Tuple of (ciphertext, key_used).
    """
    validate_text(plaintext, allow_empty=True)
    alpha_count = count_alphabetic_characters(plaintext)
    
    if alpha_count == 0:
        return plaintext, ""
        
    if key is None or not str(key).strip():
        # Auto-generate secure random key of matching length
        valid_key = generate_otp_key(alpha_count)
    else:
        valid_key = validate_one_time_pad_key(key, alpha_count)
        
    result = []
    k_idx = 0
    
    for char in plaintext:
        if 'A' <= char <= 'Z':
            shift = ord(valid_key[k_idx]) - ord('A')
            enc_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            result.append(enc_char)
            k_idx += 1
        elif 'a' <= char <= 'z':
            shift = ord(valid_key[k_idx]) - ord('A')
            enc_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            result.append(enc_char)
            k_idx += 1
        else:
            result.append(char)
            
    return "".join(result), valid_key


def otp_decrypt(ciphertext: str, key: str) -> str:
    """
    Decrypt ciphertext using One-Time Pad.
    
    Args:
        ciphertext: The input ciphertext.
        key: The exact key used for encryption.
        
    Returns:
        Decrypted plaintext.
    """
    validate_text(ciphertext, allow_empty=True)
    alpha_count = count_alphabetic_characters(ciphertext)
    
    if alpha_count == 0:
        return ciphertext
        
    valid_key = validate_one_time_pad_key(key, alpha_count)
    
    result = []
    k_idx = 0
    
    for char in ciphertext:
        if 'A' <= char <= 'Z':
            shift = ord(valid_key[k_idx]) - ord('A')
            dec_char = chr((ord(char) - ord('A') - shift + 26) % 26 + ord('A'))
            result.append(dec_char)
            k_idx += 1
        elif 'a' <= char <= 'z':
            shift = ord(valid_key[k_idx]) - ord('A')
            dec_char = chr((ord(char) - ord('a') - shift + 26) % 26 + ord('a'))
            result.append(dec_char)
            k_idx += 1
        else:
            result.append(char)
            
    return "".join(result)
