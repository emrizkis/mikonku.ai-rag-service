from typing import Any
from src.core.interfaces import IVectorStore, IEmbedder, ILLM
from langchain_core.prompts import PromptTemplate

class RAGPipeline:
    """
    Business Logic class for Retrieval-Augmented Generation.
    It takes a question, searches the Vector Store for context, and sends it to the LLM.
    """
    def __init__(self, vector_store: IVectorStore, embedder: IEmbedder, llm: ILLM):
        self.vector_store = vector_store
        self.embedder = embedder
        self.llm = llm

    def ask(self, question: str, user_id: str = None) -> Any:
        # 1. Retrieval: Cari data terdekat dari ChromaDB
        print(f"📖 Sedang menelototi dokumen untuk mencari info terkait '{question}'...")
        
        # [NEW] Multi-Tenancy Search Constraint
        filter_args = {"user_id": user_id} if user_id else None
        
        if filter_args:
            print(f"👁️‍🗨️ Menerapkan Mode Keamanan: Hanya mencari Dokumen Pribadi milik UUID: '{user_id}'...")
            
        docs = self.vector_store.similarity_search(
            question, 
            k=3, 
            embedder=self.embedder,
            filter_dict=filter_args
        )
        
        # Ekstrak konten teksnya ke dalam satu kesatuan String besar
        context_text = "\n\n---\n\n".join([doc.page_content for doc in docs])
        
        # 2. Augmentation: Bangun Template Prompt
        # Prompt ini sengaja didesain untuk berbahasa Indonesia agar Phi-3 menjawab konsisten
        prompt_template = PromptTemplate.from_template(
            "Tugas Anda adalah sebagai Asisten AI penjawab singkat.\n\n"
            "--- KONTEKS DOKUMEN ---\n{context}\n----------------------\n\n"
            "Berdasarkan konteks dokumen di atas, tolong jawab pertanyaan ini dengan singkat, sangat ringkas dan 'to the point'.\n"
            "Pertanyaan: {question}\n\n"
            "Jawaban Anda:"
        )
        
        prompt_formatted = prompt_template.format(context=context_text, question=question)
        
        # 3. Generation: Proses Teks Memakai Ollama
        print(f"🤖 Menghubungi Model LLM phi3 untuk Memulai Streaming Teks...\n")
        return self.llm.stream(prompt_formatted)
