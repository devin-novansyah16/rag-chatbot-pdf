import streamlit as st
import os
from src.rag_pipeline import build_vectorstore, get_answer
from src.utils import save_uploaded_file, clear_vectorstore

st.set_page_config(page_title="RAG PDF Chatbot", page_icon="📄", layout="wide")

st.markdown("""
<style>
    .main-title { font-size: 2rem; font-weight: 700; color: #1a1a2e; }
    .sub-title  { color: #555; font-size: 0.95rem; margin-top: -10px; }
    .source-box { background: #fffbeb; border-left: 3px solid #f59e0b;
                  padding: 8px 12px; border-radius: 4px; font-size: 0.82rem; color: #555; }
    .status-ok  { color: #16a34a; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = None

try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    groq_api_key = None

with st.sidebar:
    st.markdown("## ⚙️ Pengaturan")
    st.markdown("---")

    if groq_api_key:
        st.success("🔑 API Key: Terhubung")
    else:
        groq_api_key = st.text_input("🔑 Groq API Key", type="password", placeholder="gsk_.....")

    st.markdown("---")
    st.markdown("### 📤 Upload Dokumen PDF")

    uploaded_file = st.file_uploader("Pilih file PDF", type=["pdf"])

    if uploaded_file and groq_api_key:
        if st.button("🚀 Proses Dokumen", use_container_width=True):
            with st.spinner("Membaca dan mengindeks dokumen..."):
                try:
                    pdf_path = save_uploaded_file(uploaded_file)
                    vs = build_vectorstore(pdf_path)
                    st.session_state.vectorstore = vs
                    st.session_state.pdf_name = uploaded_file.name
                    st.session_state.chat_history = []
                    st.success("✅ Dokumen siap!")
                except Exception as e:
                    st.error(f"Error: {e}")
    elif uploaded_file and not groq_api_key:
        st.warning("⚠️ Masukkan Groq API Key dulu!")

    if st.session_state.pdf_name:
        st.markdown("---")
        st.markdown(f"📄 **Aktif:** `{st.session_state.pdf_name}`")
        if st.button("🗑️ Hapus & Reset", use_container_width=True):
            clear_vectorstore()
            st.session_state.vectorstore = None
            st.session_state.pdf_name = None
            st.session_state.chat_history = []
            st.rerun()

    st.markdown("---")
    st.markdown("### 📚 Cara Pakai")
    st.markdown("""
1. Upload file **PDF**
2. Klik **Proses Dokumen**
3. Mulai **tanya jawab**!
    """)

st.markdown('<div class="main-title">📄 RAG PDF Chatbot</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Tanya apa saja tentang isi dokumen PDF kamu</div>', unsafe_allow_html=True)
st.markdown("---")

col1, col2, col3 = st.columns(3)
with col1:
    if groq_api_key:
        st.markdown("🔑 API Key: <span class='status-ok'>Terhubung</span>", unsafe_allow_html=True)
    else:
        st.markdown("🔑 API Key: ⬜ Belum diisi")
with col2:
    if st.session_state.pdf_name:
        st.markdown("📄 Dokumen: <span class='status-ok'>Siap</span>", unsafe_allow_html=True)
    else:
        st.markdown("📄 Dokumen: ⬜ Belum diupload")
with col3:
    st.markdown(f"💬 Pertanyaan: **{len(st.session_state.chat_history)}**")

st.markdown("---")

for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.write(chat["question"])
    with st.chat_message("assistant"):
        st.write(chat["answer"])
        if chat.get("sources"):
            with st.expander("📎 Sumber kutipan"):
                for i, src in enumerate(chat["sources"], 1):
                    st.markdown(f'<div class="source-box"><b>Kutipan {i}:</b> ...{src}...</div>', unsafe_allow_html=True)

if prompt := st.chat_input("Tanya sesuatu tentang dokumen..."):
    if not groq_api_key:
        st.error("⚠️ Masukkan Groq API Key di sidebar!")
    elif st.session_state.vectorstore is None:
        st.error("⚠️ Upload dan proses dokumen PDF dulu!")
    else:
        with st.chat_message("user"):
            st.write(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Sedang mencari jawaban..."):
                try:
                    result = get_answer(prompt, st.session_state.vectorstore, groq_api_key)
                    st.write(result["answer"])
                    sources = result.get("sources", [])
                    if sources:
                        with st.expander("📎 Sumber kutipan"):
                            for i, src in enumerate(sources, 1):
                                st.markdown(f'<div class="source-box"><b>Kutipan {i}:</b> ...{src}...</div>', unsafe_allow_html=True)
                    st.session_state.chat_history.append({"question": prompt, "answer": result["answer"], "sources": sources})
                except Exception as e:
                    st.error(f"Error: {e}")

if not st.session_state.chat_history and st.session_state.vectorstore:
    st.info("💡 Dokumen siap! Coba tanya: *'Apa isi utama dokumen ini?'*")
elif not st.session_state.vectorstore:
    st.markdown("<div style='text-align:center; padding: 60px 20px; color: #999;'><div style='font-size: 4rem;'>📄</div><div style='font-size: 1.1rem; margin-top: 10px;'>Upload PDF di sidebar untuk mulai</div></div>", unsafe_allow_html=True)