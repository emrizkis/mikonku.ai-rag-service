from typing import List, Any
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.core.interfaces import ITextSplitter

class SimpleTextSplitter(ITextSplitter):
    """
    Concrete implementation of ITextSplitter using RecursiveCharacterTextSplitter from LangChain.
    """
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        
    def split_documents(self, documents: List[Any]) -> List[Any]:
        """
        Splits lists of documents into chunks.
        """
        chunks = self.splitter.split_documents(documents)
        return chunks
