"""
validators.py - Input and Key Validation Module
Design and Development of a Classical Cryptography Toolkit
Course: Network Security | Class: Final Year (ECM) 2026-27

This module provides validation functions for plaintext inputs, cipher keys,
and parameter configurations across all classical ciphers.
"""

from typing import Tuple, List, Optional
import math


class ValidationError(ValueError):
    """Custom exception raised when an input or key fails validation."""
    pass


def validate_text(text: str, allow_empty: bool = True) -> str:
    """
    Validate standard text input.
    
    Args:
        text: Input string.
        allow_empty: If False, raises ValidationError when string is empty.
        
    Returns:
        The validated text string.
    """
    if text is None:
        raise ValidationError("Input text cannot be None.")
    if not allow_empty and not text.strip():
        raise ValidationError("Input text cannot be empty or whitespace only.")
    return text


def validate_caesar_key(key: any) -> int:
    """
    Validate Caesar Cipher key.
    Must be an integer (shift factor).
    
    Args:
        key: Integer or string convertible to integer.
        
    Returns:
        Integer shift value normalized to 0-25.
    """
    if key is None or (isinstance(key, str) and not key.strip()):
        raise ValidationError("Caesar key cannot be empty. Please enter an integer shift value (e.g., 3, 5, 13).")
    try:
        val = int(str(key).strip())
    except ValueError:
        raise ValidationError(f"Invalid Caesar key '{key}'. Key must be a valid integer.")
    return val % 26


def validate_monoalphabetic_key(key: str) -> str:
    """
    Validate Monoalphabetic Substitution key.
    Accepts either:
    1. A full 26-letter substitution alphabet with unique A-Z characters.
    2. A keyword from which a 26-letter substitution alphabet will be derived.
    
    Returns:
        A validated 26-letter uppercase substitution alphabet.
    """
    if not key or not str(key).strip():
        raise ValidationError("Monoalphabetic key cannot be empty. Provide a 26-letter alphabet or a keyword.")
    
    clean_key = "".join([c.upper() for c in str(key) if c.isalpha()])
    if not clean_key:
        raise ValidationError("Monoalphabetic key must contain alphabetic letters.")
    
    if len(clean_key) == 26 and len(set(clean_key)) == 26:
        return clean_key
    elif len(clean_key) == 26 and len(set(clean_key)) < 26:
        duplicates = [c for c in clean_key if clean_key.count(c) > 1]
        raise ValidationError(f"26-letter key contains duplicate letters: {sorted(list(set(duplicates)))}. All 26 letters must be unique.")
    else:
        # Derive 26-letter alphabet from keyword
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        seen = set()
        derived = []
        for char in clean_key:
            if char not in seen:
                seen.add(char)
                derived.append(char)
        for char in alphabet:
            if char not in seen:
                seen.add(char)
                derived.append(char)
        return "".join(derived)


def validate_playfair_key(key: str) -> str:
    """
    Validate Playfair Cipher keyword.
    
    Args:
        key: Keyword string.
        
    Returns:
        Cleaned uppercase alphabetic keyword (with J replaced by I).
    """
    if not key or not str(key).strip():
        raise ValidationError("Playfair keyword cannot be empty. Enter an alphabetic keyword (e.g., 'MONARCHY').")
    clean = "".join([c.upper() for c in str(key) if c.isalpha()])
    if not clean:
        raise ValidationError("Playfair keyword must contain at least one alphabetic character.")
    return clean.replace('J', 'I')


def validate_vigenere_key(key: str) -> str:
    """
    Validate Vigenere Cipher keyword.
    
    Args:
        key: Keyword string.
        
    Returns:
        Cleaned uppercase alphabetic keyword.
    """
    if not key or not str(key).strip():
        raise ValidationError("Vigenère key cannot be empty. Please enter an alphabetic keyword (e.g., 'CIPHER').")
    clean = "".join([c.upper() for c in str(key) if c.isalpha()])
    if not clean:
        raise ValidationError("Vigenère key must contain at least one alphabetic character (A-Z).")
    return clean


def parse_hill_key(key: any) -> List[List[int]]:
    """
    Parse and validate a Hill Cipher key matrix (2x2 or 3x3).
    Supports:
    - 4-letter or 9-letter keyword (e.g. 'HILL' -> 2x2, 'GYBNQKURP' -> 3x3)
    - Comma or space separated integers (e.g. '3 3 2 5' -> 2x2, '6 24 1 13 16 10 20 17 15' -> 3x3)
    
    Returns:
        Nested list representation of the square matrix modulo 26.
    """
    if not key or not str(key).strip():
        raise ValidationError("Hill key cannot be empty. Provide a 4-letter keyword, 9-letter keyword, or 4 / 9 integers.")
    
    raw = str(key).strip()
    
    # Try parsing as numbers first
    # Replace commas, semicolons, brackets, newlines with space
    cleaned_num_str = raw.replace(',', ' ').replace(';', ' ').replace('[', ' ').replace(']', ' ')
    tokens = cleaned_num_str.split()
    
    numbers = []
    is_numeric = True
    for token in tokens:
        try:
            numbers.append(int(token))
        except ValueError:
            is_numeric = False
            break
            
    if is_numeric and len(numbers) in (4, 9):
        size = int(math.isqrt(len(numbers)))
        matrix = [[numbers[r * size + c] % 26 for c in range(size)] for r in range(size)]
    else:
        # Try alphabetic keyword
        alpha_chars = [c.upper() for c in raw if c.isalpha()]
        if len(alpha_chars) == 4:
            size = 2
            matrix = [
                [ord(alpha_chars[0]) - ord('A'), ord(alpha_chars[1]) - ord('A')],
                [ord(alpha_chars[2]) - ord('A'), ord(alpha_chars[3]) - ord('A')]
            ]
        elif len(alpha_chars) == 9:
            size = 3
            matrix = [
                [ord(alpha_chars[r * 3 + c]) - ord('A') for c in range(3)]
                for r in range(3)
            ]
        else:
            raise ValidationError(
                f"Invalid Hill Cipher key '{raw}'. Must be either:\n"
                "- 4 or 9 integers (e.g., '3 3 2 5' for 2x2 or '6 24 1 13 16 10 20 17 15' for 3x3)\n"
                "- 4 or 9 alphabetic characters (e.g., 'HILL' for 2x2 or 'GYBNQKURP' for 3x3)."
            )
            
    # Validate invertibility modulo 26
    det = compute_matrix_determinant(matrix) % 26
    if det == 0:
        raise ValidationError(f"Matrix determinant is 0 mod 26. Matrix is singular and cannot be inverted.")
    gcd_val = math.gcd(det, 26)
    if gcd_val != 1:
        raise ValidationError(
            f"Matrix determinant det(K) = {det} is not coprime to 26 (gcd({det}, 26) = {gcd_val} != 1).\n"
            f"A valid Hill Cipher key must have gcd(det(K), 26) == 1 to allow modular inversion for decryption."
        )
        
    return matrix


def compute_matrix_determinant(matrix: List[List[int]]) -> int:
    """Compute standard determinant of 2x2 or 3x3 matrix."""
    n = len(matrix)
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    elif n == 3:
        a, b, c = matrix[0]
        d, e, f = matrix[1]
        g, h, i = matrix[2]
        return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)
    else:
        raise ValidationError(f"Unsupported matrix size {n}x{n}. Only 2x2 and 3x3 are supported.")


def validate_one_time_pad_key(key: str, required_length: int) -> str:
    """
    Validate One-Time Pad key.
    
    Args:
        key: The key string.
        required_length: Number of alphabetic letters required.
        
    Returns:
        Cleaned uppercase alphabetic key.
    """
    if not key or not str(key).strip():
        raise ValidationError("One-Time Pad key cannot be empty. Generate or supply a random key.")
    clean = "".join([c.upper() for c in str(key) if c.isalpha()])
    if len(clean) != required_length:
        raise ValidationError(
            f"One-Time Pad key length mismatch: Key has {len(clean)} alphabetic characters, "
            f"but message requires exactly {required_length} characters.\n"
            f"Rule: In classical OTP, len(Key) == len(Plaintext)."
        )
    return clean


def validate_rail_fence_key(key: any) -> int:
    """
    Validate Rail Fence Cipher key (number of rails/depth).
    
    Args:
        key: Integer or string convertible to integer.
        
    Returns:
        Integer depth >= 2.
    """
    if key is None or (isinstance(key, str) and not key.strip()):
        raise ValidationError("Rail Fence key cannot be empty. Enter number of rails >= 2 (e.g., 2, 3, 4).")
    try:
        rails = int(str(key).strip())
    except ValueError:
        raise ValidationError(f"Invalid Rail Fence key '{key}'. Rails must be an integer.")
    if rails < 2:
        raise ValidationError(f"Number of rails must be at least 2. Provided: {rails}.")
    return rails


def validate_columnar_key(key: str) -> List[int]:
    """
    Validate Columnar Transposition key.
    Accepts:
    1. Keyword (e.g. 'ZEBRA', 'HACK') - column order determined by alphabetical order of letters.
    2. Numeric permutation (e.g. '3 1 4 2' or '3,1,4,2' or '3142' if 1-indexed).
    
    Returns:
        0-indexed column permutation list.
    """
    if not key or not str(key).strip():
        raise ValidationError("Columnar Transposition key cannot be empty. Enter a keyword (e.g. 'ZEBRA') or numeric order (e.g. '3 1 4 2').")
    
    raw = str(key).strip()
    
    # Check if purely numbers
    cleaned_num = raw.replace(',', ' ').replace(';', ' ')
    tokens = cleaned_num.split()
    if tokens and all(t.isdigit() for t in tokens) and len(tokens) > 1:
        nums = [int(t) for t in tokens]
        min_v, max_v = min(nums), max(nums)
        # Check if 1-indexed permutation: 1..N
        if set(nums) == set(range(1, len(nums) + 1)):
            return [x - 1 for x in nums]
        # Check if 0-indexed permutation: 0..N-1
        if set(nums) == set(range(0, len(nums))):
            return nums
        raise ValidationError(
            f"Numeric key must be a permutation of 1..{len(nums)} or 0..{len(nums)-1}. Provided: {nums}"
        )
    
    # Check alphabetic keyword
    clean_alpha = "".join([c.upper() for c in raw if c.isalpha()])
    if len(clean_alpha) < 2:
        raise ValidationError("Columnar keyword must be at least 2 alphabetic characters long.")
    
    # Alphabetical order with stable sorting for duplicates
    indexed_chars = sorted([(c, idx) for idx, c in enumerate(clean_alpha)], key=lambda x: (x[0], x[1]))
    # Map original index to order rank (0..len-1)
    # Order: the column that comes first alphabetically is read first
    # So the order of columns to read is [orig_idx for (char, orig_idx) in indexed_chars]
    return [idx for (_, idx) in indexed_chars]
