import argparse
from src.core.config import Config
from src.data_ingestion.pdf_loader import BasePDFLoader
from src.data_ingestion.text_splitter import SimpleTextSplitter
from src.embeddings.hf_embedder import HuggingFaceCPUEmbedder
from src.vector_store.chroma_client import ChromaVectorStore
from src.pipelines.ingestion_pipeline import IngestionPipeline

def main():
    parser = argparse.ArgumentParser(description="AI Data Ingestion Pipeline (SOLID)")
    parser.add_argument("--file", type=str, required=True, help="Path ke file PDF")
    args = parser.parse_args()

    # Dependency Injection Container Process
    # We instantiate the concrete classes here.
    loader = BasePDFLoader()
    splitter = SimpleTextSplitter(chunk_size=Config.CHUNK_SIZE, chunk_overlap=Config.CHUNK_OVERLAP)
    embedder = HuggingFaceCPUEmbedder()
    vector_store = ChromaVectorStore()

    # Pass the dependencies to the pipeline
    pipeline = IngestionPipeline(
        loader=loader,
        splitter=splitter,
        embedder=embedder,
        vector_store=vector_store
    )
    
    # Run the use-case
    pipeline.run(args.file)

if __name__ == "__main__":
    main()
