import os
import logging

from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings

from .model_service import ModelService


EMBEDDING_MODEL_NAME = "gemini-embedding-001"

logger = logging.getLogger(__name__)


class GoogleModelService(ModelService):
    """
    Service class for creating Google Generative AI models and retrieving API keys.
    """
    def __init__(self, model_name: str = "gemini-3-pro-preview"):
        self.model_name = model_name
        logger.info("Initializing GoogleModelService...")

    def create_llm_model(self, temperature: float = 0.1) -> GoogleGenerativeAI:
        """
        Create and return a Google Generative AI model instance.
        """
        model = GoogleGenerativeAI(
            model=self.model_name,
            temperature=temperature,
            api_key=self._get_api_key()
        )
        logger.info("AI model created successfully.")
        return model

    def create_embedding_model(self):
        """
        Create and return a Google Generative AI embedding model instance.
        """
        embedding_model = GoogleGenerativeAIEmbeddings(
            model=EMBEDDING_MODEL_NAME,
            api_key=self._get_api_key()
        )
        logger.info("Embedding model created successfully.")
        return embedding_model

    def _get_api_key(self) -> str:
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables.")
        return api_key
