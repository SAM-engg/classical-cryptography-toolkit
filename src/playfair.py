"""
playfair.py - Playfair Cipher Implementation
Design and Development of a Classical Cryptography Toolkit
Course: Network Security | Class: Final Year (ECM) 2026-27

Principle:
    The Playfair Cipher is the first practical digraphic substitution cipher, invented
    by Charles Wheatstone in 1854 and popularized by Lord Playfair. Instead of single
    letters, it encrypts pairs of letters (digraphs) using a 5x5 key matrix.

Key Matrix Construction:
    - 5x5 grid containing 25 letters of the English alphabet.
    - Standard convention: 'I' and 'J' share the same position (J is replaced by I).
    - Unique letters of the keyword appear first, followed by remaining alphabet letters.

Digraph Preparation Rules:
    1. Filter alphabetic characters and convert to uppercase; replace 'J' with 'I'.
    2. Split into pairs of 2 letters.
    3. If a pair contains identical letters (e.g., 'EE', 'LL'), insert a filler character
       'X' (or 'Q' if the repeated letter is 'X') between them.
    4. If the message has an odd length after pairing, append filler 'X' (or 'Z' if the
       last letter is 'X') to complete the final digraph.

Encryption / Decryption Rules:
    - Same Row: Shift right by 1 for encryption (wrap to col 0); shift left by 1 for decryption.
    - Same Column: Shift down by 1 for encryption (wrap to row 0); shift up by 1 for decryption.
    - Rectangle: Swap column coordinates; letter 1 takes (row1, col2) and letter 2 takes (row2, col1).
"""

from typing import List, Tuple, Dict
from src.validators import validate_text, validate_playfair_key


def generate_playfair_matrix(key: str) -> Tuple[List[List[str]], Dict[str, Tuple[int, int]]]:
    """
    Construct the 5x5 Playfair matrix and coordinate lookup map from key.
    
    Args:
        key: Keyword string.
        
    Returns:
        matrix: 5x5 nested list of characters.
        positions: Dictionary mapping each char to (row, col).
    """
    clean_key = validate_playfair_key(key)
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # Note: J is omitted, merged into I
    
    seen = set()
    grid_chars = []
    
    for char in clean_key:
        if char not in seen and char in alphabet:
            seen.add(char)
            grid_chars.append(char)
            
    for char in alphabet:
        if char not in seen:
            seen.add(char)
            grid_chars.append(char)
            
    matrix = [grid_chars[i * 5:(i + 1) * 5] for i in range(5)]
    positions = {matrix[r][c]: (r, c) for r in range(5) for c in range(5)}
    # Map J to the same coordinates as I
    positions['J'] = positions['I']
    
    return matrix, positions


def prepare_playfair_text(plaintext: str) -> List[Tuple[str, str]]:
    """
    Preprocess plaintext into valid Playfair digraphs according to classical rules:
    - Uppercase conversion and 'J' -> 'I'
    - Insert filler 'X' (or 'Q') between identical consecutive letters in a pair
    - Pad final single letter with 'X' (or 'Z')
    
    Returns:
        List of 2-character tuples [(c1, c2), ...].
    """
    clean = [c.upper().replace('J', 'I') for c in plaintext if c.isalpha()]
    if not clean:
        return []
        
    digraphs = []
    i = 0
    while i < len(clean):
        c1 = clean[i]
        if i + 1 < len(clean):
            c2 = clean[i + 1]
            if c1 == c2:
                # Repeated letter in digraph: insert filler
                filler = 'Q' if c1 == 'X' else 'X'
                digraphs.append((c1, filler))
                i += 1  # advance by 1 so c2 starts the next pair
            else:
                digraphs.append((c1, c2))
                i += 2
        else:
            # Odd single letter at end: pad with filler
            filler = 'Z' if c1 == 'X' else 'X'
            digraphs.append((c1, filler))
            i += 1
            
    return digraphs


def playfair_encrypt(plaintext: str, key: str, preserve_spacing: bool = False) -> str:
    """
    Encrypt plaintext using Playfair Cipher.
    
    Args:
        plaintext: The input text.
        key: Keyword string.
        preserve_spacing: If True, formats output with space between digraphs.
        
    Returns:
        Ciphertext string.
    """
    validate_text(plaintext, allow_empty=True)
    matrix, pos = generate_playfair_matrix(key)
    digraphs = prepare_playfair_text(plaintext)
    
    if not digraphs:
        return ""
        
    cipher_pairs = []
    for c1, c2 in digraphs:
        r1, col1 = pos[c1]
        r2, col2 = pos[c2]
        
        if r1 == r2:
            # Same row: shift right
            e1 = matrix[r1][(col1 + 1) % 5]
            e2 = matrix[r2][(col2 + 1) % 5]
        elif col1 == col2:
            # Same column: shift down
            e1 = matrix[(r1 + 1) % 5][col1]
            e2 = matrix[(r2 + 1) % 5][col2]
        else:
            # Rectangle: swap columns
            e1 = matrix[r1][col2]
            e2 = matrix[r2][col1]
            
        cipher_pairs.append(e1 + e2)
        
    sep = " " if preserve_spacing else ""
    return sep.join(cipher_pairs)


def playfair_decrypt(ciphertext: str, key: str, preserve_spacing: bool = False) -> str:
    """
    Decrypt ciphertext using Playfair Cipher.
    
    Args:
        ciphertext: The input ciphertext.
        key: Keyword string.
        preserve_spacing: If True, formats output with space between digraphs.
        
    Returns:
        Decrypted plaintext string (uppercase digraphs with fillers as generated).
    """
    validate_text(ciphertext, allow_empty=True)
    matrix, pos = generate_playfair_matrix(key)
    
    # Extract only alphabetic letters from ciphertext
    clean = [c.upper().replace('J', 'I') for c in ciphertext if c.isalpha()]
    if not clean:
        return ""
    if len(clean) % 2 != 0:
        clean.append('X')  # safety pad if malformed odd ciphertext provided
        
    plain_pairs = []
    for i in range(0, len(clean), 2):
        c1, c2 = clean[i], clean[i + 1]
        r1, col1 = pos[c1]
        r2, col2 = pos[c2]
        
        if r1 == r2:
            # Same row: shift left
            p1 = matrix[r1][(col1 - 1 + 5) % 5]
            p2 = matrix[r2][(col2 - 1 + 5) % 5]
        elif col1 == col2:
            # Same column: shift up
            p1 = matrix[(r1 - 1 + 5) % 5][col1]
            p2 = matrix[(r2 - 1 + 5) % 5][col2]
        else:
            # Rectangle: swap columns
            p1 = matrix[r1][col2]
            p2 = matrix[r2][col1]
            
        plain_pairs.append(p1 + p2)
        
    sep = " " if preserve_spacing else ""
    return sep.join(plain_pairs)
