import logging


from .models.model_service import ModelService
from .document_processors.document_processor import DocumentProcessor
from .rag_pipeline import RAGPipeline
from .prompts import get_prompt_template

logger = logging.getLogger(__name__)

class QueryExecutor:
    def __init__(self, file_processor: DocumentProcessor, llm_model: ModelService, pipeline: RAGPipeline):
        self.file_processor = file_processor
        self.vectorstore = pipeline.start_rag_pipeline()
        self.model = llm_model.create_llm_model()

    def execute_query(self, query: str) -> str:
        """
        Execute a query using the LLM model.
        """
        if not self.vectorstore:
            logger.error("Vectorstore not initialized.")                 
            return "Error: Vectorstore could not be loaded."

        logger.info(f"Searching for context related to: {query}")
        docs = self.vectorstore.similarity_search(query, k=4)

        if not docs:
             logger.warning(f"No documents found for query: {query}")
             return "No relevant information found in the documents."

        context = "\n\n".join([doc.page_content for doc in docs])
        
        prompt_template = get_prompt_template()
        chain = prompt_template | self.model

        logger.info("Invoking model...")
        response = chain.invoke({"context": context, "target_ie": query})
        return response
