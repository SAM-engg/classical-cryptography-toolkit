"""
rail_fence.py - Rail Fence (Zigzag) Transposition Cipher Implementation
Design and Development of a Classical Cryptography Toolkit
Course: Network Security | Class: Final Year (ECM) 2026-27

Principle:
    The Rail Fence Cipher is a form of transposition cipher that gets its name from
    the way the letters are written down in a zigzag pattern across a given number
    of parallel rails (depth k), and then read off horizontally row by row.

Mathematical Pattern:
    - Cycle length: T = 2 * (k - 1) for k >= 2.
    - For index i, rail index is:
        rail(i) = i % T if (i % T) < k else T - (i % T)
    - Full round-trip reversibility preserves exact characters including spaces,
      newlines, and punctuation.
"""

from src.validators import validate_text, validate_rail_fence_key


def rail_fence_encrypt(plaintext: str, key: any) -> str:
    """
    Encrypt plaintext using the Rail Fence Cipher.
    
    Args:
        plaintext: The input text.
        key: Number of rails (integer >= 2).
        
    Returns:
        Ciphertext string.
    """
    validate_text(plaintext, allow_empty=True)
    rails = validate_rail_fence_key(key)
    
    n = len(plaintext)
    if n <= 1 or rails >= n:
        return plaintext
        
    cycle = 2 * (rails - 1)
    fence = [[] for _ in range(rails)]
    
    for i, char in enumerate(plaintext):
        pos = i % cycle
        rail = pos if pos < rails else cycle - pos
        fence[rail].append(char)
        
    return "".join("".join(row) for row in fence)


def rail_fence_decrypt(ciphertext: str, key: any) -> str:
    """
    Decrypt ciphertext using the Rail Fence Cipher.
    
    Args:
        ciphertext: The input ciphertext.
        key: Number of rails (integer >= 2).
        
    Returns:
        Decrypted plaintext.
    """
    validate_text(ciphertext, allow_empty=True)
    rails = validate_rail_fence_key(key)
    
    n = len(ciphertext)
    if n <= 1 or rails >= n:
        return ciphertext
        
    cycle = 2 * (rails - 1)
    
    # Step 1: Mark the zigzag path with placeholder True
    matrix = [[False] * n for _ in range(rails)]
    for i in range(n):
        pos = i % cycle
        rail = pos if pos < rails else cycle - pos
        matrix[rail][i] = True
        
    # Step 2: Fill the marked spots with ciphertext characters row by row
    char_idx = 0
    filled = [[''] * n for _ in range(rails)]
    for r in range(rails):
        for c in range(n):
            if matrix[r][c] and char_idx < n:
                filled[r][c] = ciphertext[char_idx]
                char_idx += 1
                
    # Step 3: Read characters following original zigzag order
    result = []
    for i in range(n):
        pos = i % cycle
        rail = pos if pos < rails else cycle - pos
        result.append(filled[rail][i])
        
    return "".join(result)
