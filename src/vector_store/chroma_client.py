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
