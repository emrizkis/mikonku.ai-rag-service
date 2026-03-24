# 📚 FASE 2: AI DATA ENGINEERING & VECTOR MANAGEMENT
**Tujuan:** Membangun "Ingatan Jangka Panjang" (Vector Database) agar AI bisa menjawab berdasarkan dokumen perbankan lokal secara akurat (RAG).

---

## 🏗️ 1. INFRASTRUKTUR (ANTIGRAVITY / PODMAN)
Kita akan menjalankan **ChromaDB** sebagai server di dalam container. Ini berfungsi sebagai "gudang" penyimpanan vektor teks kamu.

### Run ChromaDB Server
Jalankan perintah ini di PowerShell untuk men-deploy database:

```powershell
podman run -d `
  --name chromadb-server `
  -p 8000:8000 `
  -v chroma_vault:/chroma/chroma `
  -e IS_PERSISTENT=TRUE `
  -e ANONYMIZED_TELEMETRY=False `
  chromadb/chroma
```

## 🐍 2. PYTHON ENVIRONMENT (.VENV)

Agar VRAM GTX 1650 (4GB) tetap lega untuk menjalankan LLM di Ollama, kita akan menjalankan proses Embedding menggunakan CPU di sisi host Windows.

Setup Environment
Buka folder project kamu di terminal.

Jalankan urutan perintah berikut: 

```command 
# Create venv
python -m venv .venv

# Activate venv
.\.venv\Scripts\Activate.ps1

# Install Dependencies
pip install langchain langchain-community langchain-huggingface chromadb pypdf
```

