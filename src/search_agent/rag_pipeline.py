from pathlib import Path
import logging

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.documents.base import Document
from langchain_core.embeddings import Embeddings

from .document_processors.document_processor import DocumentProcessor


logger = logging.getLogger(__name__)

# Constants
FAISS_INDEX_PATH = "faiss_index"

class RAGPipeline:
    """
    Class to orchestrate the Retrieval-Augmented Generation (RAG) pipeline.
    """
    def __init__(self, file_processor: DocumentProcessor, embedding_service: Embeddings):
        self.file_processor = file_processor
        self.embedding_service = embedding_service
        self.vectorstore = None


    def split_text(self, docs: list[Document], chunk_size: int = 1000, chunk_overlap: int = 200) -> list[Document]:
        """
        Split text into chunks of specified size with overlap.
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        chunks = text_splitter.split_documents(docs)
        return chunks


    def embed_texts(self, chunks: list[Document], embedding_service: Embeddings) -> FAISS:
        """
        Embed a list of texts using the specified embedding model.
        """ 
        logger.info("Creating vectorstore from documents...")
        embeddings = embedding_service
        vectorstore = FAISS.from_documents(chunks, embeddings)
        vectorstore.save_local(FAISS_INDEX_PATH)
        logger.info(f"Vectorstore created and saved locally as '{FAISS_INDEX_PATH}'.")
        
        return vectorstore


    def start_rag_pipeline(self) -> FAISS | None:
        """
        Orchestrate the document processing and embedding pipeline.
        """
        logger.info("Starting RAG pipeline...")
        faiss_index_path = Path(FAISS_INDEX_PATH) / "index.faiss"
        
        if faiss_index_path.exists():
            logger.info("FAISS index already exists. Loading existing vectorstore.")
            return self.load_vectorstore()

        try:
            pdf_path = self.file_processor.get_3gpp_document_path()
        except FileNotFoundError:
            logger.error("Pipeline aborted: 3GPP document not found.")
            return None

        try:
            document = self.file_processor.load_document(pdf_path)
        except FileNotFoundError:
            logger.error("Pipeline aborted: Failed to load document.")
            return None

        chunks = self.split_text(document)
        if not chunks:
            logger.error("Pipeline aborted: No text chunks created from document.")
            return None

        vectorstore = self.embed_texts(chunks, embedding_service=self.embedding_service)
        logger.info("Document processing and embedding pipeline completed.")

        return vectorstore

    def load_vectorstore(self) -> FAISS | None:
        """
        Load the FAISS vectorstore from local storage.
        """
        faiss_index_path = Path(FAISS_INDEX_PATH) / "index.faiss"
        
        if not faiss_index_path.exists():
            logger.warning("FAISS index does not exist locally.")
            return None

        vectorstore = FAISS.load_local(
            FAISS_INDEX_PATH,
            embeddings=self.embedding_service,
            allow_dangerous_deserialization=True
        )
        logger.info("FAISS vectorstore loaded successfully.")
        return vectorstore
