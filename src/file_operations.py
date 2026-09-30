"""
file_operations.py - File I/O and Text File Encryption/Decryption Module
Design and Development of a Classical Cryptography Toolkit
Course: Network Security | Class: Final Year (ECM) 2026-27

This module handles:
1. Safe loading and encoding verification (UTF-8) of text files.
2. Graceful handling of empty files, missing files, permission errors, and binary encoding.
3. Encryption and decryption of file content using any selected classical cipher.
4. Preview generation without mutating source files.
5. Safe saving of results to a user-chosen target file without overwriting the input file.

Security Notice:
    Classical ciphers are strictly for educational demonstrations. They provide
    zero modern cryptographic security and must NEVER be used to protect confidential,
    financial, medical, or personal user data.
"""

import os
from typing import Dict, Any, Tuple

from src.caesar import caesar_encrypt, caesar_decrypt
from src.monoalphabetic import monoalphabetic_encrypt, monoalphabetic_decrypt
from src.playfair import playfair_encrypt, playfair_decrypt
from src.hill import hill_encrypt, hill_decrypt
from src.vigenere import vigenere_encrypt, vigenere_decrypt
from src.one_time_pad import otp_encrypt, otp_decrypt
from src.rail_fence import rail_fence_encrypt, rail_fence_decrypt
from src.columnar_transposition import columnar_encrypt, columnar_decrypt
from src.validators import ValidationError


class FileOperationError(Exception):
    """Custom exception raised for file operation failures."""
    pass


def read_text_file(filepath: str, max_chars: int = 200000) -> Tuple[str, Dict[str, Any]]:
    """
    Safely read text from a file with UTF-8 encoding.
    
    Args:
        filepath: Path to the target text file.
        max_chars: Upper boundary on characters read to prevent memory exhaustion.
        
    Returns:
        Tuple of (content_string, metadata_dict).
    """
    if not filepath or not os.path.exists(filepath):
        raise FileOperationError(f"File not found: '{filepath}'. Please verify the path.")
        
    if not os.path.isfile(filepath):
        raise FileOperationError(f"Target path '{filepath}' is a directory, not a regular text file.")
        
    file_size = os.path.getsize(filepath)
    if file_size == 0:
        raise FileOperationError(f"The file '{os.path.basename(filepath)}' is completely empty (0 bytes).")
        
    # Read with UTF-8 encoding; fallback with informative message
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read(max_chars)
    except UnicodeDecodeError:
        try:
            # Fallback attempt with utf-8-sig (handles BOM) or latin-1
            with open(filepath, 'r', encoding='utf-8-sig') as f:
                content = f.read(max_chars)
        except Exception:
            raise FileOperationError(
                f"File '{os.path.basename(filepath)}' is not a valid UTF-8 text file. "
                f"Binary files (e.g. .exe, .pdf, images) are not supported by classical text ciphers."
            )
    except PermissionError:
        raise FileOperationError(f"Permission denied when attempting to read '{filepath}'.")
    except Exception as exc:
        raise FileOperationError(f"Unexpected error reading file: {str(exc)}")
        
    metadata = {
        "filename": os.path.basename(filepath),
        "filepath": filepath,
        "filesize_bytes": file_size,
        "char_count": len(content),
        "is_truncated": (file_size > max_chars)
    }
    
    return content, metadata


def write_text_file(filepath: str, content: str, allow_overwrite: bool = True) -> int:
    """
    Safely write text content to a destination file.
    
    Args:
        filepath: Destination file path.
        content: Text content to write.
        allow_overwrite: Whether overwriting an existing file is permitted.
        
    Returns:
        Number of characters written.
    """
    if not filepath:
        raise FileOperationError("Destination filepath cannot be empty.")
        
    if os.path.exists(filepath) and not allow_overwrite:
        raise FileOperationError(f"Destination file '{filepath}' already exists and overwrite is disabled.")
        
    # Ensure directory exists
    dir_path = os.path.dirname(filepath)
    if dir_path and not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)
        
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return len(content)
    except PermissionError:
        raise FileOperationError(f"Permission denied when writing to '{filepath}'.")
    except Exception as exc:
        raise FileOperationError(f"Error saving file: {str(exc)}")


def process_file_cipher(
    content: str,
    cipher_name: str,
    key: Any,
    mode: str = "encrypt"
) -> Tuple[str, str]:
    """
    Encrypt or decrypt content string using the specified cipher and key.
    
    Args:
        content: Text to process.
        cipher_name: Name of cipher.
        key: Key value.
        mode: 'encrypt' or 'decrypt'.
        
    Returns:
        Tuple of (output_text, extra_info_string).
    """
    extra_info = ""
    is_encrypt = (mode.lower() == "encrypt")
    
    if cipher_name == "Caesar Cipher":
        output = caesar_encrypt(content, key) if is_encrypt else caesar_decrypt(content, key)
        
    elif cipher_name == "Monoalphabetic Cipher":
        output = monoalphabetic_encrypt(content, key) if is_encrypt else monoalphabetic_decrypt(content, key)
        
    elif cipher_name == "Playfair Cipher":
        if is_encrypt:
            output = playfair_encrypt(content, key)
            extra_info = "Note: Digraphs processed; non-alphabetics stripped, J replaced by I."
        else:
            output = playfair_decrypt(content, key)
            
    elif cipher_name == "Hill Cipher":
        if is_encrypt:
            output = hill_encrypt(content, key)
            extra_info = "Note: Block padding applied if needed; alphabetic characters encrypted."
        else:
            output = hill_decrypt(content, key)
            
    elif cipher_name == "Vigenere Cipher":
        output = vigenere_encrypt(content, key) if is_encrypt else vigenere_decrypt(content, key)
        
    elif cipher_name == "One-Time Pad":
        if is_encrypt:
            output, key_used = otp_encrypt(content, key)
            extra_info = f"One-Time Pad Key: {key_used}"
        else:
            output = otp_decrypt(content, key)
            
    elif cipher_name == "Rail Fence Cipher":
        output = rail_fence_encrypt(content, key) if is_encrypt else rail_fence_decrypt(content, key)
        
    elif cipher_name == "Columnar Transposition Cipher":
        output = columnar_encrypt(content, key) if is_encrypt else columnar_decrypt(content, key)
        
    else:
        raise ValidationError(f"Unrecognized cipher selection '{cipher_name}'.")
        
    return output, extra_info
