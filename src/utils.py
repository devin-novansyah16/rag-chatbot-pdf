"""
src/utils.py
Helper functions untuk file handling
"""
import os
import shutil

UPLOAD_DIR = "uploads"
VECTORSTORE_DIR = "vectorstore"


def save_uploaded_file(uploaded_file) -> str:
    """Simpan file yang diupload ke folder uploads/, return path."""
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path


def clear_vectorstore():
    """Hapus vectorstore dan file upload yang tersimpan."""
    if os.path.exists(VECTORSTORE_DIR):
        shutil.rmtree(VECTORSTORE_DIR)
    if os.path.exists(UPLOAD_DIR):
        shutil.rmtree(UPLOAD_DIR)


def get_file_size_mb(file_path: str) -> float:
    """Return ukuran file dalam MB."""
    return os.path.getsize(file_path) / (1024 * 1024)
