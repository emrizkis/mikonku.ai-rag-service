from abc import ABC, abstractmethod
from typing import List, Any

class IDocumentLoader(ABC):
    """Abstract interface for loading documents from a source."""
    
    @abstractmethod
    def load(self, file_path: str) -> List[Any]:
        """
        Loads a document and returns a list of its elements/documents.
        A 'Document' here usually contains 'page_content' and 'metadata'.
        """
        pass

class ITextSplitter(ABC):
    """Abstract interface for text splitting strategies."""
    
    @abstractmethod
    def split_documents(self, documents: List[Any]) -> List[Any]:
        """
        Splits a list of documents into sub-documents (chunks).
        """
        pass

class IEmbedder(ABC):
    """Abstract interface for text embedding."""
    
    @abstractmethod
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embeds a list of texts into vector representations.
        """
        pass
    
    @abstractmethod
    def get_embedding_model(self) -> Any:
        """
        Returns the underlying provider embedding model object (e.g., HuggingFaceEmbeddings).
        This is useful for passing the model directly to vector stores like ChromaDB
        which might require the raw object.
        """
        pass

class IVectorStore(ABC):
    """Abstract interface for vector database operations."""
    
    @abstractmethod
    def add_documents(self, documents: List[Any], embedder: IEmbedder) -> None:
        """
        Embeds and loads documents into the vector store.
        """
        pass
        
    @abstractmethod
    def similarity_search(self, query: str, k: int = 3, embedder: IEmbedder = None, filter_dict: dict = None) -> List[Any]:
        """
        Searches the vector store for the top k most similar documents to the query,
        optionally constrained by a metadata filter parameter.
        """
        pass
        
    @abstractmethod
    def delete_document(self, doc_id: str, user_id: str = None) -> bool:
        """
        Hard deletes all vector chunks associated with a precise doc_id tag.
        """
        pass
        
    @abstractmethod
    def delete_group(self, group_id: str, user_id: str) -> bool:
        """
        Hard deletes all vector chunks associated with a specific workspace group tag.
        """
        pass
        
    @abstractmethod
    def delete_user(self, user_id: str) -> bool:
        """
        Hard deletes all vector chunks entirely associated with a specific user account.
        """
        pass

class ILLM(ABC):
    """Abstract interface for Large Language Models."""
    
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Takes a fully formatted prompt string and returns the model's text generation.
        """
        pass

    @abstractmethod
    def stream(self, prompt: str) -> Any:
        """
        Streams the model's text generation chunk by chunk.
        """
        pass
