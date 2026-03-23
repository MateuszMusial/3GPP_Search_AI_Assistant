import logging
from pathlib import Path

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents.base import Document

from .document_processor import DocumentProcessor


logger = logging.getLogger(__name__)


class PDFProcessor(DocumentProcessor):
    """
    PDF document processor.
    """
    def __init__(self, document_path: str) -> None:
        if not document_path:
            raise FileNotFoundError("No file path provided.")

        path = Path(document_path)
        if not path.parent.exists():
            raise FileNotFoundError(f"Folder {path.parent} does not exist.")
        
        self.file_path = document_path


    def load_document(self) -> list[Document]:
        """
        Load a PDF document using PyMuPDF.
        """
        try:

            loader = PyMuPDFLoader(f"data/{self.file_path}")
            document = loader.load()
            logger.info(f"Document loaded successfully from {self.file_path}.")
            return document
        except Exception as e:
            logger.error(f"Failed to load document from {self.file_path}: {e}")
            raise FileNotFoundError(f"Failed to load document from {self.file_path}: {e}")
