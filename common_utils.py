from pathlib import Path
import logging

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)


def get_3gpp_document_path(data_dir: str = "data") -> str | None:
    """
    Get the path of the first PDF document in the specified directory.
    """
    base_path = Path(data_dir)

    if not base_path.exists():
        logger.error(f"Folder {data_dir} not exist.")
        return None

    pdf_files = list(base_path.glob("*.pdf"))
    if not pdf_files:
        logger.error("No PDF files found in the specified directory.")
        return None
    
    return str(pdf_files[0])


def load_pdf_document(file_path: Path) -> str | None:
    """
    Load the content of a PDF document.
    """
    try:
        loader = PyPDFLoader(file_path)
        data = loader.load()
        return data
    except Exception as e:
        logger.error(f"Failed to load PDF document: {e}")
        return None
    

def split_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> list[str]:
    """
    Split text into chunks of specified size with overlap.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = text_splitter.split_text(text)
    return chunks