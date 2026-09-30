/**
 * Classical Cryptography Toolkit - Web Client Logic
 * Final Year ECM Network Security Mini-Project
 */

// Local dictionary of cipher guides & test vectors (fallback and instant client data)
const CIPHERS_DATA = {
  "Caesar Cipher": {
    category: "Substitution Cipher",
    formula: "C_i = (P_i + k) mod 26",
    desc: "Monoalphabetic shift cipher. Shifts each alphabet letter forward by fixed key k (mod 26). Case, spaces, and punctuation are preserved.",
    keyPrompt: "Shift Key (Integer 0–25):",
    keyHint: "Enter integer shift value (e.g. 5)",
    defaultKey: "5",
    defaultSample: "NETWORK SECURITY",
    verifiedOutput: "SJYBTWP XJHZWNYD",
    isOtp: false
  },
  "Monoalphabetic Cipher": {
    category: "Substitution Cipher",
    formula: "C_i = f(P_i)  where f is a bijection across A-Z",
    desc: "Fixed 1-to-1 letter mapping using a 26-letter substitution alphabet or keyword-expanded permutation. Case and punctuation preserved.",
    keyPrompt: "26-Letter Permutation or Keyword:",
    keyHint: "Enter 26 unique letters (e.g. QWERTY...) or a keyword",
    defaultKey: "QWERTYUIOPASDFGHJKLZXCVBNM",
    defaultSample: "CLASSICAL CRYPTOGRAPHY",
    isOtp: false
  },
  "Playfair Cipher": {
    category: "Substitution Cipher (Polygraphic)",
    formula: "5x5 Matrix Digraph Rules (Row: Right, Col: Down, Rectangle: Swap)",
    desc: "Digraphic substitution using 5x5 matrix (J combined with I). Automatically inserts filler 'X' (or 'Q') between identical pairs and pads odd lengths.",
    keyPrompt: "Alphabetic Keyword:",
    keyHint: "Enter word (e.g. MONARCHY)",
    defaultKey: "MONARCHY",
    defaultSample: "INSTRUMENTS",
    isOtp: false
  },
  "Hill Cipher": {
    category: "Substitution Cipher (Linear Algebra)",
    formula: "C = (P * K) mod 26  |  det(K) must satisfy gcd(det(K), 26) = 1",
    desc: "Polygraphic modular matrix multiplication. Key matrix must be strictly invertible modulo 26; rejects invalid keys where det is 0 or divisible by 2 or 13.",
    keyPrompt: "Key Matrix (2x2 or 3x3 integers or letters):",
    keyHint: "Enter '3 3 2 5' (2x2) or 'HILL' or 9 numbers for 3x3",
    defaultKey: "3 3 2 5",
    defaultSample: "HELP",
    isOtp: false
  },
  "Vigenere Cipher": {
    category: "Substitution Cipher (Polyalphabetic)",
    formula: "C_i = (P_i + K_j) mod 26  |  j advances for alphabetic chars only",
    desc: "Polyalphabetic substitution using a repeating keyword keystream. Spaces and punctuation are preserved without advancing the key index.",
    keyPrompt: "Alphabetic Keyword:",
    keyHint: "Enter keyword (e.g. SECURITY)",
    defaultKey: "SECURITY",
    defaultSample: "CRYPTOGRAPHY AND NETWORK SECURITY",
    isOtp: false
  },
  "One-Time Pad": {
    category: "Substitution Cipher (Shannon Perfect Secrecy)",
    formula: "C_i = (P_i + K_i) mod 26  |  Uniformly random, equal length, used once",
    desc: "Information-theoretic security. The key must be generated via CSPRNG, strictly match the message length, and NEVER be reused.",
    keyPrompt: "Random Key (Equal length to letters):",
    keyHint: "Leave blank to auto-generate secure CSPRNG key",
    defaultKey: "",
    defaultSample: "PERFECT SECRECY",
    isOtp: true
  },
  "Rail Fence Cipher": {
    category: "Transposition Cipher (Geometric)",
    formula: "Cycle T = 2*(k - 1)  |  Row-by-row readout from zigzag fence",
    desc: "Transposition cipher: plaintext is written in a zigzag across k parallel rails, then read horizontally row-by-row. Round-trip preserves all characters.",
    keyPrompt: "Number of Rails (Depth >= 2):",
    keyHint: "Enter integer depth >= 2 (e.g. 3)",
    defaultKey: "3",
    defaultSample: "DEFEND THE EAST WALL",
    isOtp: false
  },
  "Columnar Transposition Cipher": {
    category: "Transposition Cipher (Permutation Grid)",
    formula: "Grid width W = len(key)  |  Columns read in alphabetical key order",
    desc: "Text written in rows of key width W, then read column-by-column according to key character rank. Irregular rectangular grids are accurately handled.",
    keyPrompt: "Keyword or Column Permutation:",
    keyHint: "Enter word (e.g. ZEBRA) or numbers (e.g. 3 1 4 2)",
    defaultKey: "ZEBRA",
    defaultSample: "WE ARE DISCOVERED FLEE AT ONCE",
    isOtp: false
  }
};

let currentCipher = "Caesar Cipher";
let activeFileMode = "encrypt";
let loadedFileContent = "";
let processedFileContent = "";

// DOM Elements
const pageTitle = document.getElementById("page-title");
const categoryBadge = document.getElementById("category-badge");
const cipherFormula = document.getElementById("cipher-formula");
const cipherDesc = document.getElementById("cipher-desc");
const keyLabel = document.getElementById("key-label");
const keyHint = document.getElementById("key-hint");
const keyInput = document.getElementById("key-input");
const otpGenBtn = document.getElementById("otp-gen-btn");
const plaintextInput = document.getElementById("plaintext-input");
const outputText = document.getElementById("output-text");
const ptCharCount = document.getElementById("pt-char-count");
const ctCharCount = document.getElementById("ct-char-count");
const latencyText = document.getElementById("latency-text");
const toast = document.getElementById("toast");

// Views
const cipherView = document.getElementById("cipher-view");
const compareView = document.getElementById("compare-view");
const fileView = document.getElementById("file-view");
const helpView = document.getElementById("help-view");

// Initialize application
document.addEventListener("DOMContentLoaded", () => {
  setupNavigation();
  setupCipherControls();
  setupCompareControls();
  setupFileControls();
  updateCharCounts();
  showCipher("Caesar Cipher");
});

function showToast(message, isError = false) {
  toast.textContent = message;
  toast.className = `toast show ${isError ? "error" : "success"}`;
  setTimeout(() => {
    toast.className = "toast";
  }, 3500);
}

function updateCharCounts() {
  ptCharCount.textContent = `${plaintextInput.value.length} chars`;
  ctCharCount.textContent = `${outputText.value.length} chars`;
}

plaintextInput.addEventListener("input", updateCharCounts);

function setupNavigation() {
  document.querySelectorAll(".nav-item").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".nav-item").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");

      const cipher = btn.dataset.cipher;
      const view = btn.dataset.view;

      if (cipher) {
        showCipher(cipher);
      } else if (view === "compare") {
        showCompareView();
      } else if (view === "file-crypto") {
        const mode = btn.id === "nav-file-enc" ? "encrypt" : "decrypt";
        showFileView(mode);
      } else if (view === "help") {
        showHelpView();
      }
    });
  });
}

function showCipher(cipherName) {
  currentCipher = cipherName;
  const data = CIPHERS_DATA[cipherName];

  cipherView.style.display = "block";
  compareView.style.display = "none";
  fileView.style.display = "none";
  helpView.style.display = "none";

  pageTitle.textContent = cipherName.toUpperCase();
  categoryBadge.textContent = data.category;
  cipherFormula.textContent = data.formula;
  cipherDesc.textContent = data.desc;
  keyLabel.textContent = data.keyPrompt;
  keyHint.textContent = data.keyHint;
  keyInput.value = data.defaultKey;
  otpGenBtn.style.display = data.isOtp ? "inline-flex" : "none";

  plaintextInput.value = data.defaultSample;
  outputText.value = "";
  updateCharCounts();
  latencyText.textContent = "Ready";
}

function showCompareView() {
  cipherView.style.display = "none";
  compareView.style.display = "block";
  fileView.style.display = "none";
  helpView.style.display = "none";

  pageTitle.textContent = "9. ALGORITHM COMPARISON";
  categoryBadge.textContent = "Comparative Analysis";
}

function showFileView(mode = "encrypt") {
  activeFileMode = mode;
  cipherView.style.display = "none";
  compareView.style.display = "none";
  fileView.style.display = "block";
  helpView.style.display = "none";

  const num = mode === "encrypt" ? "10" : "11";
  const title = mode === "encrypt" ? "ENCRYPT TEXT FILE" : "DECRYPT TEXT FILE";
  pageTitle.textContent = `${num}. ${title}`;
  categoryBadge.textContent = "File Cryptography";
  document.getElementById("file-mode-title").textContent = `${num}. ${title}`;
  document.getElementById("file-process-btn").textContent = `PROCESS (${mode.toUpperCase()})`;
}

function showHelpView() {
  cipherView.style.display = "none";
  compareView.style.display = "none";
  fileView.style.display = "none";
  helpView.style.display = "block";

  pageTitle.textContent = "12. HELP & CRYPTOGRAPHIC THEORY";
  categoryBadge.textContent = "Reference Manual";
}

function setupCipherControls() {
  // Load Sample
  document.getElementById("load-sample-btn").addEventListener("click", () => {
    const data = CIPHERS_DATA[currentCipher];
    if (data) {
      keyInput.value = data.defaultKey;
      plaintextInput.value = data.defaultSample;
      outputText.value = "";
      updateCharCounts();
      showToast(`Loaded verified sample vector for ${currentCipher}.`);
    }
  });

  // Clear Plaintext
  document.getElementById("clear-pt-btn").addEventListener("click", () => {
    plaintextInput.value = "";
    outputText.value = "";
    updateCharCounts();
  });

  // Copy Output
  document.getElementById("copy-btn").addEventListener("click", () => {
    if (!outputText.value) {
      showToast("Output is empty. Nothing to copy.", true);
      return;
    }
    navigator.clipboard.writeText(outputText.value).then(() => {
      showToast("Output copied to clipboard!");
    });
  });

  // Use as Input (Swap)
  document.getElementById("swap-btn").addEventListener("click", () => {
    if (!outputText.value) {
      showToast("No output to transfer.", true);
      return;
    }
    plaintextInput.value = outputText.value;
    outputText.value = "";
    updateCharCounts();
    showToast("Transferred output to plaintext input.");
  });

  // Generate OTP Key
  otpGenBtn.addEventListener("click", async () => {
    const text = plaintextInput.value;
    const alphaCount = (text.match(/[a-zA-Z]/g) || []).length || 16;
    try {
      const res = await fetch("/api/generate-otp", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ length: alphaCount })
      });
      const data = await res.json();
      keyInput.value = data.key;
      showToast(`Generated CSPRNG OTP key (${alphaCount} characters).`);
    } catch (e) {
      // Fallback client generation
      const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
      let key = "";
      for (let i = 0; i < alphaCount; i++) {
        key += alphabet[Math.floor(Math.random() * alphabet.length)];
      }
      keyInput.value = key;
      showToast(`Generated OTP key (${alphaCount} characters).`);
    }
  });

  // Encrypt Button
  document.getElementById("encrypt-btn").addEventListener("click", async () => {
    const pt = plaintextInput.value;
    const key = keyInput.value;

    const t0 = performance.now();
    try {
      const res = await fetch("/api/encrypt", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          cipher: currentCipher,
          plaintext: pt,
          key: key
        })
      });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || "Encryption failed.");
      }
      const elapsed = (performance.now() - t0).toFixed(3);
      outputText.value = data.ciphertext;
      if (data.key_used && !keyInput.value) {
        keyInput.value = data.key_used;
      }
      updateCharCounts();
      latencyText.textContent = `${data.exec_time_ms ? data.exec_time_ms.toFixed(3) : elapsed} ms`;
      showToast(`Successfully encrypted via ${currentCipher}.`);
    } catch (err) {
      showToast(err.message, true);
    }
  });

  // Decrypt Button
  document.getElementById("decrypt-btn").addEventListener("click", async () => {
    const ct = plaintextInput.value; // User decrypts whatever is in input box
    const key = keyInput.value;

    const t0 = performance.now();
    try {
      const res = await fetch("/api/decrypt", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          cipher: currentCipher,
          ciphertext: ct,
          key: key
        })
      });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || "Decryption failed.");
      }
      const elapsed = (performance.now() - t0).toFixed(3);
      outputText.value = data.plaintext;
      updateCharCounts();
      latencyText.textContent = `${data.exec_time_ms ? data.exec_time_ms.toFixed(3) : elapsed} ms`;
      showToast(`Successfully decrypted via ${currentCipher}.`);
    } catch (err) {
      showToast(err.message, true);
    }
  });
}

function setupCompareControls() {
  document.getElementById("run-compare-btn").addEventListener("click", async () => {
    const text = document.getElementById("compare-text-input").value;
    const selectedBoxes = Array.from(document.querySelectorAll(".ciphers-selector-grid input:checked"));
    const selected = selectedBoxes.map(b => b.value);

    if (!text.trim()) {
      showToast("Please enter benchmark text.", true);
      return;
    }
    if (selected.length === 0) {
      showToast("Select at least one cipher.", true);
      return;
    }

    const tbody = document.getElementById("compare-tbody");
    tbody.innerHTML = `<tr><td colspan="8" style="text-align:center; padding: 2rem;">Running benchmarks across ${selected.length} algorithms...</td></tr>`;

    try {
      const res = await fetch("/api/compare", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ciphers: selected,
          plaintext: text
        })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Benchmark failed.");

      tbody.innerHTML = "";
      data.results.forEach(r => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td><strong>${r.cipher_name}</strong></td>
          <td>${r.type}</td>
          <td>${r.input_len}</td>
          <td>${r.ciphertext_len}</td>
          <td>${r.encrypt_time_ms.toFixed(4)}</td>
          <td>${r.decrypt_time_ms.toFixed(4)}</td>
          <td><span class="pass-tag">${r.round_trip_success ? "Passed" : "Review"}</span></td>
          <td style="font-size: 0.78rem;">${r.notes || r.status}</td>
        `;
        tbody.appendChild(tr);
      });
      showToast(`Benchmark complete for ${data.results.length} ciphers.`);
    } catch (err) {
      tbody.innerHTML = `<tr><td colspan="8" style="color:var(--accent-rose); text-align:center;">${err.message}</td></tr>`;
      showToast(err.message, true);
    }
  });
}

function setupFileControls() {
  const dropzone = document.getElementById("file-dropzone");
  const fileInput = document.getElementById("file-upload-input");
  const loadedFileName = document.getElementById("loaded-file-name");
  const inputPreview = document.getElementById("file-input-preview");
  const outputPreview = document.getElementById("file-output-preview");
  const cipherSelect = document.getElementById("file-cipher-select");
  const keyInput = document.getElementById("file-key-input");
  const processBtn = document.getElementById("file-process-btn");
  const downloadBtn = document.getElementById("file-download-btn");

  dropzone.addEventListener("click", () => fileInput.click());

  dropzone.addEventListener("dragover", e => {
    e.preventDefault();
    dropzone.style.borderColor = "var(--primary)";
  });
  dropzone.addEventListener("dragleave", () => {
    dropzone.style.borderColor = "rgba(148, 163, 184, 0.25)";
  });
  dropzone.addEventListener("drop", e => {
    e.preventDefault();
    dropzone.style.borderColor = "rgba(148, 163, 184, 0.25)";
    if (e.dataTransfer.files.length) {
      handleFileSelected(e.dataTransfer.files[0]);
    }
  });

  fileInput.addEventListener("change", () => {
    if (fileInput.files.length) {
      handleFileSelected(fileInput.files[0]);
    }
  });

  function handleFileSelected(file) {
    loadedFileName.textContent = `${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
    const reader = new FileReader();
    reader.onload = e => {
      loadedFileContent = e.target.result;
      inputPreview.value = loadedFileContent.slice(0, 10000);
      outputPreview.value = "";
      downloadBtn.disabled = true;
      showToast(`Loaded ${file.name} successfully.`);
    };
    reader.readAsText(file);
  }

  cipherSelect.addEventListener("change", () => {
    const cData = CIPHERS_DATA[cipherSelect.value];
    if (cData) {
      keyInput.value = cData.defaultKey;
    }
  });

  processBtn.addEventListener("click", async () => {
    if (!loadedFileContent) {
      showToast("Please choose or drop a text file first.", true);
      return;
    }

    const cname = cipherSelect.value;
    const key = keyInput.value;
    const endpoint = activeFileMode === "encrypt" ? "/api/encrypt" : "/api/decrypt";
    const body = activeFileMode === "encrypt"
      ? { cipher: cname, plaintext: loadedFileContent, key: key }
      : { cipher: cname, ciphertext: loadedFileContent, key: key };

    try {
      const res = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Processing failed.");

      processedFileContent = activeFileMode === "encrypt" ? data.ciphertext : data.plaintext;
      outputPreview.value = processedFileContent.slice(0, 10000);
      downloadBtn.disabled = false;
      showToast(`File processed successfully with ${cname}!`);
    } catch (err) {
      showToast(err.message, true);
    }
  });

  downloadBtn.addEventListener("click", () => {
    if (!processedFileContent) return;
    const blob = new Blob([processedFileContent], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = activeFileMode === "encrypt" ? "encrypted_output.txt" : "decrypted_output.txt";
    a.click();
    URL.revokeObjectURL(url);
    showToast("Downloaded processed file.");
  });
}
