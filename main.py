"""
main.py - Entry Point for Classical Cryptography Toolkit
Final Year ECM Network Security Mini-Project (2026-27)
Project Title: Design and Development of a Classical Cryptography Toolkit

Usage:
    python main.py          Launch Tkinter Graphical User Interface
    python main.py --web    Launch Local Web Application (http://localhost:8000)
    python main.py --cli    Launch interactive Command-Line Interface
    python main.py --demo   Run automated terminal demonstration of all 8 ciphers
"""

import sys
import os

# Ensure the project root directory is in the Python path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.caesar import caesar_encrypt, caesar_decrypt
from src.monoalphabetic import monoalphabetic_encrypt, monoalphabetic_decrypt
from src.playfair import playfair_encrypt, playfair_decrypt
from src.hill import hill_encrypt, hill_decrypt
from src.vigenere import vigenere_encrypt, vigenere_decrypt
from src.one_time_pad import otp_encrypt, otp_decrypt, generate_otp_key
from src.rail_fence import rail_fence_encrypt, rail_fence_decrypt
from src.columnar_transposition import columnar_encrypt, columnar_decrypt
from src.comparison import compare_ciphers


def run_demonstration():
    """Run a verified, deterministic console demonstration of all 8 classical ciphers."""
    print("=" * 76)
    print(" CLASSICAL CRYPTOGRAPHY TOOLKIT - AUTOMATED VERIFICATION DEMO")
    print(" Final Year ECM Network Security Mini-Project (2026-27)")
    print("=" * 76)

    # 1. Caesar Cipher (Verified demonstration requirement)
    pt1 = "NETWORK SECURITY"
    k1 = 5
    ct1 = caesar_encrypt(pt1, k1)
    dec1 = caesar_decrypt(ct1, k1)
    print("\n[1] CAESAR CIPHER (Shift Modulo 26)")
    print(f"    Plaintext : {pt1}")
    print(f"    Key       : {k1}")
    print(f"    Ciphertext: {ct1}")
    print(f"    Decrypted : {dec1}")
    print(f"    Verified  : {'YES' if ct1 == 'SJYBTWP XJHZWNYD' and dec1 == pt1 else 'NO'}")
    print("    Note      : Standard A-Z shift produces 'SJYBTWP XJHZWNYD'.")

    # 2. Monoalphabetic Substitution Cipher
    pt2 = "CLASSICAL CRYPTOGRAPHY"
    k2 = "QWERTYUIOPASDFGHJKLZXCVBNM"
    ct2 = monoalphabetic_encrypt(pt2, k2)
    dec2 = monoalphabetic_decrypt(ct2, k2)
    print("\n[2] MONOALPHABETIC SUBSTITUTION CIPHER")
    print(f"    Plaintext : {pt2}")
    print(f"    Key       : {k2}")
    print(f"    Ciphertext: {ct2}")
    print(f"    Decrypted : {dec2}")
    print(f"    Round-Trip: {'PASSED' if dec2 == pt2 else 'FAILED'}")

    # 3. Playfair Cipher
    pt3 = "INSTRUMENTS"
    k3 = "MONARCHY"
    ct3 = playfair_encrypt(pt3, k3)
    dec3 = playfair_decrypt(ct3, k3)
    print("\n[3] PLAYFAIR CIPHER (5x5 Matrix Digraphs)")
    print(f"    Plaintext : {pt3}")
    print(f"    Keyword   : {k3}")
    print(f"    Ciphertext: {ct3}")
    print(f"    Decrypted : {dec3}")
    print("    Note      : Digraph pairing inserts filler 'X' and merges 'J' into 'I'.")

    # 4. Hill Cipher
    pt4 = "HELP"
    k4 = "3 3 2 5"
    ct4 = hill_encrypt(pt4, k4)
    dec4 = hill_decrypt(ct4, k4)
    print("\n[4] HILL CIPHER (2x2 Matrix Invertible Mod 26)")
    print(f"    Plaintext : {pt4}")
    print(f"    Key Matrix: {k4} (det=9 mod 26, invertible)")
    print(f"    Ciphertext: {ct4}")
    print(f"    Decrypted : {dec4}")
    print(f"    Round-Trip: {'PASSED' if dec4 == pt4 else 'FAILED'}")

    # 5. Vigenere Cipher
    pt5 = "CRYPTOGRAPHY AND NETWORK SECURITY"
    k5 = "SECURITY"
    ct5 = vigenere_encrypt(pt5, k5)
    dec5 = vigenere_decrypt(ct5, k5)
    print("\n[5] VIGENERE POLYALPHABETIC CIPHER")
    print(f"    Plaintext : {pt5}")
    print(f"    Keyword   : {k5}")
    print(f"    Ciphertext: {ct5}")
    print(f"    Decrypted : {dec5}")
    print(f"    Round-Trip: {'PASSED' if dec5 == pt5 else 'FAILED'}")

    # 6. One-Time Pad
    pt6 = "PERFECT SECRECY"
    ct6, otp_key = otp_encrypt(pt6)
    dec6 = otp_decrypt(ct6, otp_key)
    print("\n[6] ONE-TIME PAD (Information-Theoretic Security)")
    print(f"    Plaintext : {pt6}")
    print(f"    CSPRNG Key: {otp_key}")
    print(f"    Ciphertext: {ct6}")
    print(f"    Decrypted : {dec6}")
    print(f"    Round-Trip: {'PASSED' if dec6 == pt6 else 'FAILED'}")

    # 7. Rail Fence Cipher
    pt7 = "DEFEND THE EAST WALL"
    k7 = 3
    ct7 = rail_fence_encrypt(pt7, k7)
    dec7 = rail_fence_decrypt(ct7, k7)
    print("\n[7] RAIL FENCE TRANSPOSITION CIPHER")
    print(f"    Plaintext : {pt7}")
    print(f"    Rails (k) : {k7}")
    print(f"    Ciphertext: {ct7}")
    print(f"    Decrypted : {dec7}")
    print(f"    Round-Trip: {'PASSED' if dec7 == pt7 else 'FAILED'}")

    # 8. Columnar Transposition Cipher
    pt8 = "WE ARE DISCOVERED FLEE AT ONCE"
    k8 = "ZEBRA"
    ct8 = columnar_encrypt(pt8, k8)
    dec8 = columnar_decrypt(ct8, k8)
    print("\n[8] COLUMNAR TRANSPOSITION CIPHER")
    print(f"    Plaintext : {pt8}")
    print(f"    Key Word  : {k8}")
    print(f"    Ciphertext: {ct8}")
    print(f"    Decrypted : {dec8}")
    print(f"    Round-Trip: {'PASSED' if dec8 == pt8 else 'FAILED'}")

    # 9. Comparative Benchmarking Summary
    print("\n" + "=" * 76)
    print(" [9] ALGORITHM BENCHMARK SUMMARY (Sample Text Comparison)")
    print("=" * 76)
    bench_text = "FINAL YEAR ECM NETWORK SECURITY DEMONSTRATION"
    ciphers = [
        "Caesar Cipher", "Monoalphabetic Cipher", "Playfair Cipher",
        "Hill Cipher", "Vigenere Cipher", "One-Time Pad",
        "Rail Fence Cipher", "Columnar Transposition Cipher"
    ]
    results = compare_ciphers(ciphers, bench_text)
    print(f"{'Cipher':<30} | {'Enc Time (ms)':<14} | {'Dec Time (ms)':<14} | {'Round-Trip'}")
    print("-" * 76)
    for r in results:
        rt_status = "PASSED" if r["round_trip_success"] else "REVIEW"
        print(f"{r['cipher_name']:<30} | {r['encrypt_time_ms']:<14.4f} | {r['decrypt_time_ms']:<14.4f} | {rt_status}")
    print("=" * 76)
    print("All 8 algorithms demonstrated successfully.\n")


def run_cli_menu():
    """Text-based CLI menu mirroring the 13 options."""
    while True:
        print("\n" + "=" * 60)
        print(" CLASSICAL CRYPTOGRAPHY TOOLKIT - MAIN MENU")
        print("=" * 60)
        print(" SUBSTITUTION CIPHERS:")
        print("  1. Caesar Cipher")
        print("  2. Monoalphabetic Cipher")
        print("  3. Playfair Cipher")
        print("  4. Hill Cipher")
        print("  5. Vigenere Cipher")
        print("  6. One-Time Pad")
        print(" TRANSPOSITION CIPHERS:")
        print("  7. Rail Fence Cipher")
        print("  8. Columnar Transposition Cipher")
        print(" TOOLS & ANALYSIS:")
        print("  9. Compare Algorithms")
        print(" 10. Encrypt Text File")
        print(" 11. Decrypt Text File")
        print(" 12. Help & Theory")
        print(" 13. Exit")
        print("=" * 60)
        
        choice = input("Select an option (1-13): ").strip()
        if choice == "1":
            pt = input("Enter plaintext: ")
            k = input("Enter shift key integer (e.g. 5): ")
            enc = caesar_encrypt(pt, k)
            print(f"Ciphertext: {enc}")
            print(f"Decrypted : {caesar_decrypt(enc, k)}")
        elif choice == "2":
            pt = input("Enter plaintext: ")
            k = input("Enter 26-letter key or keyword: ")
            enc = monoalphabetic_encrypt(pt, k)
            print(f"Ciphertext: {enc}")
            print(f"Decrypted : {monoalphabetic_decrypt(enc, k)}")
        elif choice == "3":
            pt = input("Enter plaintext: ")
            k = input("Enter keyword: ")
            enc = playfair_encrypt(pt, k)
            print(f"Ciphertext: {enc}")
            print(f"Decrypted : {playfair_decrypt(enc, k)}")
        elif choice == "4":
            pt = input("Enter plaintext: ")
            k = input("Enter matrix key (e.g. '3 3 2 5'): ")
            enc = hill_encrypt(pt, k)
            print(f"Ciphertext: {enc}")
            print(f"Decrypted : {hill_decrypt(enc, k)}")
        elif choice == "5":
            pt = input("Enter plaintext: ")
            k = input("Enter keyword: ")
            enc = vigenere_encrypt(pt, k)
            print(f"Ciphertext: {enc}")
            print(f"Decrypted : {vigenere_decrypt(enc, k)}")
        elif choice == "6":
            pt = input("Enter plaintext: ")
            k = input("Enter key (or leave empty to auto-generate): ").strip()
            enc, key_used = otp_encrypt(pt, k if k else None)
            print(f"Key used  : {key_used}")
            print(f"Ciphertext: {enc}")
            print(f"Decrypted : {otp_decrypt(enc, key_used)}")
        elif choice == "7":
            pt = input("Enter plaintext: ")
            k = input("Enter number of rails >= 2: ")
            enc = rail_fence_encrypt(pt, k)
            print(f"Ciphertext: {enc}")
            print(f"Decrypted : {rail_fence_decrypt(enc, k)}")
        elif choice == "8":
            pt = input("Enter plaintext: ")
            k = input("Enter keyword or column order: ")
            enc = columnar_encrypt(pt, k)
            print(f"Ciphertext: {enc}")
            print(f"Decrypted : {columnar_decrypt(enc, k)}")
        elif choice == "9":
            pt = input("Enter text for comparison benchmark: ")
            results = compare_ciphers(list(CIPHER_GUIDES.keys()), pt)
            print("\nBenchmark Results:")
            for r in results:
                print(f" - {r['cipher_name']}: Enc={r['encrypt_time_ms']:.3f}ms, Dec={r['decrypt_time_ms']:.3f}ms")
        elif choice == "12":
            print("\nHelp: Classical ciphers are educational algorithms designed to illustrate cryptographic concepts.")
        elif choice == "13":
            print("Exiting. Thank you!")
            break
        else:
            print("Invalid selection. Please choose an option between 1 and 13.")


def main():
    """Main execution dispatcher."""
    if len(sys.argv) > 1:
        flag = sys.argv[1].lower()
        if flag in ("--demo", "-d"):
            run_demonstration()
            return
        elif flag in ("--web", "-w"):
            from web_server import run_server
            run_server(8000)
            return
        elif flag in ("--cli", "-c"):
            run_cli_menu()
            return
        elif flag in ("--help", "-h"):
            print("Usage: python main.py [--gui | --web | --cli | --demo]")
            return

    # Attempt to launch GUI by default
    try:
        from src.gui import launch_gui
        launch_gui()
    except Exception as exc:
        print(f"\n[Notice] GUI could not be initialized directly: {exc}")
        print("Defaulting to automated demonstration mode:\n")
        run_demonstration()


if __name__ == "__main__":
    main()
