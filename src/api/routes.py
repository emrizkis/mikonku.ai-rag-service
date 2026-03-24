import os
import shutil
from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

# Impor singleton dependencies dari penyedia terpusat
from src.api.dependencies import ingestion_pipeline, rag_pipeline, vector_store

# Inisialisasi Kumpulan Rute (Router)
router = APIRouter(prefix="/api", tags=["RAG Endpoints"])

# Skema JSON Validasi 
class ChatRequest(BaseModel):
    question: str
    user_id: str  # Wajib disertakan dari Frontend (Misal UUID Budi)
    group_id: str = None  # Opsional: Jika user punya banyak folder/grup proyek

@router.post("/ingest")
async def api_ingest_document(
    file: UploadFile = File(...),
    user_id: str = Form(..., description="KTP Rekaman UUID Pemilik Dokumen Tunggal"),
    doc_id: str = Form(..., description="UUID Unik dari Database SQL Anda untuk Dokumen Web Ini"),
    group_id: str = Form(None, description="Opsional: KTP Folder/Grup Proyek")
):
    """Mengunggah file PDF dan memasukannya ke memory ChromaDB."""
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Hanya menerima file berformat .pdf")
    
    # Amankan file unggahan sementara ke OS Lokal
    temp_path = f"tmp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        # Kirim file temp rute Ingestion solid standar beserta Stempel KTP Ekstra & KTP Dokumen Utama
        ingestion_pipeline.run(temp_path, user_id=user_id, group_id=group_id, doc_id=doc_id)
        return {"status": "success", "message": f"Dokumen '{file.filename}' (ID SQL: {doc_id}) berhasil diselundupkan dan Disegel Eksklusif!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Bersihkan file sampah (House-keeping)
        if os.path.exists(temp_path):
            os.remove(temp_path)

@router.post("/chat")
async def api_chat(request: ChatRequest):
    """Bertanya ke RAG Pipeline dan merespons via HTTP Streaming seperti ChatGPT."""
    try:
        # Modul `StreamingResponse` akan mengambil generator Python dan menyalurkannya *Bytes-By-Bytes* ke Frontend HTTP!
        # parameter user_id dan group_id dilempar masuk ke dasar Pipeline
        answer_stream = rag_pipeline.ask(request.question, user_id=request.user_id, group_id=request.group_id)
        return StreamingResponse(answer_stream, media_type="text/event-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/document/{doc_id}")
async def api_delete_document(doc_id: str, user_id: str):
    """Menghapus secara fisik jejak rekam vektor PDF dari ingatan memori ChromaDB."""
    try:
        success = vector_store.delete_document(doc_id=doc_id, user_id=user_id)
        return {"status": "success", "message": f"Seluruh jejak vektor dokumen {doc_id} telah dihapus/dibakar dari memori AI selamanya!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/group/{group_id}")
async def api_delete_group(group_id: str, user_id: str):
    """Menghapus massal seluruh dokumen dalam sebuah Workspace Grup."""
    try:
        # Pengecekan otomatis di ChromaClient sudah memastikan User tidak bisa menghapus grup milik orang lain.
        success = vector_store.delete_group(group_id=group_id, user_id=user_id)
        return {"status": "success", "message": f"Ledakan Massal! Seluruh dokumen di dalam Grup '{group_id}' milik Anda telah musnah dari memori AI!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/user/{user_id}")
async def api_delete_user(user_id: str):
    """Menghapus secara total seluruh eksistensi data milik suatu User dari memori AI."""
    try:
        success = vector_store.delete_user(user_id=user_id)
        return {"status": "success", "message": f"Kiamat Data! Seluruh eksistensi dokumen milik User '{user_id}' telah dibumihanguskan terbakar habis dari memori AI!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
