import os
from typing import List, Any
from langchain_community.document_loaders import PyPDFLoader
from src.core.interfaces import IDocumentLoader

class BasePDFLoader(IDocumentLoader):
    """
    Concrete implementation of IDocumentLoader using PyPDFLoader from LangChain.
    """
    
    def load(self, file_path: str) -> List[Any]:
        """
        Loads the PDF and extracts its text contents.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File tidak ditemukan: {file_path}")
            
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        return documents
