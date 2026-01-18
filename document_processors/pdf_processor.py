import logging
from pathlib import Path

from langchain_community.document_loaders import PyMuPDFLoader
from document_processors.document_processor import DocumentProcessor


logger = logging.getLogger(__name__)


class PDFProcessor(DocumentProcessor):
    """
    PDF document processor implementation.
    """
    def get_3gpp_document_path(self, data_dir: str = "data") -> str:
        """
        Get the path of the first PDF document in the specified directory.
        """
        base_path = Path(data_dir)

        if not base_path.exists():
            raise FileNotFoundError(f"Folder {data_dir} does not exist.")

        pdf_files = list(base_path.glob("*.pdf"))
        if not pdf_files:
            raise FileNotFoundError("No PDF files found in the specified directory.")
        
        return str(pdf_files[0])

    def load_document(self, file_path: str):
        """
        Load a PDF document using PyMuPDF.
        """
        try:
            loader = PyMuPDFLoader(file_path)
            document = loader.load()
            logger.info(f"Document loaded successfully from {file_path}.")
            return document
        except Exception as e:
            logger.error(f"Failed to load document from {file_path}: {e}")
            return None
