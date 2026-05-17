# 📄 RAG PDF Chatbot

Aplikasi chatbot berbasis **Retrieval-Augmented Generation (RAG)** yang memungkinkan kamu tanya jawab dengan dokumen PDF menggunakan AI. Dibangun dengan LangChain, FAISS, dan Groq LLM — **100% gratis**.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red)
![LangChain](https://img.shields.io/badge/LangChain-0.1+-green)
![Groq](https://img.shields.io/badge/LLM-Groq%20(Free)-orange)
[![Streamlit App](https://img.shields.io/badge/Streamlit-Live%20Demo-FF4B4B?logo=streamlit&logoColor=white)](https://devin-novansyah16-rag-chatbot-pdf.streamlit.app)

---

## 🌐 Live Demo

**👉 [devin-novansyah16-rag-chatbot-pdf.streamlit.app](https://devin-novansyah16-rag-chatbot-pdf.streamlit.app)**

> Langsung coba tanpa install apapun! Upload PDF kamu dan mulai tanya jawab.

---

## 🎯 Fitur

- 📤 **Upload PDF** — Dokumen apa saja, langsung diproses
- 🔍 **Semantic Search** — Mencari jawaban berdasarkan makna, bukan kata kunci
- 💬 **Chat History** — Riwayat percakapan tersimpan selama sesi
- 📎 **Source Kutipan** — Setiap jawaban disertai potongan teks sumbernya
- 🌐 **Multibahasa** — Mendukung dokumen dan pertanyaan Bahasa Indonesia
- ⚡ **Cepat** — Menggunakan Groq (LPU) untuk inferensi super cepat
- 🆓 **Gratis** — Tidak butuh kartu kredit, langsung bisa dipakai

---

## 🏗️ Arsitektur RAG

```
PDF Upload
    ↓
PyPDFLoader → Text Chunks (RecursiveCharacterTextSplitter)
    ↓
HuggingFace Embeddings (multilingual-MiniLM)
    ↓
FAISS Vectorstore (local)
    ↓
User Query → Semantic Retrieval (top-4 chunks)
    ↓
Groq LLM (llama-3.3-70b) → Answer + Sources
```

---

## 🚀 Cara Menjalankan Lokal

### 1. Clone & install
```bash
git clone https://github.com/devin-novansyah16/rag-chatbot-pdf.git
cd rag-chatbot-pdf
pip install -r requirements.txt
```

### 2. Dapatkan Groq API Key (gratis)
1. Daftar di [console.groq.com](https://console.groq.com)
2. Buat API Key baru
3. Copy key-nya (format: `gsk_...`)

### 3. Buat file secrets
```bash
mkdir .streamlit
```
Buat file `.streamlit/secrets.toml` dan isi:
```toml
GROQ_API_KEY = "gsk_xxxxxxxxxxxx"
```

### 4. Jalankan aplikasi
```bash
streamlit run app.py
```

---

## 📁 Struktur Project

```
rag-chatbot-pdf/
│
├── app.py                  # Streamlit UI utama
├── src/
│   ├── rag_pipeline.py     # Core RAG: load, embed, retrieve, answer
│   ├── utils.py            # Helper: file handling
│   └── __init__.py
│
├── .env.example            # Template environment variable
├── requirements.txt
└── README.md
```

---

## 🛠️ Tech Stack

| Komponen | Library | Keterangan |
|----------|---------|-----------|
| UI | Streamlit | Web app framework |
| PDF Loader | PyPDF | Ekstrak teks dari PDF |
| Text Splitter | LangChain | Chunking dokumen |
| Embeddings | HuggingFace (multilingual-MiniLM) | Gratis, support Bahasa Indonesia |
| Vector Store | FAISS | Similarity search lokal |
| LLM | Groq (llama-3.3-70b) | Gratis, sangat cepat |
| Orchestration | LangChain | RAG pipeline |
| Deploy | Streamlit Cloud | Hosting gratis |

---

## 💡 Contoh Pertanyaan

Setelah upload PDF, coba tanya:
- *"Apa isi utama dokumen ini?"*
- *"Ringkas dokumen ini dalam 5 poin!"*
- *"Apa yang dikatakan dokumen tentang [topik]?"*
- *"Sebutkan rekomendasi yang ada di dokumen!"*

---

## 🔭 Rencana Pengembangan

- [ ] Support multi-dokumen sekaligus
- [ ] Export chat history ke PDF
- [ ] Tambahkan model embedding lokal (Ollama)
- [ ] Tambah fitur highlight teks sumber di PDF

---

## 👤 Author

**Devin Novansyah**
- GitHub: [@devin-novansyah16](https://github.com/devin-novansyah16)

---

⭐ Jika bermanfaat, jangan lupa beri bintang!
