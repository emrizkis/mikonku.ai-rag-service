import os
from src.core.interfaces import IDocumentLoader, ITextSplitter, IEmbedder, IVectorStore

class IngestionPipeline:
    """
    Orchestrator class that glues all SOLID components together.
    It expects abstract interfaces, so it is fully decoupled from actual implementations.
    """
    
    def __init__(
        self,
        loader: IDocumentLoader,
        splitter: ITextSplitter,
        embedder: IEmbedder,
        vector_store: IVectorStore
    ):
        self.loader = loader
        self.splitter = splitter
        self.embedder = embedder
        self.vector_store = vector_store

    def run(self, file_path: str, user_id: str = None, group_id: str = None, doc_id: str = None):
        """
        Executes the extraction, chunking, and embedding/loading pipeline.
        """
        print(f"[1/4] Memuat dokumen PDF dari {file_path}...")
        documents = self.loader.load(file_path)
        print(f"      -> {len(documents)} halaman dimuat.")
        
        print(f"\n[2/4] Memecah (chunking) dokumen...")
        chunks = self.splitter.split_documents(documents)
        print(f"      -> Dipecah menjadi {len(chunks)} chunks.")
        
        # [NEW] Multi-Tenancy Identity Injection
        if user_id:
            print(f"      -> 🔐 Menyegel seluruh {len(chunks)} vektor HANYA untuk pemilik UUID: '{user_id}' (Grup: '{group_id}')")
            for chunk in chunks:
                if not getattr(chunk, 'metadata', None):
                    chunk.metadata = {}
                chunk.metadata["user_id"] = user_id
                
                # Jika grup proyek juga diisi, stempel ganda!
                if group_id:
                    chunk.metadata["group_id"] = group_id
                
                # [NEW] Segel Dokumen Tunggal (Untuk Fitur Delete File CRUD)
                if doc_id:
                    chunk.metadata["doc_id"] = doc_id
        
        print(f"\n[3/4 & 4/4] Membangun embeddings CPU dan menyimpan ke ChromaDB Store...")
        self.vector_store.add_documents(chunks, self.embedder)
        
        print(f"\n✅ Pipeline ingestion selesai dengan sukses. Data vektor aman tersimpan!")
