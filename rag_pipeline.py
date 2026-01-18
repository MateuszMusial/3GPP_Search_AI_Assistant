import os
from pathlib import Path
import logging

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, GoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_core.documents.base import Document
from document_processors.document_processor import DocumentProcessor


logger = logging.getLogger(__name__)

# Constants
MODEL_NAME = "gemini-2.5-pro"
EMBEDDING_MODEL_NAME = "models/embedding-001"
FAISS_INDEX_PATH = "faiss_index"


def create_model(temperature: float = 0.1) -> GoogleGenerativeAI:
    """
    Create and return a Google Generative AI model instance.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        logger.warning("GOOGLE_API_KEY not found in environment variables.")
        
    model = GoogleGenerativeAI(
        model=MODEL_NAME,
        temperature=temperature,
        api_key=api_key
    )
    logger.info("AI model created successfully.")
    return model


def split_text(docs: list[Document], chunk_size: int = 1000, chunk_overlap: int = 200) -> list[Document]:
    """
    Split text into chunks of specified size with overlap.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = text_splitter.split_documents(docs)
    return chunks


def embed_texts(chunks: list[Document], model_name: str) -> FAISS:
    """
    Embed a list of texts using the specified embedding model.
    """ 
    logger.info("Creating vectorstore from documents...")
    embeddings = GoogleGenerativeAIEmbeddings(model=model_name)
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(FAISS_INDEX_PATH)
    logger.info(f"Vectorstore created and saved locally as '{FAISS_INDEX_PATH}'.")
    
    return vectorstore


def start_rag_pipeline(file_processor: DocumentProcessor) -> FAISS | None:
    """
    Orchestrate the document processing and embedding pipeline.
    """
    logger.info("Starting RAG pipeline...")
    faiss_index_path = Path(FAISS_INDEX_PATH) / "index.faiss"
    
    if faiss_index_path.exists():
        logger.info("FAISS index already exists. Loading existing index.")
        vectorstore = FAISS.load_local(
            FAISS_INDEX_PATH, 
            GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL_NAME),
            allow_dangerous_deserialization=True
        )
        return vectorstore
        
    pdf_path = file_processor.get_3gpp_document_path()
    if not pdf_path:
        logger.error("Pipeline aborted: No document found.")
        return None

    document = file_processor.load_document(pdf_path)
    if not document:
        logger.error("Pipeline aborted: Failed to load document.")
        return None

    chunks = split_text(document)
    vectorstore = embed_texts(chunks, model_name=EMBEDDING_MODEL_NAME)

    logger.info("Document processing and embedding pipeline completed.")
    return vectorstore
