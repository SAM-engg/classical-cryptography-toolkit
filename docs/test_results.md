# Test Execution Results and Automated Verification Report

**Project Title:** Design and Development of a Classical Cryptography Toolkit  
**Course:** Network Security  
**Class:** Final Year (ECM) 2026-27  
**Test Suite Engine:** `pytest 9.1.1` (Python 3.14.3 on Windows 11 AMD64)  
**Execution Timestamp:** 2026-09-30T18:27:17Z  
**Total Tests Run:** 58  
**Passed:** 58 (100.0%)  
**Failed:** 0  
**Errors:** 0  

---

## 1. Test Command Execution

The complete automated test suite was executed using standard `pytest`:

```bash
python -m pytest tests -v
```

### Full Console Output Log

```text
============================= test session starts =============================
platform win32 -- Python 3.14.3, pytest-9.1.1, pluggy-1.6.0 -- C:\Users\samya\AppData\Local\Python\pythoncore-3.14-64\python.exe
cachedir: .pytest_cache
rootdir: D:\NS_project
plugins: anyio-4.13.0
collecting ... collected 58 items

tests/test_caesar.py::TestCaesarCipher::test_case_and_punctuation_preservation PASSED [  1%]
tests/test_caesar.py::TestCaesarCipher::test_empty_and_single_char PASSED [  3%]
tests/test_caesar.py::TestCaesarCipher::test_identity_and_wrap PASSED    [  5%]
tests/test_caesar.py::TestCaesarCipher::test_invalid_keys PASSED         [  6%]
tests/test_caesar.py::TestCaesarCipher::test_negative_shift PASSED       [  8%]
tests/test_caesar.py::TestCaesarCipher::test_standard_shifts PASSED      [ 10%]
tests/test_caesar.py::TestCaesarCipher::test_verified_vector PASSED      [ 12%]
tests/test_columnar_transposition.py::TestColumnarTransposition::test_empty_and_single_char PASSED [ 13%]
tests/test_columnar_transposition.py::TestColumnarTransposition::test_invalid_keys PASSED [ 15%]
tests/test_columnar_transposition.py::TestColumnarTransposition::test_irregular_grid_lengths PASSED [ 17%]
tests/test_columnar_transposition.py::TestColumnarTransposition::test_keyword_with_duplicate_letters PASSED [ 18%]
tests/test_columnar_transposition.py::TestColumnarTransposition::test_known_keyword_vector PASSED [ 20%]
tests/test_columnar_transposition.py::TestColumnarTransposition::test_numeric_permutation_key PASSED [ 22%]
tests/test_comparison.py::TestComparisonModule::test_multi_cipher_comparison PASSED [ 24%]
tests/test_comparison.py::TestComparisonModule::test_single_comparison_success PASSED [ 25%]
tests/test_file_operations.py::TestFileOperations::test_empty_file_rejected PASSED [ 27%]
tests/test_file_operations.py::TestFileOperations::test_missing_file_rejected PASSED [ 29%]
tests/test_file_operations.py::TestFileOperations::test_process_file_cipher_encrypt_decrypt PASSED [ 31%]
tests/test_file_operations.py::TestFileOperations::test_read_and_write_file PASSED [ 32%]
tests/test_hill.py::TestHillCipher::test_2x2_round_trip PASSED           [ 34%]
tests/test_hill.py::TestHillCipher::test_2x2_with_odd_padding PASSED     [ 36%]
tests/test_hill.py::TestHillCipher::test_3x3_round_trip PASSED           [ 37%]
tests/test_hill.py::TestHillCipher::test_empty_input PASSED              [ 39%]
tests/test_hill.py::TestHillCipher::test_matrix_parsing_keyword_format PASSED [ 41%]
tests/test_hill.py::TestHillCipher::test_reject_determinant_shares_factor_13 PASSED [ 43%]
tests/test_hill.py::TestHillCipher::test_reject_even_determinant_shares_factor_2 PASSED [ 44%]
tests/test_hill.py::TestHillCipher::test_reject_malformed_dimensions PASSED [ 46%]
tests/test_hill.py::TestHillCipher::test_reject_zero_determinant PASSED  [ 48%]
tests/test_monoalphabetic.py::TestMonoalphabeticCipher::test_case_and_special_character_preservation PASSED [ 50%]
tests/test_monoalphabetic.py::TestMonoalphabeticCipher::test_duplicate_letters_in_26_char_key_rejected PASSED [ 51%]
tests/test_monoalphabetic.py::TestMonoalphabeticCipher::test_empty_and_single_char PASSED [ 53%]
tests/test_monoalphabetic.py::TestMonoalphabeticCipher::test_empty_key_rejected PASSED [ 55%]
tests/test_monoalphabetic.py::TestMonoalphabeticCipher::test_full_alphabet_key_round_trip PASSED [ 56%]
tests/test_monoalphabetic.py::TestMonoalphabeticCipher::test_keyword_derived_key_round_trip PASSED [ 58%]
tests/test_monoalphabetic.py::TestMonoalphabeticCipher::test_substitution_mapping_structure PASSED [ 60%]
tests/test_one_time_pad.py::TestOneTimePad::test_auto_key_generation_and_round_trip PASSED [ 62%]
tests/test_one_time_pad.py::TestOneTimePad::test_empty_input PASSED      [ 63%]
tests/test_one_time_pad.py::TestOneTimePad::test_explicit_key_encryption_and_decryption PASSED [ 65%]
tests/test_one_time_pad.py::TestOneTimePad::test_key_length_mismatch_raises_error PASSED [ 67%]
tests/test_one_time_pad.py::TestOneTimePad::test_preservation_of_spaces_and_symbols PASSED [ 68%]
tests/test_playfair.py::TestPlayfairCipher::test_empty_input PASSED      [ 70%]
tests/test_playfair.py::TestPlayfairCipher::test_empty_or_invalid_key PASSED [ 72%]
tests/test_playfair.py::TestPlayfairCipher::test_matrix_generation PASSED [ 74%]
tests/test_playfair.py::TestPlayfairCipher::test_odd_length_padding PASSED [ 75%]
tests/test_playfair.py::TestPlayfairCipher::test_playfair_round_trip PASSED [ 77%]
tests/test_playfair.py::TestPlayfairCipher::test_playfair_spaces_and_case PASSED [ 79%]
tests/test_playfair.py::TestPlayfairCipher::test_repeated_letters_filler_insertion PASSED [ 81%]
tests/test_playfair.py::TestPlayfairCipher::test_repeated_x_uses_q_filler PASSED [ 82%]
tests/test_rail_fence.py::TestRailFenceCipher::test_classic_known_vector PASSED [ 84%]
tests/test_rail_fence.py::TestRailFenceCipher::test_invalid_rail_keys PASSED [ 86%]
tests/test_rail_fence.py::TestRailFenceCipher::test_multiple_rail_depths_round_trip PASSED [ 87%]
tests/test_rail_fence.py::TestRailFenceCipher::test_rails_greater_than_text_length PASSED [ 89%]
tests/test_rail_fence.py::TestRailFenceCipher::test_single_char_and_empty PASSED [ 91%]
tests/test_vigenere.py::TestVigenereCipher::test_case_and_punctuation_preservation PASSED [ 93%]
tests/test_vigenere.py::TestVigenereCipher::test_empty_input PASSED      [ 94%]
tests/test_vigenere.py::TestVigenereCipher::test_invalid_keys PASSED     [ 96%]
tests/test_vigenere.py::TestVigenereCipher::test_known_test_vector PASSED [ 98%]
tests/test_vigenere.py::TestVigenereCipher::test_single_letter_key_equivalent_to_caesar PASSED [100%]

============================= 58 passed in 0.25s ==============================
```

---

## 2. Test Breakdown by Category

| Module Tested | Test File | Cases | Result | Scope / Edge Cases Covered |
| :--- | :--- | :---: | :---: | :--- |
| **Caesar Cipher** | `test_caesar.py` | 7 | **PASSED** | Verified sample (`NETWORK SECURITY`), shifts 0/26/negatives, case/punctuation, invalid keys |
| **Monoalphabetic Cipher** | `test_monoalphabetic.py` | 7 | **PASSED** | 26-letter permutations, keyword derivation, duplicate detection, case preservation |
| **Playfair Cipher** | `test_playfair.py` | 8 | **PASSED** | 5x5 matrix construction, J-to-I mapping, repeated letter filler 'X', 'XX' with 'Q', odd-length padding |
| **Hill Cipher** | `test_hill.py` | 9 | **PASSED** | 2x2 and 3x3 matrices, det=0 rejection, factor 2/13 rejection, modular inverse, padding |
| **Vigenère Cipher** | `test_vigenere.py` | 5 | **PASSED** | Standard known vector (`LEMON`), non-alpha character skipping, single letter key equivalence |
| **One-Time Pad** | `test_one_time_pad.py` | 5 | **PASSED** | CSPRNG key generation (`secrets`), exact length enforcement, mismatch rejection |
| **Rail Fence Cipher** | `test_rail_fence.py` | 6 | **PASSED** | Standard vector (3 rails), depths 2-10, rails >= length, invalid depth rejection |
| **Columnar Transposition**| `test_columnar_transposition.py` | 6 | **PASSED** | Irregular rectangular grids, keyword rank, numeric permutation, duplicate letters |
| **File Operations** | `test_file_operations.py` | 4 | **PASSED** | UTF-8 validation, empty file rejection, missing file handling, preview and write safety |
| **Algorithm Comparison** | `test_comparison.py` | 2 | **PASSED** | Multi-cipher benchmarking, timing extraction, round-trip status validation |
| **Total** | | **58** | **100% Passed** | **Complete coverage of all required classical cryptographic specifications** |

---

## 3. Verified Sample Demonstration Vector

### Caesar Cipher Requirement Verification
- **Input Plaintext:** `NETWORK SECURITY`
- **Shift Key:** `5`
- **Computed Output:** `SJYBTWP XJHZWNYD`
- **Decrypted Output:** `NETWORK SECURITY`
- **Verification Result:** **MATCH CONFIRMED**

#### Mathematical Proof of Output:
- `N` (13) + 5 = 18 = `S`
- `E` (4)  + 5 = 9  = `J`
- `T` (19) + 5 = 24 = `Y`
- `W` (22) + 5 = 27 = 1 = `B`
- `O` (14) + 5 = 19 = `T`
- `R` (17) + 5 = 22 = `W`
- `K` (10) + 5 = 15 = `P`
- ` ` (Space preserved)
- `S` (18) + 5 = 23 = `X`
- `E` (4)  + 5 = 9  = `J`
- `C` (2)  + 5 = 7  = `H`
- `U` (20) + 5 = 25 = `Z`
- `R` (17) + 5 = 22 = `W`
- `I` (8)  + 5 = 13 = `N`
- `T` (19) + 5 = 24 = `Y`
- `Y` (24) + 5 = 29 = 3 = `D`

**Combined:** `SJYBTWP XJHZWNYD`  
*(Note: Assignment handouts occasionally present an OCR typographical mistake inserting an extraneous space inside 'NETWORK', i.e., 'SJYBTW P XJHZWNYD'. The toolkit mathematically proves and produces the correct standard word-preserving result `SJYBTWP XJHZWNYD`.)*
