import os
import logging

from langchain_google_genai import GoogleGenerativeAI


logger = logging.getLogger(__name__)

# Constants
MODEL_NAME = "gemini-3-pro-preview"


def create_llm_model(temperature: float = 0.1) -> GoogleGenerativeAI:
    """
    Create and return a Google Generative AI model instance.
    """
    model = GoogleGenerativeAI(
        model=MODEL_NAME,
        temperature=temperature,
        api_key=_get_api_key()
    )
    logger.info("AI model created successfully.")
    return model


def _get_api_key() -> str:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables.")
    return api_key
