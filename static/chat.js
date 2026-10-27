"use strict";

const daftarPesan = document.getElementById("daftarPesan");
const formulir = document.getElementById("formulir");
const kolomPesan = document.getElementById("kolomPesan");
const tombolKirim = document.getElementById("tombolKirim");
const tombolBaru = document.getElementById("tombolBaru");
const indikator = document.getElementById("indikator");
const peringatan = document.getElementById("peringatan");

const riwayat = [];

const SAPAAN = "Halo, saya asisten AI yang memakai model dari Groq. Silakan tulis pertanyaan atau topik apa pun, lalu saya bantu jawab.";

function larikanHtml(teks) {
    return teks
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;");
}

function formatPesan(teks) {
    const aman = larikanHtml(teks)
        .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
        .replace(/`([^`]+)`/g, "<code>$1</code>");
    return aman
        .split(/\n{2,}/)
        .map((blok) => "<p>" + blok.replace(/\n/g, "<br>") + "</p>")
        .join("");
}

function tampilkanPesan(peran, teks, ralat) {
    const el = document.createElement("div");
    el.className = "pesan " + (peran === "user" ? "pesan-pengguna" : "pesan-asisten");
    if (ralat) {
        el.classList.add("pesan-ralat");
    }
    el.innerHTML = formatPesan(teks);
    daftarPesan.appendChild(el);
    daftarPesan.scrollTop = daftarPesan.scrollHeight;
    return el;
}

function aturMengetik(aktif) {
    indikator.hidden = !aktif;
    tombolKirim.disabled = aktif;
    if (aktif) {
        daftarPesan.scrollTop = daftarPesan.scrollHeight;
    }
}

async function kirimPesan(teks) {
    riwayat.push({ role: "user", content: teks });
    tampilkanPesan("user", teks, false);
    aturMengetik(true);
    try {
        const respons = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ messages: riwayat }),
        });
        const data = await respons.json();
        if (data.reply) {
            const ralat = Boolean(data.error);
            if (!ralat) {
                riwayat.push({ role: "assistant", content: data.reply });
            }
            tampilkanPesan("assistant", data.reply, ralat);
        } else {
            tampilkanPesan("assistant", data.error || "Terjadi kesalahan yang tidak dikenal.", true);
        }
    } catch (e) {
        tampilkanPesan("assistant", "Maaf, permintaan gagal dikirim. Periksa koneksi Anda lalu coba lagi.", true);
    } finally {
        aturMengetik(false);
        kolomPesan.focus();
    }
}

formulir.addEventListener("submit", (event) => {
    event.preventDefault();
    const teks = kolomPesan.value.trim();
    if (!teks || tombolKirim.disabled) {
        return;
    }
    kolomPesan.value = "";
    kolomPesan.style.height = "auto";
    kirimPesan(teks);
});

kolomPesan.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        formulir.requestSubmit();
    }
});

kolomPesan.addEventListener("input", () => {
    kolomPesan.style.height = "auto";
    kolomPesan.style.height = Math.min(kolomPesan.scrollHeight, 140) + "px";
});

tombolBaru.addEventListener("click", () => {
    riwayat.length = 0;
    daftarPesan.innerHTML = "";
    tampilkanPesan("assistant", SAPAAN, false);
    kolomPesan.focus();
});

async function mulai() {
    tampilkanPesan("assistant", SAPAAN, false);
    try {
        const respons = await fetch("/api/status");
        const data = await respons.json();
        if (!data.configured) {
            peringatan.hidden = false;
        }
    } catch (e) {
        peringatan.hidden = false;
    }
    kolomPesan.focus();
}

mulai();
