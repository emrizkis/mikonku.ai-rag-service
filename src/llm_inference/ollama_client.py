from langchain_community.chat_models import ChatOllama
from typing import Any
from src.core.interfaces import ILLM
from src.core.config import Config

class OllamaClient(ILLM):
    """
    Concrete implementation of ILLM.
    Connects to the Ollama service running locally/in Podman.
    """
    
    def __init__(self, model_name: str = Config.OLLAMA_MODEL_NAME, host: str = Config.OLLAMA_HOST):
        # We instantiate LangChain's ChatOllama for better Instruction parsing and strict stopping.
        self.llm = ChatOllama(
            model=model_name, 
            base_url=host,
            temperature=0.1,
            num_predict=300 # Limit output to ~300 tokens to forcefully prevent endless loops.
        )
        
    def generate(self, prompt: str) -> str:
        """
        Sends the prompt to Ollama and returns the completion string.
        """
        return self.llm.invoke(prompt).content

    def stream(self, prompt: str) -> Any:
        """
        Streams the response natively from Ollama.
        """
        for chunk in self.llm.stream(prompt):
            yield chunk.content
