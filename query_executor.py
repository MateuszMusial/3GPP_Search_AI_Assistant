import logging

from rag_pipeline import start_rag_pipeline
from model_service import create_llm_model
from document_processors.document_processor import DocumentProcessor

logger = logging.getLogger(__name__)

class QueryExecutor:
    def __init__(self, file_processor: DocumentProcessor):
        self.file_processor = file_processor
        self.vectorstore = start_rag_pipeline(file_processor=self.file_processor)
        self.model = create_llm_model()

    def execute_query(self, query: str) -> str:
        """
        Execute a query using the LLM model.
        """
        response = self.model.invoke(query)
        return response