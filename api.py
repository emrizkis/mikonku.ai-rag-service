from fastapi import FastAPI

# Mengimpor modul Router Eksternal (Clean Architecture)
from src.api.routes import router

app = FastAPI(
    title="Mikonku.ai REST API", 
    description="RAG Backend terotomatisasi penuh berbasis Clean Architecture.",
    version="1.0.0"
)

# Mencangkokkan cabang rute yang sudah murni terpisah
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    # Mengeksekusi ASGI Uvicorn Engine Lokal
    uvicorn.run("api:app", host="0.0.0.0", port=8080, reload=True)
