from abc import ABC, abstractmethod
from langchain_core.documents.base import Document


class DocumentProcessor(ABC):
    """
    Abstract base class for document processing.
    """
    file_path: str
    
    def __init__(self, document_path: str) -> None:
        pass
   

    @abstractmethod
    def load_document(self) -> list[Document]:
        """
        Load a document from the specified file path.
        """
        pass

    
