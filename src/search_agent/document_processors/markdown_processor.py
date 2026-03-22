import logging
from pathlib import Path

from .document_processor import DocumentProcessor


logger = logging.getLogger(__name__)

class MarkdownProcessor(DocumentProcessor):
    """
    Markdown document processor implementation.
    """
    def get_3gpp_document_path(self, data_dir: str = "data") -> str:
        """
        Get the path of the first Markdown document in the specified directory.
        """
        base_path = Path(data_dir)

        if not base_path.exists():
            raise FileNotFoundError(f"Folder {data_dir} does not exist.")

        md_files = list(base_path.glob("*.md"))
        if not md_files:
            raise FileNotFoundError("No Markdown files found in the specified directory.")
        
        return str(md_files[0])

    def load_document(self, file_path: str):
        """
        Load a Markdown document by reading its content.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            logger.info(f"Document loaded successfully from {file_path}.")
            return content
        except Exception as e:
            logger.error(f"Failed to load document from {file_path}: {e}")
            return None