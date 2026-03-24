import argparse
from src.embeddings.hf_embedder import HuggingFaceCPUEmbedder
from src.vector_store.chroma_client import ChromaVectorStore
from src.llm_inference.ollama_client import OllamaClient
from src.pipelines.rag_pipeline import RAGPipeline

def main():
    parser = argparse.ArgumentParser(description="AI RAG Chatbot CLI (Fase 3)")
    parser.add_argument("--ask", type=str, required=True, help="Ketikan pertanyaan Anda dari dokumen PDF-nya")
    args = parser.parse_args()

    # 1. Instantiate Concrete Classes (Dependency Injection Container)
    embedder = HuggingFaceCPUEmbedder()
    vector_store = ChromaVectorStore()
    llm = OllamaClient()

    # 2. Inject interfaces into RAG Pipeline
    rag = RAGPipeline(
        vector_store=vector_store,
        embedder=embedder,
        llm=llm
    )
    
    # 3. Request logic Execution!
    answer_stream = rag.ask(args.ask)
    
    # 4. Print Streaming Output Beautifully
    print("\n" + "="*70)
    print(f"💡 \033[1mJawaban Terbaca Langsung (Streaming):\033[0m\n")
    
    for chunk in answer_stream:
        # Mencetak tiap kata secara live begitu dipikirkan oleh GPU
        print(chunk, end="", flush=True)
        
    print("\n\n" + "="*70 + "\n")

if __name__ == "__main__":
    main()
