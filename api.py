import os
import shutil
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

# Pipeline Imports Moduler
from src.embeddings.hf_embedder import HuggingFaceCPUEmbedder
from src.vector_store.chroma_client import ChromaVectorStore
from src.llm_inference.ollama_client import OllamaClient
from src.pipelines.ingestion_pipeline import IngestionPipeline
from src.pipelines.rag_pipeline import RAGPipeline
from src.data_ingestion.pdf_loader import BasePDFLoader
from src.data_ingestion.text_splitter import SimpleTextSplitter

app = FastAPI(
    title="Mikonku.ai REST API", 
    description="RAG Backend terotomatisasi penuh berbasis Clean Architecture.",
    version="1.0.0"
)

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

# Skema JSON Validasi 
class ChatRequest(BaseModel):
    question: str
    user_id: str  # Wajib disertakan dari Frontend (Misal UUID Budi)

@app.post("/api/ingest")
async def api_ingest_document(
    file: UploadFile = File(...),
    user_id: str = Form(..., description="KTP Rekaman UUID Pemilik Dokumen Tunggal")
):
    """Mengunggah file PDF dan memasukannya ke memory ChromaDB."""
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Hanya menerima file berformat .pdf")
    
    # Amankan file unggahan sementara ke OS Lokal
    temp_path = f"tmp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        # Kirim file temp rute Ingestion solid standar beserta Stempel KTP-nya
        ingestion_pipeline.run(temp_path, user_id=user_id)
        return {"status": "success", "message": f"Dokumen '{file.filename}' berhasil diselundupkan dan Disegel Eksklusif untuk Pemilik: {user_id}!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Bersihkan file sampah (House-keeping)
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.post("/api/chat")
async def api_chat(request: ChatRequest):
    """Bertanya ke RAG Pipeline dan merespons via HTTP Streaming seperti ChatGPT."""
    try:
        # Modul `StreamingResponse` akan mengambil generator Python dan menyalurkannya *Bytes-By-Bytes* ke Frontend HTTP!
        # [NEW] parameter user_id dilempar masuk ke dasar Pipeline
        answer_stream = rag_pipeline.ask(request.question, user_id=request.user_id)
        return StreamingResponse(answer_stream, media_type="text/event-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Mengeksekusi ASGI Uvicorn Engine (Disarankan tanpa container untuk tes lokal)
    uvicorn.run("api:app", host="0.0.0.0", port=8080, reload=True)
