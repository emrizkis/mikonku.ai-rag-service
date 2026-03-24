from src.core.config import Config
import chromadb
import sys

def main():
    print("="*60)
    print("⚠️  [PERINGATAN KERAS] TOMBOL NUKLIR DATABASE  ⚠️")
    print("="*60)
    print("Anda akan **MENGHAPUS TOTAL** seluruh memori AI Vektor")
    print("Dari semua User dan semua Group Workspace tanpa kecuali!")
    print(f"Target Server : {Config.CHROMA_HOST}:{Config.CHROMA_PORT}")
    print(f"Nama Koleksi  : '{Config.CHROMA_COLLECTION_NAME}'")
    print("-" * 60)
    
    confirm = input("Ketik 'KIAMAT' dengan huruf besar jika Anda yakin: ")
    if confirm != 'KIAMAT':
        print("Operasi dibatalkan. Mengamankan data kembali. Fiuh...")
        sys.exit(0)

    print(f"\n🔄 Menghubungi ChromaDB di {Config.CHROMA_HOST}:{Config.CHROMA_PORT}...")
    client = chromadb.HttpClient(
        host=Config.CHROMA_HOST,
        port=Config.CHROMA_PORT,
    )
    
    collection_name = Config.CHROMA_COLLECTION_NAME
    try:
        # Pengeksekusian hard wipe seluruh koleksi tanpa pandang bulu
        client.delete_collection(name=collection_name)
        print(f"✅ LEDAKAN SELESAI: Koleksi '{collection_name}' berhasil dilenyapkan.")
        print("Database vektor ChromaDB Anda hari ini resmi kembali sebersih kertas putih!")
    except Exception as e:
        print(f"⚠️ Operasi terhenti: Koleksi tampaknya sudah kosong atau server mati.")
        print(f"Bocoran Error Asli Chrome: {e}")

if __name__ == "__main__":
    main()
