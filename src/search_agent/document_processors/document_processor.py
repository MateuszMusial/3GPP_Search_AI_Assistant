from abc import ABC, abstractmethod


class DocumentProcessor(ABC):
    """
    Abstract base class for document processing.
    """
    @abstractmethod
    def get_3gpp_document_path(self, data_dir: str) -> str:
        """
        Get the path of the first document in the specified directory.
        """
        pass

    @abstractmethod
    def load_document(self, file_path: str):
        """
        Load a document from the specified file path.
        """
        pass

    