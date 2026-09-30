"""
caesar.py - Caesar Cipher Implementation
Design and Development of a Classical Cryptography Toolkit
Course: Network Security | Class: Final Year (ECM) 2026-27

Principle:
    The Caesar Cipher is a monoalphabetic substitution cipher where each letter in
    the plaintext is shifted forward by a fixed number of positions (k) in the alphabet.
    Decryption involves shifting backwards by the same key value k.

Mathematical Formulation:
    Encryption: C_i = (P_i + k) mod 26
    Decryption: P_i = (C_i - k + 26) mod 26
    where P_i and C_i are the 0-indexed positions of characters (A=0, ..., Z=25).

Character and Case Handling:
    - Uppercase letters (A-Z) wrap within 'A' through 'Z'.
    - Lowercase letters (a-z) wrap within 'a' through 'z'.
    - Spaces, punctuation, numbers, and symbols are preserved unchanged.

Demonstration Note:
    Plaintext: "NETWORK SECURITY" with Key: 5
    - NETWORK  -> S J Y B T W P  (N+5=S, E+5=J, T+5=Y, W+5=B, O+5=T, R+5=W, K+5=P)
    - SECURITY -> X J H Z W N Y D (S+5=X, E+5=J, C+5=H, U+5=Z, R+5=W, I+5=N, T+5=Y, Y+5=D)
    - Ciphertext: "SJYBTWP XJHZWNYD"
    (Note: Some historical problem sheets contain a typographical error 'SJYBTW P XJHZWNYD'
     introducing an erroneous space in 'NETWORK'; the mathematically correct output
     preserving word boundaries is 'SJYBTWP XJHZWNYD'.)
"""

from src.validators import validate_text, validate_caesar_key


def caesar_encrypt(plaintext: str, key: any) -> str:
    """
    Encrypt plaintext using the Caesar Cipher.
    
    Args:
        plaintext: The input text to encrypt.
        key: Integer shift key (or string convertible to int).
        
    Returns:
        The encrypted ciphertext string.
    """
    validate_text(plaintext, allow_empty=True)
    k = validate_caesar_key(key)
    
    result = []
    for char in plaintext:
        if 'A' <= char <= 'Z':
            shift_c = chr((ord(char) - ord('A') + k) % 26 + ord('A'))
            result.append(shift_c)
        elif 'a' <= char <= 'z':
            shift_c = chr((ord(char) - ord('a') + k) % 26 + ord('a'))
            result.append(shift_c)
        else:
            result.append(char)
            
    return "".join(result)


def caesar_decrypt(ciphertext: str, key: any) -> str:
    """
    Decrypt ciphertext using the Caesar Cipher.
    
    Args:
        ciphertext: The input ciphertext to decrypt.
        key: Integer shift key (or string convertible to int).
        
    Returns:
        The decrypted plaintext string.
    """
    validate_text(ciphertext, allow_empty=True)
    k = validate_caesar_key(key)
    return caesar_encrypt(ciphertext, -k)
