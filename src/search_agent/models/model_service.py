from abc import ABC, abstractmethod


class ModelService(ABC):
    """
    Abstract base class for model services. This class defines the interface for creating language models and retrieving API keys.
    """
    @abstractmethod
    def create_llm_model(self, temperature: float = 0.1):
        pass

    @abstractmethod
    def create_embedding_model(self):
        pass

    @abstractmethod
    def _get_api_key(self) -> str:
        pass
