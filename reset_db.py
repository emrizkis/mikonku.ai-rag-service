from src.core.config import Config
import chromadb

def main():
    print(f"🔄 Menghubungi ChromaDB di {Config.CHROMA_HOST}:{Config.CHROMA_PORT}...")
    client = chromadb.HttpClient(
        host=Config.CHROMA_HOST,
        port=Config.CHROMA_PORT,
    )
    
    collection_name = Config.CHROMA_COLLECTION_NAME
    try:
        # Menghapus koleksi beserta seluruh vektor di dalamnya
        client.delete_collection(name=collection_name)
        print(f"✅ Koleksi memori '{collection_name}' berhasil dihapus.")
        print("Database vektor ChromaDB Anda kini sudah bersih dan kosong!")
    except Exception as e:
        print(f"⚠️ Operasi dihentikan: Koleksi mungkin sudah kosong atau tidak ditemukan. Detail: {e}")

if __name__ == "__main__":
    main()
