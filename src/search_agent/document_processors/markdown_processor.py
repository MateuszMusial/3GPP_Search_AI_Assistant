import logging
from pathlib import Path

from langchain_core.documents.base import Document

from .document_processor import DocumentProcessor


logger = logging.getLogger(__name__)

class MarkdownProcessor(DocumentProcessor):
    """
    Markdown document processor.
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
        Load a Markdown document by reading its content.
        """
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                content = f.read()
            logger.info(f"Document loaded successfully from {self.file_path}.")
            return [Document(page_content=content, metadata={"source": self.file_path})]
        except Exception as e:
            logger.error(f"Failed to load document from {self.file_path}: {e}")
            raise FileNotFoundError(f"Failed to load document from {self.file_path}: {e}")