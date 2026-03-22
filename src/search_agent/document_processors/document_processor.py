from abc import ABC, abstractmethod


class DocumentProcessor(ABC):
    """
    Abstract base class for document processing.
    """
    def __init__(self, document_path: str) -> None:
        pass
   

    @abstractmethod
    def load_document(self):
        """
        Load a document from the specified file path.
        """
        pass

    