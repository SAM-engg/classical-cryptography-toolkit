# Classical Cryptography Toolkit
## Final Year ECM Network Security Mini-Project (2026–27)

---

### Slide 1: Title and Project Team
- **Project Title:** Design and Development of a Classical Cryptography Toolkit
- **Course:** Network Security
- **Branch / Class:** Final Year Electronics & Computer Engineering (ECM) 2026–27
- **Project Team Members:**
  - `[STUDENT_NAME_1]` (Roll No: `[ROLL_NO_1]`, Batch: `[BATCH_1]`)
  - `[STUDENT_NAME_2]` (Roll No: `[ROLL_NO_2]`, Batch: `[BATCH_2]`)
  - `[STUDENT_NAME_3]` (Roll No: `[ROLL_NO_3]`, Batch: `[BATCH_3]`)
- **Project Guide:** `[GUIDE_NAME]`, Department of ECM
- **Institution:** `[COLLEGE_NAME_PLACEHOLDER]`

---

### Slide 2: Problem Statement & Objectives
- **Problem Statement:**
  - Classical ciphers are often studied abstractly without practical, mathematically rigorous implementations.
  - Typical issues: unhandled edge cases (spaces, punctuation, non-invertible matrices), lack of input validation, and lack of visual comparison tools.
- **Project Objectives:**
  - Implement 8 classical ciphers (Substitution & Transposition) with 100% reversible accuracy.
  - Enforce modular arithmetic validation (Hill matrix invertibility $\gcd(\det(K), 26) = 1$, OTP CSPRNG keys).
  - Develop a modern, accessible Tkinter desktop GUI with 13 categorized options.
  - Deliver comparative performance benchmarking and safe text file encryption.

---

### Slide 3: System Architecture & Supported Ciphers
- **Architecture Model:** Decoupled Presentation, Validation, and Cryptographic Engine layers.
- **Supported Ciphers (8 Core Algorithms):**
  - **Substitution Ciphers:**
    1. *Caesar Cipher:* Shift modulo 26, case and punctuation preserved.
    2. *Monoalphabetic Cipher:* Full 26-letter permutation and keyword-derived alphabets.
    3. *Playfair Cipher:* 5x5 matrix, digraph pairing, filler handling ('X' and 'Q').
    4. *Hill Cipher:* 2x2 and 3x3 linear algebraic matrix encryption modulo 26.
    5. *Vigenère Cipher:* Polyalphabetic keyword stream with non-alphabetic bypass.
    6. *One-Time Pad:* CSPRNG-generated keys, Shannon perfect secrecy principles.
  - **Transposition Ciphers:**
    7. *Rail Fence Cipher:* Zigzag rail traversal with full character preservation.
    8. *Columnar Transposition:* Permutation grid with dynamic irregular rectangle support.

---

### Slide 4: Implementation Highlights & GUI Architecture
- **Interactive Tkinter Interface:**
  - 13 Main Menu Options across Substitution, Transposition, Tools, and File I/O.
  - Live execution timing display in milliseconds.
  - One-click "Load Verified Sample" button for instant demonstration.
  - Dynamic key prompt updates and real-time status feedback.
- **Algorithm Comparison Engine (Option 9):**
  - Multi-cipher selection dashboard with Treeview metrics table.
  - Benchmarks execution time and ciphertext expansion ratio.
- **Text File Operations (Options 10 & 11):**
  - Safe UTF-8 file loading with preview windows.
  - Destination file dialog to prevent accidental overwriting of source files.

---

### Slide 5: Testing & Automated Verification
- **Automated Test Suite:**
  - Built with `pytest 9.1.1` and standard `unittest`.
  - **58 Test Cases executed, 58 Passed (100% Success Rate) in 0.25 seconds.**
- **Key Test Cases Covered:**
  - Verified sample vector: `NETWORK SECURITY` with key 5 $\to$ `SJYBTWP XJHZWNYD`.
  - Invertible vs non-invertible Hill matrices (rejection of $\det = 0, \gcd(\det, 26) \neq 1$).
  - Playfair repeated character filler insertion and odd-length padding.
  - One-Time Pad length parity and CSPRNG uniformity.
  - Transposition reversible reconstruction across irregular text lengths.

---

### Slide 6: Conclusion, Applications & Future Scope
- **Applications:**
  - Hands-on laboratory learning platform for Network Security and Cryptography students.
  - Demonstration of confusion, diffusion, and cryptanalytic vulnerabilities.
- **Key Educational Takeaway:**
  - Execution speed does not equal cryptographic security.
  - Classical ciphers are historically vital for understanding modern cryptographic foundations.
- **Future Enhancements:**
  - Automated frequency analysis and Kasiski examination modules.
  - Extension to modern symmetric algorithms (AES, DES) and asymmetric algorithms (RSA).
