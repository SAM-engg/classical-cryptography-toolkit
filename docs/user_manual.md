# Classical Cryptography Toolkit - User Manual
## Beginner-Friendly Guide for Windows 10/11

---

## 1. Prerequisites and System Requirements

To run the Classical Cryptography Toolkit, your computer requires:
- **Operating System:** Windows 10 or Windows 11 (64-bit).
- **Python Version:** Python 3.10, 3.11, 3.12, 3.13, or 3.14.
  - Verify Python installation by opening **PowerShell** or **Command Prompt** and typing:
    ```powershell
    python --version
    ```
- **Standard Library:** Tkinter (included by default in official Python Windows installers).

---

## 2. Installation and Virtual Environment Setup

### Step 1: Open the Project Directory
Open **Windows PowerShell** or **Command Prompt** and navigate to the project directory:
```powershell
cd d:\NS_project
```

### Step 2: (Optional but Recommended) Create a Virtual Environment
```powershell
# Create a virtual environment named 'venv'
python -m venv venv

# Activate on Windows PowerShell:
.\venv\Scripts\Activate.ps1

# (Or Activate on Command Prompt):
venv\Scripts\activate.bat
```

### Step 3: Install Dependencies
The core toolkit relies primarily on standard Python libraries. For running tests and generating documents:
```powershell
python -m pip install -r requirements.txt
```

---

## 3. How to Launch the Application

The toolkit supports three launch modes via `main.py`:

### Mode A: Launch the Graphical User Interface (Default)
```powershell
python main.py
```
This opens the complete desktop GUI titled **"CLASSICAL CRYPTOGRAPHY TOOLKIT"**.

### Mode B: Automated Terminal Demonstration
```powershell
python main.py --demo
```
Runs a complete deterministic demonstration of all 8 classical ciphers and prints verification metrics in the terminal.

### Mode C: Interactive Command-Line Interface (CLI)
```powershell
python main.py --cli
```
Allows running cipher operations from a text-based terminal menu.

---

## 4. Navigating the GUI

The application window is organized into:
1. **Top Header:** Displays project title, academic year (2026-27), and course details.
2. **Left Navigation Sidebar:** Contains 13 numbered options organized into three categories:
   - **SUBSTITUTION CIPHERS:** Options 1 to 6
   - **TRANSPOSITION CIPHERS:** Options 7 to 8
   - **TOOLS & ANALYSIS:** Options 9 to 13
3. **Main Content Area:** Displays the active cipher or tool workspace with interactive input/output areas.
4. **Bottom Status Bar:** Shows real-time feedback messages (colored green for success, red for errors) and precise execution time in milliseconds (ms).

---

## 5. How to Use Every Cipher

### Option 1: Caesar Cipher
- **Principle:** Shifts letters forward by key $k \pmod{26}$.
- **Key Format:** An integer between 0 and 25 (e.g., `5`).
- **Example Usage:**
  - Plaintext: `NETWORK SECURITY`
  - Key: `5`
  - Click **ENCRYPT** $\to$ Output: `SJYBTWP XJHZWNYD`
  - Click **DECRYPT** $\to$ Output: `NETWORK SECURITY`
- **One-Click Sample:** Click **Load Verified Sample** to pre-populate this test vector instantly.

### Option 2: Monoalphabetic Substitution Cipher
- **Principle:** Replaces each alphabet character with a unique substitute letter.
- **Key Formats Supported:**
  1. Full 26-letter permutation: `QWERTYUIOPASDFGHJKLZXCVBNM`
  2. Keyword: `ZEBRAS` (automatically derives unique alphabet)
- **Example Usage:**
  - Plaintext: `CLASSICAL CRYPTOGRAPHY`
  - Key: `QWERTYUIOPASDFGHJKLZXCVBNM`
  - Click **ENCRYPT** $\to$ Output: `ESQLLOEQS EKNHZGUKQHIN`

### Option 3: Playfair Cipher
- **Principle:** Encrypts letter pairs (digraphs) across a 5x5 key matrix.
- **Key Format:** An alphabetic keyword (e.g., `MONARCHY`).
- **Rules Handled Automatically:**
  - Combines 'I' and 'J'.
  - Inserts filler 'X' between repeated letters (e.g. `LL` $\to$ `LX L`).
  - Pads odd-length messages with 'X' at the end.
- **Example Usage:**
  - Plaintext: `INSTRUMENTS`
  - Keyword: `MONARCHY`
  - Click **ENCRYPT** $\to$ Output: `GATLMZCLRQXA`

### Option 4: Hill Cipher
- **Principle:** Polygraphic matrix multiplication modulo 26: $C = (P \cdot K) \pmod{26}$.
- **Key Formats Supported:**
  - $2 \times 2$ matrix: 4 space-separated integers (e.g., `3 3 2 5`) or 4-letter keyword (`HILL`).
  - $3 \times 3$ matrix: 9 space-separated integers (e.g., `6 24 1 13 16 10 20 17 15`).
- **Invertibility Rule:** The matrix determinant $\det(K)$ must satisfy $\gcd(\det(K), 26) = 1$. The toolkit rejects invalid or non-invertible matrices with an explanation.
- **Example Usage:**
  - Plaintext: `HELP`
  - Key: `3 3 2 5`
  - Click **ENCRYPT** $\to$ Output: `DPLE`

### Option 5: Vigenère Cipher
- **Principle:** Polyalphabetic substitution using a repeating keyword.
- **Key Format:** Alphabetic keyword (e.g., `SECURITY`).
- **Character Handling:** Preserves spaces and punctuation without advancing the key.
- **Example Usage:**
  - Plaintext: `ATTACK AT DAWN`
  - Key: `LEMON`
  - Click **ENCRYPT** $\to$ Output: `LXFOPV EF RNHR`

### Option 6: One-Time Pad (Vernam Cipher)
- **Principle:** Information-Theoretic Security (perfect secrecy).
- **Key Requirement:** Must be uniformly random, secret, equal length to letters, and never reused.
- **How to Use:**
  - Enter your message in the Plaintext area.
  - Leave key empty OR click **Generate OTP Key** to generate a CSPRNG random key.
  - Click **ENCRYPT**. The generated key will appear in the key box.

### Option 7: Rail Fence Cipher
- **Principle:** Zigzag transposition across $k$ rails.
- **Key Format:** Integer depth $\ge 2$ (e.g., `3`).
- **Example Usage:**
  - Plaintext: `DEFEND THE EAST WALL`
  - Rails: `3`
  - Click **ENCRYPT** $\to$ Output: `DNHAWEEDTEES ALF  TL`

### Option 8: Columnar Transposition Cipher
- **Principle:** Grid transposition read out by alphabetical column order.
- **Key Format:** Keyword (e.g., `ZEBRA`) or space-separated permutation numbers (`3 1 4 2`).
- **Example Usage:**
  - Plaintext: `WE ARE DISCOVERED FLEE AT ONCE`
  - Key: `ZEBRA`
  - Click **ENCRYPT** $\to$ Output: `RSRLTE DV  NE ODEOAIEFACWECEE `

---

## 6. How to Use Tools & Utilities

### Option 9: Compare Algorithms
1. Click **9 Compare Algorithms** in the sidebar.
2. Enter or edit the **Benchmark Plaintext Input**.
3. Select which ciphers to evaluate using the checkboxes.
4. Click **RUN COMPARISON BENCHMARK**.
5. The interactive table will display:
   - Cipher Name & Category
   - Input Length & Ciphertext Length
   - Encryption Time (ms) & Decryption Time (ms)
   - Round-Trip Status (`Passed`)
   - Special implementation notes

### Option 10: Encrypt Text File
1. Click **10 Encrypt Text File** in the sidebar.
2. Click **Browse File...** and select any `.txt` file (e.g. `sample_files/sample_plaintext.txt`).
3. Select the desired **Cipher** from the dropdown menu.
4. Enter or review the **Key**.
5. Click **PROCESS (ENCRYPT)**. A preview appears in the right pane.
6. Click **Save Output As...** to save the encrypted text to a new file.

### Option 11: Decrypt Text File
1. Click **11 Decrypt Text File** in the sidebar.
2. Click **Browse File...** and select your encrypted file.
3. Select the corresponding **Cipher** and enter the matching **Key**.
4. Click **PROCESS (DECRYPT)**.
5. Click **Save Output As...** to save the recovered plaintext.

### Option 12: Help & Theory
Opens the built-in educational reference manual explaining mathematical formulations, historical origins, and vulnerability breakdowns for every cipher.

### Option 13: Exit
Opens a confirmation prompt to exit the application cleanly.

---

## 7. How to Run Automated Tests

To verify that all 58 unit and integration tests pass on your machine:
```powershell
python -m pytest tests -v
```
Or using Python's built-in test runner without any external packages:
```powershell
python -m unittest discover tests
```

---

## 8. Troubleshooting Common Issues

| Problem | Cause | Solution |
| :--- | :--- | :--- |
| **"Determinant is not coprime to 26"** | Entered a Hill matrix whose determinant shares factors with 26 (e.g. $\det$ is even or 13). | Use a valid invertible matrix such as `3 3 2 5` or `6 24 1 13 16 10 20 17 15`. |
| **"Key length mismatch"** | One-Time Pad key length does not match the number of alphabetic characters in message. | Click **Generate OTP Key** or leave the key box empty before encrypting. |
| **"Tkinter not found"** | Python on Windows was installed without the Tcl/Tk feature. | Re-run the official Python Windows installer, select **Modify**, and check **tcl/tk and IDLE**. |
| **"File not valid UTF-8"** | Selected file is a binary file (.exe, .pdf, image) rather than a plain text file. | Open and process only text files (`.txt`, `.csv`, `.md`). |
