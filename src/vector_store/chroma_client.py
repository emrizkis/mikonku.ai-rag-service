import chromadb
from typing import List, Any
from chromadb.config import Settings
from langchain_community.vectorstores import Chroma
from src.core.interfaces import IVectorStore, IEmbedder
from src.core.config import Config

class ChromaVectorStore(IVectorStore):
    """
    Concrete implementation of IVectorStore.
    Connects to an external ChromaDB server (like one running in a Podman container).
    """
    
    def __init__(self, collection_name: str = Config.CHROMA_COLLECTION_NAME):
        # We connect via HTTP to the Podman server
        self.client = chromadb.HttpClient(
            host=Config.CHROMA_HOST,
            port=Config.CHROMA_PORT,
            settings=Settings(allow_reset=True, anonymized_telemetry=False)
        )
        self.collection_name = collection_name
        self._langchain_chroma = None
        
    def add_documents(self, documents: List[Any], embedder: IEmbedder) -> None:
        """
        Adds newly loaded or split documents into ChromaDB.
        """
        embedding_function = embedder.get_embedding_model()
        
        # We use LangChain's wrapper around Chroma but pass the HttpClient so it connects to the Podman server
        self._langchain_chroma = Chroma(
            client=self.client,
            collection_name=self.collection_name,
            embedding_function=embedding_function
        )
        
        self._langchain_chroma.add_documents(documents)
        print(f"Berhasil menambahkan {len(documents)} vektor chunk ke koleksi '{self.collection_name}'.")

    def similarity_search(self, query: str, k: int = 3, embedder: IEmbedder = None, filter_dict: dict = None) -> List[Any]:
        """
        Searches the ChromaDB for relevant document chunks, with optional tenant filtering.
        """
        if not self._langchain_chroma:
            embedding_function = embedder.get_embedding_model() if embedder else None
            self._langchain_chroma = Chroma(
                client=self.client,
                collection_name=self.collection_name,
                embedding_function=embedding_function
            )
            
        return self._langchain_chroma.similarity_search(query, k=k, filter=filter_dict)

    def delete_document(self, doc_id: str, user_id: str = None) -> bool:
        """
        Hard deletes all chunks of a specific document from ChromaDB physically.
        """
        if not self._langchain_chroma:
            print("Penyimpanan kosong, tidak ada yang dihapus.")
            return False
            
        where_filter = {"doc_id": doc_id}
        if user_id:
            where_filter = {"$and": [{"doc_id": doc_id}, {"user_id": user_id}]}
            
        # Target langsung koleksi native di bawah kap engine LangChain
        self._langchain_chroma._collection.delete(where=where_filter)
        print(f"♻️ Berhasil membakar vektor secara fisik untuk dokumen: {doc_id}")
        return True

    def delete_group(self, group_id: str, user_id: str) -> bool:
        """
        Hard deletes all chunks of an entire workspace group from ChromaDB physically.
        """
        if not self._langchain_chroma:
            print("Penyimpanan kosong, tidak ada yang dihapus.")
            return False
            
        # Wajib menyertakan user_id sebagai pengaman Authorization lapis pertama
        where_filter = {"$and": [{"group_id": group_id}, {"user_id": user_id}]}
            
        self._langchain_chroma._collection.delete(where=where_filter)
        print(f"💣 Berhasil membumihanguskan massal seluruh vektor Grup Workspace: {group_id}")
        return True

    def delete_user(self, user_id: str) -> bool:
        """
        Hard deletes all chunks belonging to an entire user from ChromaDB physically.
        """
        if not self._langchain_chroma:
            print("Penyimpanan kosong, tidak ada yang dihapus.")
            return False
            
        where_filter = {"user_id": user_id}
            
        self._langchain_chroma._collection.delete(where=where_filter)
        print(f"☢️ Berhasil MENGHANGUSKAN KIAMAT seluruh rekam jejak vektor User: {user_id}")
        return True
