import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

try:
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:
    from langchain_community.embeddings import HuggingFaceEmbeddings

PROMPT_TEMPLATE = """Kamu adalah asisten AI yang membantu menjawab pertanyaan berdasarkan dokumen yang diberikan.
Jawab pertanyaan HANYA berdasarkan konteks di bawah ini. Jika informasi tidak ada dalam konteks, katakan "Informasi tersebut tidak ditemukan dalam dokumen."
Jawab dalam Bahasa Indonesia yang jelas dan mudah dipahami.

Konteks:
{context}

Pertanyaan: {question}

Jawaban:"""

QA_PROMPT = PromptTemplate(template=PROMPT_TEMPLATE, input_variables=["context", "question"])


def build_vectorstore(pdf_path: str):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    if not documents:
        raise ValueError("PDF tidak bisa dibaca atau kosong.")

    documents = [doc for doc in documents if doc.page_content.strip()]

    if not documents:
        raise ValueError("PDF sepertinya hasil scan. Coba PDF yang teksnya bisa di-copy.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )

    os.makedirs("vectorstore", exist_ok=True)
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local("vectorstore/faiss_index")
    return vectorstore


def get_answer(question: str, vectorstore, api_key: str) -> dict:
    llm = ChatGroq(
        groq_api_key=api_key,
        model_name="llama-3.3-70b-versatile",
        temperature=0.1,
        max_tokens=1024
    )

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    relevant_docs = retriever.invoke(question)
    context = "\n\n".join([doc.page_content for doc in relevant_docs])

    chain = QA_PROMPT | llm | StrOutputParser()
    answer = chain.invoke({"context": context, "question": question})

    sources = []
    for doc in relevant_docs:
        text = doc.page_content.strip()[:200]
        if text and text not in sources:
            sources.append(text)

    return {"answer": answer, "sources": sources[:3]}