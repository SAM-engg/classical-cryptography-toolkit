"""
web_server.py - FastAPI Web Server for Classical Cryptography Toolkit
Final Year ECM Network Security Mini-Project (2026-27)

Runs on http://localhost:8000
Serves the modern web frontend and provides REST endpoints for all 8 ciphers.
"""

import os
import sys
import time
from typing import List, Optional, Any
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Ensure project root is in path
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
from src.comparison import compare_ciphers, CIPHER_METADATA
from src.validators import ValidationError

app = FastAPI(
    title="Classical Cryptography Toolkit API",
    description="REST API for Classical Cryptographic Algorithms (ECM Network Security)",
    version="1.0.0"
)

# Enable CORS for local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request Models
class EncryptRequest(BaseModel):
    cipher: str
    plaintext: str
    key: Optional[Any] = None


class DecryptRequest(BaseModel):
    cipher: str
    ciphertext: str
    key: Optional[Any] = None


class CompareRequest(BaseModel):
    ciphers: List[str]
    plaintext: str


class OtpGenRequest(BaseModel):
    length: int


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Classical Cryptography Toolkit",
        "course": "Network Security (ECM 2026-27)"
    }


@app.post("/api/generate-otp")
def api_generate_otp(req: OtpGenRequest):
    length = max(1, min(req.length, 100000))
    key = generate_otp_key(length)
    return {"key": key, "length": len(key)}


@app.post("/api/encrypt")
def api_encrypt(req: EncryptRequest):
    cname = req.cipher
    pt = req.plaintext
    k = req.key
    key_used = str(k) if k is not None else ""

    t0 = time.perf_counter()
    try:
        if cname == "Caesar Cipher":
            ct = caesar_encrypt(pt, k)
        elif cname == "Monoalphabetic Cipher":
            ct = monoalphabetic_encrypt(pt, k)
        elif cname == "Playfair Cipher":
            ct = playfair_encrypt(pt, k)
        elif cname == "Hill Cipher":
            ct = hill_encrypt(pt, k)
        elif cname == "Vigenere Cipher":
            ct = vigenere_encrypt(pt, k)
        elif cname == "One-Time Pad":
            ct, key_used = otp_encrypt(pt, k if (k and str(k).strip()) else None)
        elif cname == "Rail Fence Cipher":
            ct = rail_fence_encrypt(pt, k)
        elif cname == "Columnar Transposition Cipher":
            ct = columnar_encrypt(pt, k)
        else:
            raise ValidationError(f"Unsupported cipher '{cname}'.")

        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        return {
            "cipher": cname,
            "ciphertext": ct,
            "key_used": key_used,
            "exec_time_ms": elapsed_ms
        }
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.post("/api/decrypt")
def api_decrypt(req: DecryptRequest):
    cname = req.cipher
    ct = req.ciphertext
    k = req.key

    t0 = time.perf_counter()
    try:
        if cname == "Caesar Cipher":
            pt = caesar_decrypt(ct, k)
        elif cname == "Monoalphabetic Cipher":
            pt = monoalphabetic_decrypt(ct, k)
        elif cname == "Playfair Cipher":
            pt = playfair_decrypt(ct, k)
        elif cname == "Hill Cipher":
            pt = hill_decrypt(ct, k)
        elif cname == "Vigenere Cipher":
            pt = vigenere_decrypt(ct, k)
        elif cname == "One-Time Pad":
            pt = otp_decrypt(ct, k)
        elif cname == "Rail Fence Cipher":
            pt = rail_fence_decrypt(ct, k)
        elif cname == "Columnar Transposition Cipher":
            pt = columnar_decrypt(ct, k)
        else:
            raise ValidationError(f"Unsupported cipher '{cname}'.")

        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        return {
            "cipher": cname,
            "plaintext": pt,
            "exec_time_ms": elapsed_ms
        }
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.post("/api/compare")
def api_compare(req: CompareRequest):
    try:
        results = compare_ciphers(req.ciphers, req.plaintext)
        return {"results": results}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


# Mount the frontend web directory
web_dir = os.path.join(PROJECT_ROOT, "web")
if os.path.exists(web_dir):
    app.mount("/", StaticFiles(directory=web_dir, html=True), name="static")


def run_server(port: int = 8000):
    print("=" * 70)
    print(f" Starting Classical Cryptography Toolkit on http://localhost:{port}")
    print("=" * 70)
    uvicorn.run("web_server:app", host="127.0.0.1", port=port, log_level="info")


if __name__ == "__main__":
    run_server(8000)
