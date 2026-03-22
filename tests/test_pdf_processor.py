import pytest
from pytest_mock import MockerFixture

from langchain_core.documents.base import Document

from search_agent.document_processors.pdf_processor import PDFProcessor


def test_init_success(mocker: MockerFixture) -> None:
    """
        Test whether get_3gpp_document_path behaves as expected.
    """
    # Arrange
    mock_exists = mocker.patch("pathlib.Path.exists", return_value=True)
    processor = PDFProcessor("data/test.pdf")
    # Act & Assert
    assert processor.file_path == "data/test.pdf"
    mock_exists.assert_called_once()
        

def test_init_folder_not_exists(mocker: MockerFixture) -> None:
    """
        Test whether get_3gpp_document_path raises FileNotFoundError when folder does not exist.
    """
    # Arrange
    mock_exists = mocker.patch("pathlib.Path.exists", return_value=False)
    # Act & Assert
    with pytest.raises(FileNotFoundError, match="Folder .* does not exist."):
        PDFProcessor("data/test.pdf")
    mock_exists.assert_called_once()


def test_load_document_success(mocker) -> None:
    """
    Test whether load_document successfully loads a PDF document.
    """
    # Arrange
    mock_loader_class = mocker.patch("search_agent.document_processors.pdf_processor.PyMuPDFLoader")
    expected_docs = [Document(page_content="test", metadata={})]
    mock_loader_class.return_value.load.return_value = expected_docs
    loger_mock = mocker.patch("search_agent.document_processors.pdf_processor.logger")
    processor = PDFProcessor("data/test.pdf")
    # Act
    document = processor.load_document()
    # Assert
    assert document == expected_docs
    mock_loader_class.return_value.load.assert_called_once()
    loger_mock.info.assert_called_once_with("Document loaded successfully from data/test.pdf.")

def test_load_document_failure(mocker) -> None:

    TEST_FILE_PATH = "data/test.pdf"
    # Arrange
    mock_loader_class = mocker.patch("search_agent.document_processors.pdf_processor.PyMuPDFLoader")
    mock_loader_class.side_effect = Exception(f"Failed to load document from {TEST_FILE_PATH}")
    loger_mock = mocker.patch("search_agent.document_processors.pdf_processor.logger")
    processor = PDFProcessor("data/test.pdf")
    # Act
    with pytest.raises(FileNotFoundError, match="Failed to load document from data/test.pdf:"):
        processor.load_document()
    # Assert
    loger_mock.error.assert_called_once()
