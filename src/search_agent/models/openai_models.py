import os
import logging

from langchain_openai import OpenAI, OpenAIEmbeddings

from .model_service import ModelService


EMBEDDING_MODEL_NAME = "gpt-5-embedding-001"

logger = logging.getLogger(__name__)


class OpenAIModelService(ModelService):
    """
    Service class for creating OpenAI models and retrieving API keys.
    """
    def __init__(self, model_name: str = "gpt-5-nano"):
        self.model_name = model_name
        logger.info("Initializing OpenAIModelService...")

    def create_llm_model(self, temperature: float = 0.1) -> OpenAI:
        """
        Create and return an OpenAI model instance.
        """
        model = OpenAI(
            model=self.model_name,
            temperature=temperature,
            api_key=self._get_api_key() # type: ignore[arg-type]
        )
        logger.info("AI model created successfully.")
        return model

    def create_embedding_model(self) -> OpenAIEmbeddings:
        """
        Create and return an OpenAI embedding model instance.
        """
        embedding_model = OpenAIEmbeddings(
            model=EMBEDDING_MODEL_NAME,
            api_key=self._get_api_key() # type: ignore[arg-type]
        )
        logger.info("Embedding model created successfully.")
        return embedding_model

    def _get_api_key(self) -> str:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables.")
        return api_key
