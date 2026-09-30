# Classical Cryptography Toolkit
### Final Year Engineering Mini-Project (2026–27)
**Course:** Network Security  
**Branch:** Electronics and Computer Engineering (ECM)  
**Project Title:** Design and Development of a Classical Cryptography Toolkit  

---

## 📌 Project Overview
The **Classical Cryptography Toolkit** is an educational software suite and interactive laboratory testbed designed for studying, demonstrating, and comparing classical cryptographic algorithms. Developed natively in **Python 3** with a **Tkinter Graphical User Interface**, the toolkit provides verified, mathematically sound implementations of eight fundamental classical ciphers across both substitution and transposition families.

The system features an automated benchmarking engine (Option 9), safe UTF-8 text file processing (Options 10 & 11), comprehensive mathematical documentation (Option 12), and an automated test suite with **58 tests (100% pass rate)**.

---

## 🔑 Key Features

### 1. Eight Verified Classical Ciphers
- **Substitution Ciphers:**
  1. **Caesar Cipher:** Shift modulo 26 preserving case, spaces, and punctuation. Verified test vector: `NETWORK SECURITY` + key 5 $\to$ `SJYBTWP XJHZWNYD`.
  2. **Monoalphabetic Substitution Cipher:** Supports full 26-letter permutation keys and keyword-derived alphabets.
  3. **Playfair Cipher:** $5 \times 5$ matrix digraphic substitution (J merged into I) with automatic repeated-character filler insertion ('X' and 'Q') and odd-length padding.
  4. **Hill Cipher:** Polygraphic linear algebraic cipher supporting $2 \times 2$ and $3 \times 3$ matrices modulo 26. Enforces strict modular invertibility $\gcd(\det(K), 26) = 1$ and rejects non-invertible matrices with detailed error feedback.
  5. **Vigenère Cipher:** Polyalphabetic keystream with non-alphabetic bypass and case preservation.
  6. **One-Time Pad (Vernam Cipher):** True information-theoretic secrecy using CSPRNG (`secrets` module), key length enforcement, and educational warnings regarding key reuse.
- **Transposition Ciphers:**
  7. **Rail Fence Cipher:** Geometric zigzag rail transposition across $k$ rails with complete character preservation.
  8. **Columnar Transposition Cipher:** Permutation matrix with exact column length tracking for irregular rectangular grids.

### 2. Main Menu with 13 Standardized Options
- 1 Caesar Cipher
- 2 Monoalphabetic Cipher
- 3 Playfair Cipher
- 4 Hill Cipher
- 5 Vigenère Cipher
- 6 One-Time Pad
- 7 Rail Fence Cipher
- 8 Columnar Transposition Cipher
- 9 Compare Algorithms
- 10 Encrypt Text File
- 11 Decrypt Text File
- 12 Help & Theory
- 13 Exit

### 3. Algorithm Comparison Engine (Option 9)
- Select and benchmark multiple ciphers simultaneously on custom sample text.
- Measures microsecond encryption/decryption execution times and output expansion ratios.
- Renders results in an interactive `ttk.Treeview` comparison table.

### 4. Safe Text File Cryptography (Options 10 & 11)
- Load text files with UTF-8 verification and size validation.
- Live dual-pane preview of input text and processed ciphertext.
- Saves results via Windows file dialog to prevent accidental overwriting of source files.

---

## 📂 Project Structure

```text
classical-cryptography-toolkit/
├── main.py                          # Unified entry point (GUI, CLI, Demo)
├── README.md                        # Project documentation and setup guide
├── requirements.txt                 # Dependencies specification
├── .gitignore                       # Git exclusions
├── src/                             # Core application package
│   ├── __init__.py                  # Package initializer
│   ├── caesar.py                    # Caesar cipher engine
│   ├── monoalphabetic.py            # Monoalphabetic substitution engine
│   ├── playfair.py                  # Playfair matrix & digraph engine
│   ├── hill.py                      # Modular matrix Hill cipher engine
│   ├── vigenere.py                  # Vigenere polyalphabetic engine
│   ├── one_time_pad.py              # OTP CSPRNG & Vernam cipher engine
│   ├── rail_fence.py                # Rail fence zigzag transposition
│   ├── columnar_transposition.py    # Columnar permutation grid engine
│   ├── comparison.py                # Multi-cipher benchmarking engine
│   ├── file_operations.py           # Safe UTF-8 file I/O & preview
│   ├── validators.py                # Mathematical input & key validation
│   └── gui.py                       # Polished Tkinter GUI implementation
├── tests/                           # Automated test suite (58 tests)
│   ├── __init__.py                  # Test package initializer
│   ├── test_caesar.py               # Unit tests for Caesar cipher
│   ├── test_monoalphabetic.py       # Unit tests for Monoalphabetic cipher
│   ├── test_playfair.py             # Unit tests for Playfair cipher
│   ├── test_hill.py                 # Unit tests for Hill cipher
│   ├── test_vigenere.py             # Unit tests for Vigenere cipher
│   ├── test_one_time_pad.py         # Unit tests for One-Time Pad
│   ├── test_rail_fence.py           # Unit tests for Rail Fence cipher
│   ├── test_columnar_transposition.py # Unit tests for Columnar cipher
│   ├── test_file_operations.py      # Unit tests for File operations
│   └── test_comparison.py           # Unit tests for Benchmarking
├── docs/                            # Academic deliverables & documentation
│   ├── mini_project_report.md       # Complete Markdown mini-project report
│   ├── mini_project_report.pdf      # Generated PDF report document
│   ├── user_manual.md               # Windows beginner user manual
│   ├── presentation.md              # 6-slide presentation Markdown source
│   ├── presentation.pptx            # Generated 16:9 PowerPoint presentation
│   ├── test_results.md              # Verification report and test log
│   ├── flowchart.mmd                # Mermaid system architecture flowchart
│   └── generate_docs.py             # Script generating PDF and PPTX
└── sample_files/                    # Sample test data
    ├── sample_plaintext.txt         # Pre-configured test input file
    └── sample_expected_usage.txt    # Verified test vectors & expected outputs
```

---

## 💻 System Requirements & Prerequisites
- **Operating System:** Windows 10 or Windows 11 (64-bit).
- **Python Version:** Python 3.10+ (Verified on Python 3.14.3).
- **Core Dependencies:** Python Standard Library (`tkinter`, `secrets`, `math`, `time`, `os`, `sys`, `unittest`).

---

## 🚀 Installation & Setup Guide

### 1. Clone or Open the Workspace
Navigate to the project folder in your terminal:
```powershell
cd d:\NS_project
```

### 2. Create and Activate a Virtual Environment

**On Windows PowerShell:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On Windows Command Prompt (cmd.exe):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

### 3. Install Optional Dependencies
```powershell
python -m pip install -r requirements.txt
```

---

## 🖥️ Running the Application

### 1. Launch Tkinter Graphical User Interface (Default)
```powershell
python main.py
```

### 2. Run Automated Verification Demonstration
```powershell
python main.py --demo
```
Executes an automated, deterministic verification of all eight ciphers and prints performance metrics directly to the console.

### 3. Launch Interactive Command-Line Interface (CLI)
```powershell
python main.py --cli
```

---

## 🧪 Testing Instructions

Run the complete 58-test suite using `pytest`:
```powershell
python -m pytest tests -v
```

Or using Python's built-in `unittest` runner:
```powershell
python -m unittest discover tests
```

### Actual Test Results Summary
- **Total Test Cases:** 58
- **Passed:** 58 (100.0%)
- **Failed:** 0
- **Duration:** 0.25 seconds

---

## 🖼️ User Interface & Screenshot Walkthrough

When launched, the desktop GUI provides:
1. **Sidebar Navigation:** Categorized options 1 through 13 with hover highlights and clean slate styling.
2. **Dynamic Key Input:** Dynamically updates labels and placeholders depending on the selected cipher.
3. **One-Click Verified Sample:** Automatically loads standard textbook inputs and keys (e.g. `NETWORK SECURITY` + key 5 for Caesar).
4. **Real-Time Timer:** Status bar reflects microsecond execution duration (`Execution Time: X.XXX ms`).
5. **Comparison Dashboard:** Multi-select checkboxes and Treeview table reporting encryption time, decryption time, and round-trip verification.

---

## ⚠️ Known Limitations
1. **Educational Scope:** Classical ciphers are historical artifacts intended to teach fundamental cryptographic concepts (confusion, diffusion, and cryptanalysis). They offer zero resistance against modern computational attacks.
2. **Text Encoding:** Designed for UTF-8 textual streams. Binary files (.exe, .zip, .png) must not be processed with classical alphabet-based ciphers.

---

## 🔒 Cybersecurity Disclaimer
> [!IMPORTANT]
> This toolkit is designed strictly for academic instruction in Network Security and Cryptography courses. It **must not** be used for securing sensitive personal, commercial, or governmental communications. Modern secure communication requires established cryptographic standards such as AES-GCM, RSA-OAEP, or Ed25519.
