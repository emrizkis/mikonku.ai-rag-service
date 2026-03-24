from typing import List, Any
from langchain_huggingface import HuggingFaceEmbeddings
from src.core.interfaces import IEmbedder
from src.core.config import Config

class HuggingFaceCPUEmbedder(IEmbedder):
    """
    Concrete implementation of IEmbedder.
    Uses HuggingFace embeddings running strictly on CPU to save GPU VRAM.
    """
    
    def __init__(self, model_name: str = Config.EMBEDDING_MODEL_NAME, device: str = Config.EMBEDDING_DEVICE):
        # Force the device to CPU or whatever is in Config
        self.embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={'device': device}
        )
        
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embeds a list of texts into vector representations.
        """
        return self.embeddings.embed_documents(texts)
        
    def get_embedding_model(self) -> Any:
        """
        Returns the underlying HuggingFace embeddings model object.
        """
        return self.embeddings
