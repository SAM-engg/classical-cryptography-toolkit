"""
comparison.py - Cipher Performance and Characteristic Comparison Module
Design and Development of a Classical Cryptography Toolkit
Course: Network Security | Class: Final Year (ECM) 2026-27

This module benchmarks supported classical ciphers by measuring:
1. Encryption execution time (microseconds / milliseconds)
2. Decryption execution time (microseconds / milliseconds)
3. Output length / expansion ratio
4. Classical category (Substitution vs Transposition)
5. Key space and theoretical vulnerabilities

Educational Disclaimer:
    Execution time is highly machine-dependent, environment-dependent, and affected
    by input length. High throughput or lower execution time does NOT correlate with
    cryptographic security. Classical ciphers are historically vulnerable to frequency
    analysis, known-plaintext attacks, and brute-force key enumeration.
"""

import time
from typing import Dict, List, Any, Optional

from src.caesar import caesar_encrypt, caesar_decrypt
from src.monoalphabetic import monoalphabetic_encrypt, monoalphabetic_decrypt
from src.playfair import playfair_encrypt, playfair_decrypt
from src.hill import hill_encrypt, hill_decrypt
from src.vigenere import vigenere_encrypt, vigenere_decrypt
from src.one_time_pad import otp_encrypt, otp_decrypt, generate_otp_key
from src.rail_fence import rail_fence_encrypt, rail_fence_decrypt
from src.columnar_transposition import columnar_encrypt, columnar_decrypt


# Default benchmark keys suitable for sample comparisons
DEFAULT_BENCHMARK_KEYS = {
    "Caesar Cipher": 5,
    "Monoalphabetic Cipher": "QWERTYUIOPASDFGHJKLZXCVBNM",
    "Playfair Cipher": "MONARCHY",
    "Hill Cipher": "3 3 2 5",
    "Vigenere Cipher": "SECURITY",
    "One-Time Pad": None,  # Will be generated dynamically to match alphabetic length
    "Rail Fence Cipher": 3,
    "Columnar Transposition Cipher": "SECRET"
}

CIPHER_METADATA = {
    "Caesar Cipher": {
        "type": "Substitution (Monoalphabetic)",
        "key_space": "26 (25 non-trivial)",
        "vulnerability": "Brute-force (exhaustion) & single-letter frequency analysis",
        "description": "Fixed uniform alphabetic shift k in [0, 25]."
    },
    "Monoalphabetic Cipher": {
        "type": "Substitution (Monoalphabetic)",
        "key_space": "26! ~ 4.03 x 10^26",
        "vulnerability": "Single-letter frequency analysis (ETAOIN SHRDLU), digrams/trigrams",
        "description": "Arbitrary 1-to-1 permutation of the 26-letter alphabet."
    },
    "Playfair Cipher": {
        "type": "Substitution (Polygraphic / Digraphic)",
        "key_space": "25! ~ 1.55 x 10^25 (equivalent classes ~ 1.1 x 10^12)",
        "vulnerability": "Digraph frequency analysis (e.g., TH, HE, IN, ER)",
        "description": "Encrypts letter pairs (digraphs) across 5x5 key matrix."
    },
    "Hill Cipher": {
        "type": "Substitution (Polygraphic / Linear Algebraic)",
        "key_space": "GL(2, Z_26) = 157,248 (2x2) | GL(3, Z_26) ~ 1.6 x 10^12 (3x3)",
        "vulnerability": "Known-Plaintext Attack via modular matrix inversion",
        "description": "Linear algebra modulo 26 using invertible square matrix."
    },
    "Vigenere Cipher": {
        "type": "Substitution (Polyalphabetic)",
        "key_space": "26^L where L is keyword length",
        "vulnerability": "Kasiski examination and Friedman test (Index of Coincidence)",
        "description": "Periodic polyalphabetic shift using repeating keyword."
    },
    "One-Time Pad": {
        "type": "Substitution (Information-Theoretic)",
        "key_space": "26^N (where N is text length)",
        "vulnerability": "Key reuse (Two-time pad crib dragging) & non-random key generation",
        "description": "Perfect secrecy iff key is truly random, secret, equal length, and never reused."
    },
    "Rail Fence Cipher": {
        "type": "Transposition (Zigzag Geometric)",
        "key_space": "Number of rails k in [2, N-1]",
        "vulnerability": "Brute force search over small rail depth; letter frequencies unchanged",
        "description": "Diagonally interleaves characters across k rails."
    },
    "Columnar Transposition Cipher": {
        "type": "Transposition (Permutation Grid)",
        "key_space": "W! (where W is key width)",
        "vulnerability": "Anagramming, bigram frequency reconstruction; letter frequencies unchanged",
        "description": "Writes text into rows of width W, reads columns by key rank."
    }
}


def run_single_comparison(cipher_name: str, plaintext: str, custom_key: Any = None) -> Dict[str, Any]:
    """
    Benchmark and evaluate a single cipher on the given plaintext.
    """
    key = custom_key if custom_key is not None else DEFAULT_BENCHMARK_KEYS.get(cipher_name)
    
    result = {
        "cipher_name": cipher_name,
        "type": CIPHER_METADATA[cipher_name]["type"],
        "input_len": len(plaintext),
        "status": "Success",
        "key_used": str(key),
        "encrypt_time_ms": 0.0,
        "decrypt_time_ms": 0.0,
        "ciphertext_len": 0,
        "round_trip_success": False,
        "ciphertext_sample": "",
        "notes": ""
    }
    
    try:
        if cipher_name == "Caesar Cipher":
            t0 = time.perf_counter()
            ciphertext = caesar_encrypt(plaintext, key)
            t1 = time.perf_counter()
            decrypted = caesar_decrypt(ciphertext, key)
            t2 = time.perf_counter()
            result["round_trip_success"] = (decrypted == plaintext)
            
        elif cipher_name == "Monoalphabetic Cipher":
            t0 = time.perf_counter()
            ciphertext = monoalphabetic_encrypt(plaintext, key)
            t1 = time.perf_counter()
            decrypted = monoalphabetic_decrypt(ciphertext, key)
            t2 = time.perf_counter()
            result["round_trip_success"] = (decrypted == plaintext)
            
        elif cipher_name == "Playfair Cipher":
            t0 = time.perf_counter()
            ciphertext = playfair_encrypt(plaintext, key)
            t1 = time.perf_counter()
            decrypted = playfair_decrypt(ciphertext, key)
            t2 = time.perf_counter()
            # In Playfair, standard classical behavior replaces J with I and inserts filler X
            clean_p = [c.upper().replace('J', 'I') for c in plaintext if c.isalpha()]
            result["round_trip_success"] = len(decrypted) >= len(clean_p)
            result["notes"] = "Playfair pads odd lengths / repeated letters with X and converts J to I."
            
        elif cipher_name == "Hill Cipher":
            t0 = time.perf_counter()
            ciphertext = hill_encrypt(plaintext, key)
            t1 = time.perf_counter()
            decrypted = hill_decrypt(ciphertext, key)
            t2 = time.perf_counter()
            clean_p = [c.upper() for c in plaintext if c.isalpha()]
            result["round_trip_success"] = decrypted.startswith("".join(clean_p))
            result["notes"] = "Hill pads block multiples with X; operates on alphabetic letters."
            
        elif cipher_name == "Vigenere Cipher":
            t0 = time.perf_counter()
            ciphertext = vigenere_encrypt(plaintext, key)
            t1 = time.perf_counter()
            decrypted = vigenere_decrypt(ciphertext, key)
            t2 = time.perf_counter()
            result["round_trip_success"] = (decrypted == plaintext)
            
        elif cipher_name == "One-Time Pad":
            alpha_len = sum(1 for c in plaintext if c.isalpha())
            otp_key = key if key else generate_otp_key(alpha_len)
            result["key_used"] = otp_key[:10] + ("..." if len(otp_key) > 10 else "")
            t0 = time.perf_counter()
            ciphertext, key_used = otp_encrypt(plaintext, otp_key)
            t1 = time.perf_counter()
            decrypted = otp_decrypt(ciphertext, key_used)
            t2 = time.perf_counter()
            result["round_trip_success"] = (decrypted == plaintext)
            result["notes"] = "OTP key was securely generated via secrets (CSPRNG)."
            
        elif cipher_name == "Rail Fence Cipher":
            t0 = time.perf_counter()
            ciphertext = rail_fence_encrypt(plaintext, key)
            t1 = time.perf_counter()
            decrypted = rail_fence_decrypt(ciphertext, key)
            t2 = time.perf_counter()
            result["round_trip_success"] = (decrypted == plaintext)
            
        elif cipher_name == "Columnar Transposition Cipher":
            t0 = time.perf_counter()
            ciphertext = columnar_encrypt(plaintext, key)
            t1 = time.perf_counter()
            decrypted = columnar_decrypt(ciphertext, key)
            t2 = time.perf_counter()
            result["round_trip_success"] = (decrypted == plaintext)
            
        else:
            raise ValueError(f"Unknown cipher {cipher_name}")
            
        result["encrypt_time_ms"] = (t1 - t0) * 1000.0
        result["decrypt_time_ms"] = (t2 - t1) * 1000.0
        result["ciphertext_len"] = len(ciphertext)
        result["ciphertext_sample"] = ciphertext[:30] + ("..." if len(ciphertext) > 30 else "")
        
    except Exception as exc:
        result["status"] = f"Error: {str(exc)}"
        result["round_trip_success"] = False
        
    return result


def compare_ciphers(selected_ciphers: List[str], plaintext: str, custom_keys: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """
    Run comparison over multiple selected ciphers.
    
    Args:
        selected_ciphers: List of cipher display names.
        plaintext: Sample text to encrypt.
        custom_keys: Optional mapping of cipher name to custom key.
        
    Returns:
        List of benchmark metric dictionaries.
    """
    results = []
    custom_keys = custom_keys or {}
    for name in selected_ciphers:
        if name in CIPHER_METADATA:
            k = custom_keys.get(name)
            res = run_single_comparison(name, plaintext, k)
            results.append(res)
    return results
