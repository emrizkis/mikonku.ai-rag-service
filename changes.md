# Mikonku.ai RAG Service - Evolutionary Changelog

Perjalanan evolusi arsitektur *"Mikonku.ai Local RAG Backend"* dari skrip mainan prototipe kasar (*script-kiddie*) hingga menjelma menjadi **SaaS Enterprise-Ready Microservices** dengan keamanan mutlak dan skalabilitas tanpa batas.

---

### Phase 1: Uji Konsep Ekstraktor (*Proof of Concept*)
- **Status:** Bereksperimen dengan model RAG (*Retrieval-Augmented Generation*).
- **Hasil:** Berhasil mengolah 1 file PDF lokal dan menyimpannya ke memori vektor ChromaDB melalui skrip vertikal/monolith yang masih berantakan (*Spaghetti Code*).

### Phase 2: Refactoring "The Clean Architecture" (Prinsip S.O.L.I.D)
- **Status:** Mendesain ulang total kerangka server sesuai *Best Practice Microservices*.
- **Hasil:**
  - Kode ditata rapi ke dalam pondasi struktur industri: `src/core/interfaces.py`, `src/data_ingestion/`, `src/embeddings/`, `src/vector_store/`.
  - Mengimplementasikan konsep antarmuka *Abstract Base Classes* untuk `IDocumentLoader`, `IEmbedder`, dan `IVectorStore`.
  - Menciptakan `IngestionPipeline` terpusat (*Dependency Inversion Layer*).

### Phase 3: Mesin Penjawab Obrolan (LLM Inference Engine)
- **Status:** Mengintegrasikan model *Language Model* (LLM) Lokal tanpa batasan kuota.
- **Hasil:**
  - Mengkoneksikan backend kita dengan server Podman **Ollama (Model Phi-3)** yang ringan namun sangat cepat.
  - Membangun `RAGPipeline` untuk meramu pertanyaan (Query) dengan potongan Vektor (Konteks) lalu melemparnya ke Ollama untuk diekstrak menjadi teks bahasa manusia sungguhan.

### Phase 4: Integrasi Web Server Eksekusi Terbuka (REST API Server)
- **Status:** Bertransisi dari basis aplikasi *Command Line Terminal (CLI)* menjadi antarmuka WEB terbuka untuk interaksi dengan bahasa pemrograman lain secara publik.
- **Hasil:** 
  - Mencangkok kerangka **FastAPI** yang super cepat berspesifikasi ASGI (Asynchronous Server Gateway).
  - Merancang *Endpoint* `POST /api/ingest` (menerima Upload File Multiform Type) dan `POST /api/chat` (menerima JSON string).
  - Berhasil mengerahkan arsitektur balasan instan per-kata (*HTTP Streaming Response*) ala ChatGPT.

### Phase 5: Privasi Ekstrem via Isolasi Multi-Tamu (Multi-Tenancy)
- **Status:** Mengubah *Single-User Application* menjadi sistem yang mampu menangani dan membatasi data ribuan pengguna bersamaan di dalam Server yang sama tanpa bocor sebaris pun.
- **Hasil:** 
  - Penambahan penyematan stempel Metadata UUID Ekstra (KTP Pemilik = `user_id`) kepada pecahan algoritma *Embedding*.
  - Menumbuhkan insting proteksi *ChromaDB* untuk mencari jawaban eksklusif hanya untuk dokumen tunggal dengan properti UUID dari *User* yang memanggilnya (*Metadata Overloading Constraint*).

### Phase 6: Pembedahan Memori Fisik Tingkat Granular (Document CRUD)
- **Status:** Membebaskan ruang database server dengan dukungan interaksi siklus operasi pengelolaan memori tingkat individu File Teks/Dokumen.
- **Hasil:**
  - Inskripsi stempel UUID sekunder tambahan level dokumen PDF: `doc_id`.
  - Mengerjakan fitur Hapus/Nuke langsung ke mesin penampung Vektor (*ChromaDB Memory Collection physical wipe*).
  - Melahirkan *Endpoint Sniper Target*: `DELETE /api/document/{doc_id}` .

### Phase 7: Arsitektur Memori Sesi Histori (Multi-Topik ChatGPT)
- **Status:** Mendesain cetak biru teori integrasi RAG menjadi obrolan interaktif jangka panjang. 
- **Hasil:** 
  - Merealisasikan arsitektur *Stateless History Injection* di mana RAG Engine menolak untuk menyimpan beban riwayat *Database SQL* eksternal dan melimpahkan sekuens ingatan secara murni (*Payload Inject*) dari antarmuka Web utama.

### Phase 8: Abstraksi Folder / Knowledge Bases (RAG Workspaces)
- **Status:** Mengizinkan 1 User untuk menguasai belasan entitas terpisah *Group Project/Folder/Workspace*. (Seperti fitur *Hub* ChatGPT).
- **Hasil:** 
  - RAG Backend mendukung integrasi Parameter Kunci Ketiga yang sangat langka: `group_id`.
  - Mengembangkan aljabar vektor Boolean Murni di dalam *pipeline inference* (`query: {"$and": [{"user_id": X}, {"group_id": Y}]}`).
  - Menciptakan fitur Ledakan Massal Satu Area Folder: `DELETE /api/group/{group_id}`.

### Phase 9: Penghancuran Mutlak Dunia User (The God Mode)
- **Status:** Menangani peristiwa penghancuran massal total jika seorang *User* membakar habis seluruh kepemilikan mereka (Hapus Akun).
- **Hasil:**
  - Logika native Vector Store dikustomisasi ulang untuk menerobos filter folder sub-direktori (Langsung membidik `user_id` tertinggi).
  - Membuahkan *Endpoint* pamungkas mematikan: `DELETE /api/user/{user_id}`.

### Phase 10: Rombak Massal Skalabilitas Lapisan API (Router Decoupling)
- **Status:** Memberantas seluruh kotoran di *entry point* utama dan menstranplantasikannya untuk merangkul arsitektur yang sanggup menanggung jutaan antrean permintaan *HTTP Routing*.
- **Hasil:** 
  - Mengekstrak metode *Spaghetti Endpoint* ke lapisan eksternal **FastAPI APIRouter** (`src/api/routes.py`).
  - Menyelundupkan instans *Model LLM dan Pipeline RAG Memory* ke dalam pusat injeksi independen (*Singleton Injection Array* di `dependencies.py`). 
  - Kode eksekutor peluncuran `api.py` menyusut bersih, ringkas, memukau, dan menakjubkan bagi seluruh pembaca baris demi baris pengamat sintaks. 

-- *Mikonku.ai Backend Team 2026* --
