"""
gui.py - Professional Tkinter Graphical User Interface
Design and Development of a Classical Cryptography Toolkit
Course: Network Security | Class: Final Year (ECM) 2026-27

Features:
- Main Options 1 through 13 with categorized sections:
    * SUBSTITUTION CIPHERS (1 Caesar, 2 Monoalphabetic, 3 Playfair, 4 Hill, 5 Vigenere, 6 OTP)
    * TRANSPOSITION CIPHERS (7 Rail Fence, 8 Columnar Transposition)
    * TOOLS & ANALYSIS (9 Compare Algorithms, 10 Encrypt File, 11 Decrypt File, 12 Help, 13 Exit)
- Interactive cipher operations: Encrypt, Decrypt, Copy, Clear, Sample Data
- Dynamic key format hints and validation warnings
- Algorithm comparison dashboard with Treeview benchmarking table
- Secure file operations with previews and destination file picker
- Microsecond execution timer and live status message bar
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import time
import os

from src.caesar import caesar_encrypt, caesar_decrypt
from src.monoalphabetic import monoalphabetic_encrypt, monoalphabetic_decrypt
from src.playfair import playfair_encrypt, playfair_decrypt
from src.hill import hill_encrypt, hill_decrypt
from src.vigenere import vigenere_encrypt, vigenere_decrypt
from src.one_time_pad import otp_encrypt, otp_decrypt, generate_otp_key
from src.rail_fence import rail_fence_encrypt, rail_fence_decrypt
from src.columnar_transposition import columnar_encrypt, columnar_decrypt
from src.comparison import compare_ciphers, CIPHER_METADATA
from src.file_operations import read_text_file, write_text_file, process_file_cipher, FileOperationError
from src.validators import ValidationError


# Cipher descriptive guides and sample test vectors
CIPHER_GUIDES = {
    "1 Caesar Cipher": {
        "name": "Caesar Cipher",
        "category": "Substitution",
        "desc": "Monoalphabetic shift cipher: C_i = (P_i + k) mod 26. Shifts letters forward by key k.",
        "key_prompt": "Shift Key (Integer 0-25):",
        "default_key": "5",
        "default_sample": "NETWORK SECURITY",
        "sample_output_info": "Plaintext 'NETWORK SECURITY' with key 5 produces 'SJYBTWP XJHZWNYD'.",
        "placeholder": "Enter integer shift (e.g., 5)"
    },
    "2 Monoalphabetic Cipher": {
        "name": "Monoalphabetic Cipher",
        "category": "Substitution",
        "desc": "Fixed 1-to-1 letter mapping. Uses a 26-letter substitution alphabet or keyword.",
        "key_prompt": "26-Letter Alphabet or Keyword:",
        "default_key": "QWERTYUIOPASDFGHJKLZXCVBNM",
        "default_sample": "ATTACK AT DAWN",
        "sample_output_info": "Maps each character of standard alphabet to unique replacement character.",
        "placeholder": "Enter 26 distinct letters (e.g. QWERTY...) or a keyword"
    },
    "3 Playfair Cipher": {
        "name": "Playfair Cipher",
        "category": "Substitution",
        "desc": "Digraphic substitution using 5x5 letter matrix. J merged into I. Pads repeats/odds with 'X'.",
        "key_prompt": "Alphabetic Keyword:",
        "default_key": "MONARCHY",
        "default_sample": "INSTRUMENTS",
        "sample_output_info": "Pairing: IN ST RU ME NT SX -> Encrypted using row/col/rectangle rules.",
        "placeholder": "Enter keyword (e.g., MONARCHY)"
    },
    "4 Hill Cipher": {
        "name": "Hill Cipher",
        "category": "Substitution",
        "desc": "Polygraphic cipher via linear algebra: C = (P * K) mod 26. Key must be invertible mod 26.",
        "key_prompt": "Matrix Key (4 or 9 integers or letters):",
        "default_key": "3 3 2 5",
        "default_sample": "HELP",
        "sample_output_info": "2x2 key [3, 3; 2, 5] has det=9 mod 26 (coprime, gcd(9,26)=1). Invertible.",
        "placeholder": "Enter '3 3 2 5' (2x2) or 'HILL' or 9 numbers for 3x3"
    },
    "5 Vigenere Cipher": {
        "name": "Vigenere Cipher",
        "category": "Substitution",
        "desc": "Polyalphabetic substitution using periodic key: C_i = (P_i + K_j) mod 26.",
        "key_prompt": "Alphabetic Keyword:",
        "default_key": "SECURITY",
        "default_sample": "CRYPTOGRAPHY AND NETWORK SECURITY",
        "sample_output_info": "Key repeats over alphabetic letters; spaces and punctuation preserved.",
        "placeholder": "Enter keyword (e.g., SECURITY or CIPHER)"
    },
    "6 One-Time Pad": {
        "name": "One-Time Pad",
        "category": "Substitution",
        "desc": "Information-theoretic security. Key must be uniformly random, secret, equal length, and never reused.",
        "key_prompt": "Random Key (Equal length to letters):",
        "default_key": "",
        "default_sample": "FINAL YEAR MINI PROJECT",
        "sample_output_info": "Leave key empty to automatically generate a cryptographically secure random key.",
        "placeholder": "Leave blank to auto-generate secure key or enter matching letters"
    },
    "7 Rail Fence Cipher": {
        "name": "Rail Fence Cipher",
        "category": "Transposition",
        "desc": "Transposition cipher: writes message diagonally across k rails in zigzag, reads row-by-row.",
        "key_prompt": "Number of Rails (Depth >= 2):",
        "default_key": "3",
        "default_sample": "DEFEND THE EAST WALL",
        "sample_output_info": "Zigzag pattern across 3 rails. Preserves exact characters upon decryption.",
        "placeholder": "Enter integer depth >= 2 (e.g., 3)"
    },
    "8 Columnar Transposition Cipher": {
        "name": "Columnar Transposition Cipher",
        "category": "Transposition",
        "desc": "Transposition cipher: text written in rows of key width W, read by alphabetical key column order.",
        "key_prompt": "Keyword or Column Permutation:",
        "default_key": "ZEBRA",
        "default_sample": "WE ARE DISCOVERED FLEE AT ONCE",
        "sample_output_info": "Columns read according to alphabetical rank of letters in ZEBRA.",
        "placeholder": "Enter word (e.g., ZEBRA) or numbers (e.g., 3 1 4 2)"
    }
}


class ToolkitGUI:
    """Main Application GUI Class for Classical Cryptography Toolkit."""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("CLASSICAL CRYPTOGRAPHY TOOLKIT - ECM Network Security Mini-Project")
        self.root.geometry("1100x750")
        self.root.minsize(950, 650)
        
        # Color Scheme
        self.BG_DARK = "#0f172a"       # Slate 900
        self.SIDEBAR_BG = "#1e293b"     # Slate 800
        self.SIDEBAR_HOVER = "#334155"  # Slate 700
        self.CARD_BG = "#ffffff"        # Clean white card
        self.ACCENT_BLUE = "#2563eb"    # Blue 600
        self.ACCENT_GREEN = "#16a34a"   # Green 600
        self.TEXT_MAIN = "#0f172a"
        self.TEXT_MUTED = "#64748b"
        self.BORDER_COLOR = "#cbd5e1"
        
        self.current_cipher_key = "1 Caesar Cipher"
        
        self._setup_styles()
        self._build_layout()
        self.show_cipher_view("1 Caesar Cipher")

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        # Configure Treeview styling for comparison table
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"), background="#e2e8f0", foreground="#1e293b")
        style.configure("Treeview", font=("Segoe UI", 9), rowheight=24, background="#ffffff", fieldbackground="#ffffff")
        style.map("Treeview", background=[("selected", "#3b82f6")], foreground=[("selected", "#ffffff")])
        
    def _build_layout(self):
        # Header bar
        header_frame = tk.Frame(self.root, bg=self.BG_DARK, height=54)
        header_frame.pack(side=tk.TOP, fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="CLASSICAL CRYPTOGRAPHY TOOLKIT",
            font=("Segoe UI", 14, "bold"),
            bg=self.BG_DARK,
            fg="#f8fafc"
        )
        title_label.pack(side=tk.LEFT, padx=18, pady=6)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Final Year ECM (2026-27) | Course: Network Security",
            font=("Segoe UI", 9),
            bg=self.BG_DARK,
            fg="#94a3b8"
        )
        subtitle_label.pack(side=tk.RIGHT, padx=18, pady=10)
        
        # Main container with Sidebar and Content Frame
        self.main_container = tk.Frame(self.root, bg="#f1f5f9")
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Sidebar Frame
        self.sidebar_frame = tk.Frame(self.main_container, bg=self.SIDEBAR_BG, width=240)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar_frame.pack_propagate(False)
        
        self._populate_sidebar()
        
        # Content Display Area
        self.content_container = tk.Frame(self.main_container, bg="#f8fafc")
        self.content_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=12, pady=12)
        
        # Bottom Status Bar
        self.status_bar = tk.Frame(self.root, bg="#e2e8f0", height=28)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_bar.pack_propagate(False)
        
        self.status_label = tk.Label(
            self.status_bar,
            text="Ready. Select an option from the menu to begin.",
            font=("Segoe UI", 8),
            bg="#e2e8f0",
            fg="#334155",
            anchor="w"
        )
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=12)
        
        self.time_label = tk.Label(
            self.status_bar,
            text="Execution Time: -- ms",
            font=("Segoe UI", 8, "bold"),
            bg="#e2e8f0",
            fg="#2563eb",
            anchor="e"
        )
        self.time_label.pack(side=tk.RIGHT, padx=14)

    def _populate_sidebar(self):
        """Populate the 13 navigation buttons divided by section."""
        canvas = tk.Canvas(self.sidebar_frame, bg=self.SIDEBAR_BG, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.sidebar_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.SIDEBAR_BG)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=225)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        def add_header(title):
            lbl = tk.Label(
                scrollable_frame,
                text=title,
                font=("Segoe UI", 8, "bold"),
                bg=self.SIDEBAR_BG,
                fg="#38bdf8",
                anchor="w",
                padx=12,
                pady=6
            )
            lbl.pack(fill=tk.X, pady=(6, 2))

        def add_nav_btn(text, cmd):
            btn = tk.Button(
                scrollable_frame,
                text=text,
                font=("Segoe UI", 9),
                bg=self.SIDEBAR_BG,
                fg="#f1f5f9",
                activebackground=self.SIDEBAR_HOVER,
                activeforeground="#ffffff",
                relief=tk.FLAT,
                anchor="w",
                padx=12,
                pady=4,
                cursor="hand2",
                command=cmd
            )
            btn.pack(fill=tk.X, padx=4, pady=1)
            return btn

        # Section 1: Substitution Ciphers
        add_header("SUBSTITUTION CIPHERS")
        add_nav_btn("1  Caesar Cipher", lambda: self.show_cipher_view("1 Caesar Cipher"))
        add_nav_btn("2  Monoalphabetic Cipher", lambda: self.show_cipher_view("2 Monoalphabetic Cipher"))
        add_nav_btn("3  Playfair Cipher", lambda: self.show_cipher_view("3 Playfair Cipher"))
        add_nav_btn("4  Hill Cipher", lambda: self.show_cipher_view("4 Hill Cipher"))
        add_nav_btn("5  Vigenere Cipher", lambda: self.show_cipher_view("5 Vigenere Cipher"))
        add_nav_btn("6  One-Time Pad", lambda: self.show_cipher_view("6 One-Time Pad"))
        
        # Section 2: Transposition Ciphers
        add_header("TRANSPOSITION CIPHERS")
        add_nav_btn("7  Rail Fence Cipher", lambda: self.show_cipher_view("7 Rail Fence Cipher"))
        add_nav_btn("8  Columnar Transposition", lambda: self.show_cipher_view("8 Columnar Transposition Cipher"))
        
        # Section 3: Tools & Comparison
        add_header("TOOLS & ANALYSIS")
        add_nav_btn("9  Compare Algorithms", self.show_compare_view)
        add_nav_btn("10 Encrypt Text File", lambda: self.show_file_view("encrypt"))
        add_nav_btn("11 Decrypt Text File", lambda: self.show_file_view("decrypt"))
        add_nav_btn("12 Help & Theory", self.show_help_view)
        add_nav_btn("13 Exit", self.confirm_exit)

    def _clear_content_container(self):
        for widget in self.content_container.winfo_children():
            widget.destroy()

    def set_status(self, message: str, is_error: bool = False, is_success: bool = False):
        color = "#dc2626" if is_error else ("#16a34a" if is_success else "#334155")
        self.status_label.config(text=message, fg=color)

    def set_exec_time(self, elapsed_sec: float):
        ms = elapsed_sec * 1000.0
        self.time_label.config(text=f"Execution Time: {ms:.3f} ms")

    # -------------------------------------------------------------
    # CIPHER VIEW (Options 1 to 8)
    # -------------------------------------------------------------
    def show_cipher_view(self, cipher_key: str):
        self.current_cipher_key = cipher_key
        info = CIPHER_GUIDES[cipher_key]
        self._clear_content_container()
        
        # Top Card: Header & Description
        top_card = tk.Frame(self.content_container, bg="#ffffff", bd=1, relief=tk.SOLID)
        top_card.pack(fill=tk.X, pady=(0, 10), padx=2)
        
        header_row = tk.Frame(top_card, bg="#ffffff")
        header_row.pack(fill=tk.X, padx=12, pady=(10, 4))
        
        tk.Label(
            header_row,
            text=f"{cipher_key}",
            font=("Segoe UI", 13, "bold"),
            bg="#ffffff",
            fg="#1e293b"
        ).pack(side=tk.LEFT)
        
        tk.Label(
            header_row,
            text=f"Category: {info['category']}",
            font=("Segoe UI", 9, "bold"),
            bg="#e0f2fe",
            fg="#0369a1",
            padx=8,
            pady=2
        ).pack(side=tk.RIGHT)
        
        tk.Label(
            top_card,
            text=info["desc"],
            font=("Segoe UI", 9),
            bg="#ffffff",
            fg="#475569",
            wraplength=760,
            justify="left"
        ).pack(fill=tk.X, padx=12, pady=(0, 4))
        
        # Key Configuration Card
        key_card = tk.Frame(self.content_container, bg="#ffffff", bd=1, relief=tk.SOLID)
        key_card.pack(fill=tk.X, pady=(0, 10), padx=2)
        
        key_frame = tk.Frame(key_card, bg="#ffffff")
        key_frame.pack(fill=tk.X, padx=12, pady=10)
        
        tk.Label(
            key_frame,
            text=info["key_prompt"],
            font=("Segoe UI", 9, "bold"),
            bg="#ffffff",
            fg="#1e293b"
        ).pack(side=tk.LEFT, padx=(0, 8))
        
        self.key_entry = tk.Entry(key_frame, font=("Consolas", 10), width=36)
        self.key_entry.insert(0, info["default_key"])
        self.key_entry.pack(side=tk.LEFT, padx=(0, 10), ipady=2)
        
        if cipher_key == "6 One-Time Pad":
            gen_btn = tk.Button(
                key_frame,
                text="Generate OTP Key",
                font=("Segoe UI", 8, "bold"),
                bg="#0284c7",
                fg="#ffffff",
                relief=tk.FLAT,
                cursor="hand2",
                command=self._generate_otp_key_action
            )
            gen_btn.pack(side=tk.LEFT, padx=(0, 10))
            
        load_sample_btn = tk.Button(
            key_frame,
            text="Load Verified Sample",
            font=("Segoe UI", 8),
            bg="#f1f5f9",
            fg="#334155",
            relief=tk.SOLID,
            bd=1,
            cursor="hand2",
            command=lambda: self._load_cipher_sample(cipher_key)
        )
        load_sample_btn.pack(side=tk.LEFT)
        
        # Text Areas Frame (Plaintext & Ciphertext)
        io_frame = tk.Frame(self.content_container, bg="#f8fafc")
        io_frame.pack(fill=tk.BOTH, expand=True, padx=2)
        
        # Plaintext Frame
        pt_frame = tk.LabelFrame(io_frame, text=" Plaintext Input ", font=("Segoe UI", 9, "bold"), bg="#ffffff", fg="#1e293b")
        pt_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))
        
        self.plain_text = tk.Text(pt_frame, font=("Segoe UI", 10), wrap=tk.WORD, bd=0, padx=8, pady=8)
        self.plain_text.pack(fill=tk.BOTH, expand=True)
        self.plain_text.insert("1.0", info["default_sample"])
        
        # Ciphertext / Output Frame
        ct_frame = tk.LabelFrame(io_frame, text=" Output Result (Ciphertext / Decrypted) ", font=("Segoe UI", 9, "bold"), bg="#ffffff", fg="#1e293b")
        ct_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(6, 0))
        
        self.output_text = tk.Text(ct_frame, font=("Segoe UI", 10), wrap=tk.WORD, bd=0, padx=8, pady=8)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Action Buttons Row
        btn_bar = tk.Frame(self.content_container, bg="#f8fafc")
        btn_bar.pack(fill=tk.X, pady=(10, 0), padx=2)
        
        enc_btn = tk.Button(
            btn_bar,
            text="ENCRYPT",
            font=("Segoe UI", 9, "bold"),
            bg="#16a34a",
            fg="#ffffff",
            relief=tk.FLAT,
            padx=18,
            pady=5,
            cursor="hand2",
            command=self._do_encrypt
        )
        enc_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        dec_btn = tk.Button(
            btn_bar,
            text="DECRYPT",
            font=("Segoe UI", 9, "bold"),
            bg="#2563eb",
            fg="#ffffff",
            relief=tk.FLAT,
            padx=18,
            pady=5,
            cursor="hand2",
            command=self._do_decrypt
        )
        dec_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        swap_btn = tk.Button(
            btn_bar,
            text="Use Output as Input",
            font=("Segoe UI", 9),
            bg="#f1f5f9",
            fg="#334155",
            relief=tk.SOLID,
            bd=1,
            padx=12,
            pady=5,
            cursor="hand2",
            command=self._swap_io
        )
        swap_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        copy_btn = tk.Button(
            btn_bar,
            text="Copy Output",
            font=("Segoe UI", 9),
            bg="#f1f5f9",
            fg="#334155",
            relief=tk.SOLID,
            bd=1,
            padx=12,
            pady=5,
            cursor="hand2",
            command=self._copy_output
        )
        copy_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        clear_btn = tk.Button(
            btn_bar,
            text="Clear All",
            font=("Segoe UI", 9),
            bg="#f1f5f9",
            fg="#dc2626",
            relief=tk.SOLID,
            bd=1,
            padx=12,
            pady=5,
            cursor="hand2",
            command=self._clear_text_areas
        )
        clear_btn.pack(side=tk.LEFT)
        
        self.set_status(f"Loaded {cipher_key}. Ready.")

    def _load_cipher_sample(self, cipher_key: str):
        info = CIPHER_GUIDES[cipher_key]
        self.key_entry.delete(0, tk.END)
        self.key_entry.insert(0, info["default_key"])
        self.plain_text.delete("1.0", tk.END)
        self.plain_text.insert("1.0", info["default_sample"])
        self.output_text.delete("1.0", tk.END)
        self.set_status(f"Loaded sample vector: {info['sample_output_info']}")

    def _generate_otp_key_action(self):
        text = self.plain_text.get("1.0", tk.END).strip()
        alpha_count = sum(1 for c in text if c.isalpha())
        if alpha_count == 0:
            alpha_count = 16  # fallback default
        random_key = generate_otp_key(alpha_count)
        self.key_entry.delete(0, tk.END)
        self.key_entry.insert(0, random_key)
        self.set_status(f"Generated secure OTP key of length {alpha_count}.", is_success=True)

    def _swap_io(self):
        out_content = self.output_text.get("1.0", tk.END).strip()
        if not out_content:
            self.set_status("No output available to transfer.", is_error=True)
            return
        self.plain_text.delete("1.0", tk.END)
        self.plain_text.insert("1.0", out_content)
        self.output_text.delete("1.0", tk.END)
        self.set_status("Output transferred to input area.")

    def _copy_output(self):
        out_content = self.output_text.get("1.0", tk.END).strip()
        if not out_content:
            self.set_status("Output is empty. Nothing to copy.", is_error=True)
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(out_content)
        self.set_status("Copied output to system clipboard!", is_success=True)

    def _clear_text_areas(self):
        self.plain_text.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)
        self.set_status("Text areas cleared.")

    def _do_encrypt(self):
        cipher_name = CIPHER_GUIDES[self.current_cipher_key]["name"]
        plaintext = self.plain_text.get("1.0", tk.END).rstrip("\n")
        key = self.key_entry.get().strip()
        
        t0 = time.perf_counter()
        try:
            if cipher_name == "Caesar Cipher":
                ciphertext = caesar_encrypt(plaintext, key)
            elif cipher_name == "Monoalphabetic Cipher":
                ciphertext = monoalphabetic_encrypt(plaintext, key)
            elif cipher_name == "Playfair Cipher":
                ciphertext = playfair_encrypt(plaintext, key)
            elif cipher_name == "Hill Cipher":
                ciphertext = hill_encrypt(plaintext, key)
            elif cipher_name == "Vigenere Cipher":
                ciphertext = vigenere_encrypt(plaintext, key)
            elif cipher_name == "One-Time Pad":
                ciphertext, key_used = otp_encrypt(plaintext, key if key else None)
                if not key:
                    self.key_entry.delete(0, tk.END)
                    self.key_entry.insert(0, key_used)
            elif cipher_name == "Rail Fence Cipher":
                ciphertext = rail_fence_encrypt(plaintext, key)
            elif cipher_name == "Columnar Transposition Cipher":
                ciphertext = columnar_encrypt(plaintext, key)
            else:
                raise ValidationError(f"Unknown cipher {cipher_name}")
                
            elapsed = time.perf_counter() - t0
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", ciphertext)
            self.set_exec_time(elapsed)
            self.set_status(f"Successfully encrypted using {cipher_name}.", is_success=True)
            
        except Exception as exc:
            self.set_status(f"Encryption Error: {str(exc)}", is_error=True)
            messagebox.showerror("Encryption Error", str(exc))

    def _do_decrypt(self):
        cipher_name = CIPHER_GUIDES[self.current_cipher_key]["name"]
        # Use content from plain_text area or output_text if user didn't swap
        ciphertext = self.plain_text.get("1.0", tk.END).rstrip("\n")
        key = self.key_entry.get().strip()
        
        t0 = time.perf_counter()
        try:
            if cipher_name == "Caesar Cipher":
                decrypted = caesar_decrypt(ciphertext, key)
            elif cipher_name == "Monoalphabetic Cipher":
                decrypted = monoalphabetic_decrypt(ciphertext, key)
            elif cipher_name == "Playfair Cipher":
                decrypted = playfair_decrypt(ciphertext, key)
            elif cipher_name == "Hill Cipher":
                decrypted = hill_decrypt(ciphertext, key)
            elif cipher_name == "Vigenere Cipher":
                decrypted = vigenere_decrypt(ciphertext, key)
            elif cipher_name == "One-Time Pad":
                decrypted = otp_decrypt(ciphertext, key)
            elif cipher_name == "Rail Fence Cipher":
                decrypted = rail_fence_decrypt(ciphertext, key)
            elif cipher_name == "Columnar Transposition Cipher":
                decrypted = columnar_decrypt(ciphertext, key)
            else:
                raise ValidationError(f"Unknown cipher {cipher_name}")
                
            elapsed = time.perf_counter() - t0
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", decrypted)
            self.set_exec_time(elapsed)
            self.set_status(f"Successfully decrypted using {cipher_name}.", is_success=True)
            
        except Exception as exc:
            self.set_status(f"Decryption Error: {str(exc)}", is_error=True)
            messagebox.showerror("Decryption Error", str(exc))

    # -------------------------------------------------------------
    # OPTION 9: COMPARE ALGORITHMS VIEW
    # -------------------------------------------------------------
    def show_compare_view(self):
        self._clear_content_container()
        
        # Top banner
        header = tk.Frame(self.content_container, bg="#ffffff", bd=1, relief=tk.SOLID)
        header.pack(fill=tk.X, pady=(0, 10), padx=2)
        
        tk.Label(
            header,
            text="9  Compare Classical Ciphers",
            font=("Segoe UI", 13, "bold"),
            bg="#ffffff",
            fg="#1e293b"
        ).pack(anchor="w", padx=12, pady=(10, 2))
        
        tk.Label(
            header,
            text="Select algorithms, enter sample text, and evaluate execution timing and output expansion.\n"
                 "Note: Benchmarking times vary by hardware and text size. A faster cipher does NOT imply stronger security.",
            font=("Segoe UI", 8),
            bg="#ffffff",
            fg="#64748b",
            justify="left"
        ).pack(anchor="w", padx=12, pady=(0, 8))
        
        # Input & Selection Row
        control_frame = tk.Frame(self.content_container, bg="#ffffff", bd=1, relief=tk.SOLID)
        control_frame.pack(fill=tk.X, pady=(0, 10), padx=2)
        
        # Sample text entry
        pt_label_frame = tk.Frame(control_frame, bg="#ffffff")
        pt_label_frame.pack(fill=tk.X, padx=12, pady=(8, 4))
        
        tk.Label(pt_label_frame, text="Benchmark Plaintext Input:", font=("Segoe UI", 9, "bold"), bg="#ffffff").pack(side=tk.LEFT)
        self.compare_input = tk.Entry(pt_label_frame, font=("Segoe UI", 9), width=70)
        self.compare_input.insert(0, "NETWORK SECURITY AND CLASSICAL CIPHER PERFORMANCE EVALUATION")
        self.compare_input.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        # Cipher Checkboxes
        cb_frame = tk.Frame(control_frame, bg="#ffffff")
        cb_frame.pack(fill=tk.X, padx=12, pady=6)
        
        self.cipher_vars = {}
        all_ciphers = list(CIPHER_METADATA.keys())
        
        for idx, cname in enumerate(all_ciphers):
            var = tk.BooleanVar(value=True)
            self.cipher_vars[cname] = var
            cb = tk.Checkbutton(
                cb_frame,
                text=cname,
                variable=var,
                font=("Segoe UI", 8),
                bg="#ffffff",
                activebackground="#ffffff"
            )
            col = idx % 4
            row = idx // 4
            cb.grid(row=row, column=col, sticky="w", padx=6, pady=2)
            
        run_btn = tk.Button(
            control_frame,
            text="RUN COMPARISON BENCHMARK",
            font=("Segoe UI", 9, "bold"),
            bg="#2563eb",
            fg="#ffffff",
            relief=tk.FLAT,
            padx=16,
            pady=5,
            cursor="hand2",
            command=self._execute_comparison
        )
        run_btn.pack(anchor="w", padx=12, pady=(4, 10))
        
        # Table of Results (Treeview)
        table_frame = tk.Frame(self.content_container, bg="#ffffff", bd=1, relief=tk.SOLID)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=2)
        
        columns = ("cipher", "category", "in_len", "out_len", "enc_time", "dec_time", "round_trip", "notes")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=9)
        
        self.tree.heading("cipher", text="Algorithm Name")
        self.tree.heading("category", text="Category")
        self.tree.heading("in_len", text="Input Len")
        self.tree.heading("out_len", text="Cipher Len")
        self.tree.heading("enc_time", text="Enc Time (ms)")
        self.tree.heading("dec_time", text="Dec Time (ms)")
        self.tree.heading("round_trip", text="Round-Trip")
        self.tree.heading("notes", text="Implementation Notes")
        
        self.tree.column("cipher", width=160, anchor="w")
        self.tree.column("category", width=150, anchor="w")
        self.tree.column("in_len", width=70, anchor="center")
        self.tree.column("out_len", width=70, anchor="center")
        self.tree.column("enc_time", width=95, anchor="e")
        self.tree.column("dec_time", width=95, anchor="e")
        self.tree.column("round_trip", width=80, anchor="center")
        self.tree.column("notes", width=220, anchor="w")
        
        tree_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.set_status("Option 9: Algorithm Comparison ready. Click 'Run Comparison Benchmark'.")

    def _execute_comparison(self):
        text = self.compare_input.get().strip()
        if not text:
            self.set_status("Please provide non-empty plaintext for benchmark.", is_error=True)
            return
            
        selected = [c for c, var in self.cipher_vars.items() if var.get()]
        if not selected:
            self.set_status("Select at least one cipher to compare.", is_error=True)
            return
            
        # Clear existing rows
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        t0 = time.perf_counter()
        results = compare_ciphers(selected, text)
        total_time = time.perf_counter() - t0
        
        for r in results:
            rt_str = "Passed" if r["round_trip_success"] else "Review"
            self.tree.insert("", tk.END, values=(
                r["cipher_name"],
                r["type"],
                r["input_len"],
                r["ciphertext_len"],
                f"{r['encrypt_time_ms']:.4f}",
                f"{r['decrypt_time_ms']:.4f}",
                rt_str,
                r["notes"] or r["status"]
            ))
            
        self.set_exec_time(total_time)
        self.set_status(f"Benchmark completed for {len(results)} ciphers.", is_success=True)

    # -------------------------------------------------------------
    # OPTIONS 10 & 11: FILE ENCRYPTION / DECRYPTION VIEW
    # -------------------------------------------------------------
    def show_file_view(self, mode: str = "encrypt"):
        self.file_mode = mode.lower()
        self._clear_content_container()
        
        opt_num = "10" if self.file_mode == "encrypt" else "11"
        action_title = "Encrypt Text File" if self.file_mode == "encrypt" else "Decrypt Text File"
        
        # Header
        header = tk.Frame(self.content_container, bg="#ffffff", bd=1, relief=tk.SOLID)
        header.pack(fill=tk.X, pady=(0, 10), padx=2)
        
        tk.Label(
            header,
            text=f"{opt_num}  {action_title}",
            font=("Segoe UI", 13, "bold"),
            bg="#ffffff",
            fg="#1e293b"
        ).pack(anchor="w", padx=12, pady=(10, 2))
        
        tk.Label(
            header,
            text="Load a UTF-8 text file, select a classical cipher, enter the key, preview results, "
                 "and safely save output to a distinct destination file without overwriting the input.",
            font=("Segoe UI", 8),
            bg="#ffffff",
            fg="#64748b"
        ).pack(anchor="w", padx=12, pady=(0, 8))
        
        # File selector and configuration card
        card = tk.Frame(self.content_container, bg="#ffffff", bd=1, relief=tk.SOLID)
        card.pack(fill=tk.X, pady=(0, 10), padx=2)
        
        # Row 1: File selection
        r1 = tk.Frame(card, bg="#ffffff")
        r1.pack(fill=tk.X, padx=12, pady=(8, 4))
        
        tk.Label(r1, text="Selected File:", font=("Segoe UI", 9, "bold"), bg="#ffffff").pack(side=tk.LEFT)
        self.file_path_var = tk.StringVar(value="No file selected")
        file_path_entry = tk.Entry(r1, textvariable=self.file_path_var, font=("Segoe UI", 9), state="readonly", width=55)
        file_path_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        browse_btn = tk.Button(
            r1,
            text="Browse File...",
            font=("Segoe UI", 8, "bold"),
            bg="#f1f5f9",
            fg="#1e293b",
            relief=tk.SOLID,
            bd=1,
            cursor="hand2",
            command=self._browse_input_file
        )
        browse_btn.pack(side=tk.LEFT)
        
        # Row 2: Cipher and Key selection
        r2 = tk.Frame(card, bg="#ffffff")
        r2.pack(fill=tk.X, padx=12, pady=(4, 8))
        
        tk.Label(r2, text="Cipher:", font=("Segoe UI", 9, "bold"), bg="#ffffff").pack(side=tk.LEFT)
        self.file_cipher_var = tk.StringVar(value="Caesar Cipher")
        cipher_dropdown = ttk.Combobox(
            r2,
            textvariable=self.file_cipher_var,
            values=[info["name"] for info in CIPHER_GUIDES.values()],
            state="readonly",
            width=20
        )
        cipher_dropdown.pack(side=tk.LEFT, padx=(6, 16))
        cipher_dropdown.bind("<<ComboboxSelected>>", self._on_file_cipher_changed)
        
        tk.Label(r2, text="Key:", font=("Segoe UI", 9, "bold"), bg="#ffffff").pack(side=tk.LEFT)
        self.file_key_entry = tk.Entry(r2, font=("Consolas", 9), width=24)
        self.file_key_entry.insert(0, "5")
        self.file_key_entry.pack(side=tk.LEFT, padx=(6, 16))
        
        process_btn = tk.Button(
            r2,
            text=f"PROCESS ({self.file_mode.upper()})",
            font=("Segoe UI", 8, "bold"),
            bg="#16a34a" if self.file_mode == "encrypt" else "#2563eb",
            fg="#ffffff",
            relief=tk.FLAT,
            cursor="hand2",
            command=self._process_file_action
        )
        process_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        save_btn = tk.Button(
            r2,
            text="Save Output As...",
            font=("Segoe UI", 8, "bold"),
            bg="#0284c7",
            fg="#ffffff",
            relief=tk.FLAT,
            cursor="hand2",
            command=self._save_file_action
        )
        save_btn.pack(side=tk.LEFT)
        
        # Two-pane previews: Source File Preview & Processed Output Preview
        panes = tk.Frame(self.content_container, bg="#f8fafc")
        panes.pack(fill=tk.BOTH, expand=True, padx=2)
        
        p1 = tk.LabelFrame(panes, text=" Source File Content Preview ", font=("Segoe UI", 9, "bold"), bg="#ffffff")
        p1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))
        self.file_input_preview = tk.Text(p1, font=("Segoe UI", 9), wrap=tk.WORD, bd=0, padx=8, pady=8)
        self.file_input_preview.pack(fill=tk.BOTH, expand=True)
        
        p2 = tk.LabelFrame(panes, text=" Processed Output Preview ", font=("Segoe UI", 9, "bold"), bg="#ffffff")
        p2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(6, 0))
        self.file_output_preview = tk.Text(p2, font=("Segoe UI", 9), wrap=tk.WORD, bd=0, padx=8, pady=8)
        self.file_output_preview.pack(fill=tk.BOTH, expand=True)
        
        self.loaded_file_content = ""
        self.processed_file_content = ""
        self.current_loaded_filepath = ""
        self.set_status(f"Option {opt_num}: {action_title} ready. Choose a file to start.")

    def _on_file_cipher_changed(self, event=None):
        name = self.file_cipher_var.get()
        # Find default key
        for info in CIPHER_GUIDES.values():
            if info["name"] == name:
                self.file_key_entry.delete(0, tk.END)
                self.file_key_entry.insert(0, info["default_key"])
                break

    def _browse_input_file(self):
        chosen = filedialog.askopenfilename(
            title="Select Text File",
            filetypes=[("Text Files (*.txt)", "*.txt"), ("All Files (*.*)", "*.*")]
        )
        if chosen:
            try:
                content, meta = read_text_file(chosen)
                self.current_loaded_filepath = chosen
                self.loaded_file_content = content
                self.file_path_var.set(chosen)
                self.file_input_preview.delete("1.0", tk.END)
                self.file_input_preview.insert("1.0", content[:10000])  # preview first 10k chars
                self.file_output_preview.delete("1.0", tk.END)
                self.set_status(f"Loaded '{meta['filename']}' ({meta['filesize_bytes']} bytes, {meta['char_count']} chars).", is_success=True)
            except FileOperationError as exc:
                self.set_status(str(exc), is_error=True)
                messagebox.showerror("File Read Error", str(exc))

    def _process_file_action(self):
        if not self.loaded_file_content:
            self.set_status("Please select and load a file first.", is_error=True)
            return
            
        cname = self.file_cipher_var.get()
        key = self.file_key_entry.get().strip()
        
        t0 = time.perf_counter()
        try:
            output, note = process_file_cipher(self.loaded_file_content, cname, key, mode=self.file_mode)
            elapsed = time.perf_counter() - t0
            self.processed_file_content = output
            self.file_output_preview.delete("1.0", tk.END)
            self.file_output_preview.insert("1.0", output[:10000])
            self.set_exec_time(elapsed)
            msg = f"Processed {len(output)} chars using {cname}."
            if note:
                msg += f" ({note})"
            self.set_status(msg, is_success=True)
        except Exception as exc:
            self.set_status(f"File Processing Error: {str(exc)}", is_error=True)
            messagebox.showerror("Processing Error", str(exc))

    def _save_file_action(self):
        if not self.processed_file_content:
            self.set_status("No processed output to save. Process a file first.", is_error=True)
            return
            
        default_name = "encrypted_output.txt" if self.file_mode == "encrypt" else "decrypted_output.txt"
        save_path = filedialog.asksaveasfilename(
            title="Save Output File As",
            initialfile=default_name,
            filetypes=[("Text Files (*.txt)", "*.txt"), ("All Files (*.*)", "*.*")]
        )
        if save_path:
            # Check accidental overwrite of input file
            if os.path.abspath(save_path) == os.path.abspath(self.current_loaded_filepath):
                confirm = messagebox.askyesno(
                    "Overwrite Warning",
                    "The selected destination is the SAME as the input source file.\n"
                    "Are you sure you want to overwrite your original input file?"
                )
                if not confirm:
                    return
            try:
                chars_written = write_text_file(save_path, self.processed_file_content)
                self.set_status(f"Successfully saved {chars_written} characters to '{os.path.basename(save_path)}'.", is_success=True)
                messagebox.showinfo("File Saved", f"Successfully saved to:\n{save_path}")
            except FileOperationError as exc:
                self.set_status(str(exc), is_error=True)
                messagebox.showerror("Save Error", str(exc))

    # -------------------------------------------------------------
    # OPTION 12: HELP & EDUCATIONAL THEORY
    # -------------------------------------------------------------
    def show_help_view(self):
        self._clear_content_container()
        
        help_card = tk.Frame(self.content_container, bg="#ffffff", bd=1, relief=tk.SOLID)
        help_card.pack(fill=tk.BOTH, expand=True, padx=2)
        
        tk.Label(
            help_card,
            text="12  Toolkit Documentation & Cryptographic Guide",
            font=("Segoe UI", 13, "bold"),
            bg="#ffffff",
            fg="#1e293b"
        ).pack(anchor="w", padx=14, pady=(10, 2))
        
        tk.Label(
            help_card,
            text="Final Year ECM Network Security Mini-Project (2026-27)",
            font=("Segoe UI", 9),
            bg="#ffffff",
            fg="#64748b"
        ).pack(anchor="w", padx=14, pady=(0, 6))
        
        help_text = tk.Text(help_card, font=("Segoe UI", 9), wrap=tk.WORD, bd=0, padx=12, pady=10)
        scroll = ttk.Scrollbar(help_card, orient="vertical", command=help_text.yview)
        help_text.configure(yscrollcommand=scroll.set)
        
        help_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        docs_content = """
================================================================================
CLASSICAL CRYPTOGRAPHY TOOLKIT - EDUCATIONAL REFERENCE MANUAL
Course: Network Security | Class: Final Year ECM (2026-27)
================================================================================

1. CAESAR CIPHER
   - Principle: Monoalphabetic substitution where every letter is shifted by integer k (mod 26).
   - Key: Integer shift value k (e.g. 5).
   - Case & Symbol Handling: Uppercase and lowercase are shifted independently; spaces and punctuation preserved.
   - Verified Vector: Plaintext "NETWORK SECURITY" with key 5 produces "SJYBTWP XJHZWNYD".
   - Vulnerability: 25 possible keys; trivial to break via exhaustive brute force or letter frequency analysis.

2. MONOALPHABETIC SUBSTITUTION CIPHER
   - Principle: Each letter of the plaintext alphabet maps to a unique permutation of the alphabet.
   - Key: 26 distinct letters (e.g. QWERTYUIOPASDFGHJKLZXCVBNM) or a keyword.
   - Key Space: 26! ≈ 4.03 × 10^26 possible permutations.
   - Vulnerability: Vulnerable to frequency analysis of single letters (ETAOIN SHRDLU), bigrams (TH, HE), and trigrams.

3. PLAYFAIR CIPHER
   - Principle: Practical digraphic substitution using a 5x5 key matrix (invented 1854).
   - Key: Alphabetic keyword. Letters I and J share a single matrix position.
   - Rules:
     * Digraphs with identical letters insert filler 'X'.
     * Same row: shift right; same column: shift down; rectangle: swap column coordinates.
     * Decryption reverses row/col shifts (left/up).

4. HILL CIPHER
   - Principle: Polygraphic linear algebraic substitution: C = (P * K) mod 26.
   - Key: Invertible square matrix (2x2 or 3x3) modulo 26.
   - Strict Invertibility Rule: gcd(det(K), 26) must equal 1. Reject keys where det is 0 or divisible by 2 or 13.
   - Vulnerability: Known-plaintext attack easily calculates K^(-1) via elementary modular matrix inversion.

5. VIGENÈRE CIPHER
   - Principle: Polyalphabetic substitution using a repeating keyword stream.
   - Key: Alphabetic keyword (e.g. "SECURITY").
   - Decryption: P_i = (C_i - K_j + 26) mod 26. Non-alphabetic characters do not advance the keystream.
   - Vulnerability: Kasiski examination and Friedman Index of Coincidence reveal keyword length.

6. ONE-TIME PAD (VERNAM CIPHER)
   - Principle: Information-Theoretic Security (perfect secrecy proven by Claude Shannon in 1949).
   - Mandatory Requirements:
     1. Key must be generated uniformly at random (CSPRNG via Python secrets module).
     2. Key length must strictly equal the message length.
     3. Key must be kept strictly secret.
     4. Key must NEVER be reused (two-time pad crib dragging vulnerability).

7. RAIL FENCE CIPHER
   - Principle: Geometric transposition cipher writing text in a zigzag across k rails (depth).
   - Key: Integer number of rails >= 2.
   - Reversibility: Fully preserves all characters including spaces and punctuation.

8. COLUMNAR TRANSPOSITION CIPHER
   - Principle: Text written in rows of width W, read column-by-column according to alphabetical key rank.
   - Irregular Rectangles: Our algorithm handles partial final rows with exact column length tracking.

9. COMPARISON ENGINE (MENU OPTION 9)
   - Benchmarks encryption/decryption execution speed in milliseconds and monitors output length.
   - Demonstrates that lower execution latency does not equate to higher cryptographic strength.

10 & 11. FILE ENCRYPTION / DECRYPTION (MENU OPTIONS 10 & 11)
   - Safely process UTF-8 text files with live preview before saving to a separate destination.

13. EXIT (MENU OPTION 13)
   - Confirms application exit and cleans up resources.

IMPORTANT CYBERSECURITY DISCLAIMER:
These classical ciphers are strictly educational tools designed to teach historical cryptographic
principles and cryptanalysis. They MUST NOT be used to protect real-world sensitive data.
================================================================================
"""
        help_text.insert("1.0", docs_content.strip())
        help_text.config(state="disabled")
        self.set_status("Option 12: Help & Theory loaded.")

    # -------------------------------------------------------------
    # OPTION 13: EXIT
    # -------------------------------------------------------------
    def confirm_exit(self):
        confirm = messagebox.askyesno(
            "Exit Application",
            "Are you sure you want to exit the Classical Cryptography Toolkit?"
        )
        if confirm:
            self.root.destroy()


def launch_gui():
    """Entry point to launch the Tkinter GUI."""
    root = tk.Tk()
    app = ToolkitGUI(root)
    root.mainloop()


if __name__ == "__main__":
    launch_gui()
