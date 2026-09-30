"""
hill.py - Hill Cipher Implementation (2x2 and 3x3)
Design and Development of a Classical Cryptography Toolkit
Course: Network Security | Class: Final Year (ECM) 2026-27

Principle:
    Invented by Lester S. Hill in 1929, the Hill Cipher is a polygraphic substitution
    cipher based on linear algebra and modular arithmetic modulo 26.
    Plaintext is partitioned into vectors of length m and multiplied by an m x m key
    matrix K modulo 26.

Mathematical Formulation:
    Encryption: C = (P * K) mod 26
    Decryption: P = (C * K^(-1)) mod 26
    where P and C are 1 x m row vectors, and K is an m x m invertible matrix mod 26.

Key Requirements:
    - Matrix determinant det(K) mod 26 != 0.
    - gcd(det(K), 26) == 1 (coprime to 26). Because 26 = 2 * 13, det(K) cannot be
      divisible by 2 or 13.
    - If non-invertible, decryption is mathematically impossible; the toolkit strictly
      rejects invalid keys and explains why.
"""

from typing import List, Tuple, Union
import math
from src.validators import validate_text, parse_hill_key, ValidationError


def mod_inverse(a: int, m: int = 26) -> int:
    """
    Compute the modular multiplicative inverse of a modulo m.
    Returns x such that (a * x) % m == 1.
    """
    a = a % m
    try:
        return pow(a, -1, m)
    except (ValueError, TypeError):
        raise ValidationError(
            f"Modular inverse of {a} mod {m} does not exist because gcd({a}, {m}) = {math.gcd(a, m)} != 1."
        )


def get_hill_determinant(matrix: List[List[int]]) -> int:
    """Compute determinant of a 2x2 or 3x3 matrix."""
    n = len(matrix)
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    elif n == 3:
        a, b, c = matrix[0]
        d, e, f = matrix[1]
        g, h, i = matrix[2]
        return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)
    else:
        raise ValidationError(f"Only 2x2 and 3x3 matrices are supported. Got {n}x{n}.")


def invert_hill_matrix(matrix: List[List[int]]) -> List[List[int]]:
    """
    Compute the modular inverse of a 2x2 or 3x3 matrix modulo 26.
    
    Formula: K^(-1) = (det(K)^(-1) * adj(K)) mod 26
    """
    n = len(matrix)
    det = get_hill_determinant(matrix) % 26
    det_inv = mod_inverse(det, 26)
    
    if n == 2:
        # adj([a, b; c, d]) = [d, -b; -c, a]
        a, b = matrix[0][0], matrix[0][1]
        c, d = matrix[1][0], matrix[1][1]
        adj = [
            [d, -b],
            [-c, a]
        ]
        inv = [[(adj[r][col] * det_inv) % 26 for col in range(2)] for r in range(2)]
        return inv
    elif n == 3:
        a, b, c = matrix[0]
        d, e, f = matrix[1]
        g, h, i = matrix[2]
        
        # Minors & Cofactors transposed (Adjugate)
        adj = [
            [(e * i - f * h), -(b * i - c * h), (b * f - c * e)],
            [-(d * i - f * g), (a * i - c * g), -(a * f - c * d)],
            [(d * h - e * g), -(a * h - b * g), (a * e - b * d)]
        ]
        inv = [[(adj[r][col] * det_inv) % 26 for col in range(3)] for r in range(3)]
        return inv
    else:
        raise ValidationError(f"Matrix size {n}x{n} not supported.")


def hill_encrypt(plaintext: str, key: any, pad_char: str = 'X') -> str:
    """
    Encrypt plaintext using the Hill Cipher with a 2x2 or 3x3 matrix.
    
    Args:
        plaintext: The input text to encrypt.
        key: 4 or 9 integers / keyword string representing key matrix.
        pad_char: Character used to pad incomplete final block (default 'X').
        
    Returns:
        Ciphertext string in uppercase.
    """
    validate_text(plaintext, allow_empty=True)
    matrix = parse_hill_key(key)
    m = len(matrix)
    
    clean = [c.upper() for c in plaintext if c.isalpha()]
    if not clean:
        return ""
        
    # Pad if length is not a multiple of block size m
    while len(clean) % m != 0:
        clean.append(pad_char.upper())
        
    ciphertext_chars = []
    for i in range(0, len(clean), m):
        block = [ord(clean[i + j]) - ord('A') for j in range(m)]
        # Multiply row vector block by matrix K mod 26
        # C_j = sum(block[r] * matrix[r][j]) mod 26
        for col in range(m):
            val = sum(block[r] * matrix[r][col] for r in range(m)) % 26
            ciphertext_chars.append(chr(val + ord('A')))
            
    return "".join(ciphertext_chars)


def hill_decrypt(ciphertext: str, key: any) -> str:
    """
    Decrypt ciphertext using the Hill Cipher.
    
    Args:
        ciphertext: The input ciphertext.
        key: Key matrix representation.
        
    Returns:
        Decrypted plaintext string in uppercase.
    """
    validate_text(ciphertext, allow_empty=True)
    matrix = parse_hill_key(key)
    inv_matrix = invert_hill_matrix(matrix)
    m = len(matrix)
    
    clean = [c.upper() for c in ciphertext if c.isalpha()]
    if not clean:
        return ""
    if len(clean) % m != 0:
        raise ValidationError(f"Ciphertext length ({len(clean)}) must be a multiple of block size {m}.")
        
    plaintext_chars = []
    for i in range(0, len(clean), m):
        block = [ord(clean[i + j]) - ord('A') for j in range(m)]
        # Multiply row vector block by inverse matrix K^(-1) mod 26
        for col in range(m):
            val = sum(block[r] * inv_matrix[r][col] for r in range(m)) % 26
            plaintext_chars.append(chr(val + ord('A')))
            
    return "".join(plaintext_chars)
