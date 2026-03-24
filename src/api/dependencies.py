from src.embeddings.hf_embedder import HuggingFaceCPUEmbedder
from src.vector_store.chroma_client import ChromaVectorStore
from src.llm_inference.ollama_client import OllamaClient
from src.pipelines.ingestion_pipeline import IngestionPipeline
from src.pipelines.rag_pipeline import RAGPipeline
from src.data_ingestion.pdf_loader import BasePDFLoader
from src.data_ingestion.text_splitter import SimpleTextSplitter

# Inisialisasi Singleton Instance secara Global Memory
print("⏳ Menginisialisasi Singleton Modul Pembelajaran Vektor (Harap memori RAM memadai)...")
embedder = HuggingFaceCPUEmbedder()
vector_store = ChromaVectorStore()
llm = OllamaClient()

# Sambungkan komponen Solid Dependencies ke Pipeline
ingestion_pipeline = IngestionPipeline(
    loader=BasePDFLoader(),
    splitter=SimpleTextSplitter(),
    embedder=embedder,
    vector_store=vector_store
)

rag_pipeline = RAGPipeline(
    vector_store=vector_store,
    embedder=embedder,
    llm=llm
)
