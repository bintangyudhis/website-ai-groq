import os
from pathlib import Path

import requests
from flask import Flask, jsonify, render_template, request

BASE_DIR = Path(__file__).resolve().parent


def muat_env():
    """Muat variabel dari berkas .env sederhana bila ada."""
    berkas = BASE_DIR / ".env"
    if not berkas.exists():
        return
    for baris in berkas.read_text(encoding="utf-8").splitlines():
        baris = baris.strip()
        if not baris or baris.startswith("#") or "=" not in baris:
            continue
        nama, nilai = baris.split("=", 1)
        os.environ.setdefault(nama.strip(), nilai.strip().strip('"').strip("'"))


muat_env()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "").strip()
GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile").strip()
if not GROQ_MODEL:
    GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_API_URL = os.environ.get(
    "GROQ_API_URL", "https://api.groq.com/openai/v1/chat/completions"
)

PESAN_SISTEM = (
    "Kamu adalah asisten AI yang ramah dan membantu. "
    "Jawablah dalam Bahasa Indonesia, kecuali pengguna memakai bahasa lain. "
    "Berikan jawaban yang jelas dan ringkas."
)

BATAS_RIWAYAT = 30
BATAS_KARAKTER = 4000

app = Flask(__name__)


@app.route("/")
def beranda():
    return render_template("index.html", model=GROQ_MODEL)


@app.route("/api/status")
def status():
    return jsonify({"configured": bool(GROQ_API_KEY), "model": GROQ_MODEL})


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    riwayat = data.get("messages")
    if not isinstance(riwayat, list) or not riwayat:
        return jsonify({"error": "Pesan tidak boleh kosong."}), 400

    bersih = []
    for item in riwayat[-BATAS_RIWAYAT:]:
        if not isinstance(item, dict):
            continue
        isi = str(item.get("content", "")).strip()
        if item.get("role") in ("user", "assistant") and isi:
            bersih.append({"role": item["role"], "content": isi[:BATAS_KARAKTER]})
    if not bersih or bersih[-1]["role"] != "user":
        return jsonify({"error": "Pesan terakhir harus berasal dari pengguna."}), 400

    if not GROQ_API_KEY:
        return jsonify(
            {
                "reply": (
                    "Kunci API Groq belum diatur, jadi saya belum bisa menjawab. "
                    "Salin berkas .env.example menjadi .env, isi GROQ_API_KEY "
                    "dengan kunci Anda, lalu jalankan ulang aplikasi ini."
                ),
                "error": "kunci_kosong",
            }
        )

    try:
        respons = requests.post(
            GROQ_API_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": GROQ_MODEL,
                "messages": [{"role": "system", "content": PESAN_SISTEM}] + bersih,
                "temperature": 0.7,
            },
            timeout=60,
        )
    except requests.RequestException:
        return (
            jsonify(
                {
                    "reply": "Maaf, koneksi ke layanan Groq gagal. Periksa jaringan Anda lalu coba lagi.",
                    "error": "jaringan",
                }
            ),
            502,
        )

    if respons.status_code != 200:
        return (
            jsonify(
                {
                    "reply": "Maaf, layanan Groq menolak permintaan ini. Periksa kembali kunci API dan model yang dipakai, lalu coba lagi.",
                    "error": "ditolak",
                }
            ),
            502,
        )

    try:
        payload = respons.json()
        teks = payload["choices"][0]["message"]["content"]
    except (ValueError, KeyError, IndexError, TypeError):
        return (
            jsonify(
                {
                    "reply": "Maaf, jawaban dari Groq tidak dapat dibaca. Silakan coba lagi.",
                    "error": "respons",
                }
            ),
            502,
        )

    return jsonify({"reply": teks})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))
