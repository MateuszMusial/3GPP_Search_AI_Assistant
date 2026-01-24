import pytest
from pathlib import Path
from pytest_mock import MockerFixture
from document_processors.pdf_processor import PDFProcessor
from langchain_core.documents.base import Document



def test_get_3gpp_document_path(mocker: MockerFixture) -> None:
    """
        Test whether get_3gpp_document_path behaves as expected.
    """
    # Arrange
    mock_exists = mocker.patch("pathlib.Path.exists", return_value=True)
    mock_glob = mocker.patch("pathlib.Path.glob", return_value=[Path("data/3GPP_TS_24.501.pdf")])
    pdf_processor = PDFProcessor()

    # Act & Assert
    assert pdf_processor.get_3gpp_document_path() == "data/3GPP_TS_24.501.pdf"
    mock_exists.assert_called_once()
    mock_glob.assert_called_once()
        

def test_get_3gpp_document_path_no_folder(mocker: MockerFixture) -> None:
    """
        Test whether get_3gpp_document_path raises FileNotFoundError when folder does not exist.
    """
    # Arrange
    mock_exists = mocker.patch("pathlib.Path.exists", return_value=False)
    pdf_processor = PDFProcessor()
    
    # Act & Assert
    with pytest.raises(FileNotFoundError, match="Folder data does not exist."):
        pdf_processor.get_3gpp_document_path()
    
    mock_exists.assert_called_once()


def test_get_3gpp_document_path_no_pdfs(mocker: MockerFixture) -> None:
    """
        Test whether get_3gpp_document_path raises FileNotFoundError when no PDFs are found.
    """
    # Arrange
    mock_exist = mocker.patch("pathlib.Path.exists", return_value=True)
    mock_glob = mocker.patch("pathlib.Path.glob", return_value=[])
    pdf_processor = PDFProcessor()

    # Act & Assert
    with pytest.raises(FileNotFoundError, match="No PDF files found in the specified directory."):
        pdf_processor.get_3gpp_document_path()

    mock_exist.assert_called_once()
    mock_glob.assert_called_once()


def test_load_document_success(mocker) -> None:
    """
    Test whether load_document successfully loads a PDF document.
    """
    # Arrange
    mock_loader_class = mocker.patch("document_processors.pdf_processor.PyMuPDFLoader")
    expected_docs = [Document(page_content="test", metadata={})]
    mock_loader_class.return_value.load.return_value = expected_docs
    loger_mock = mocker.patch("document_processors.pdf_processor.logger")
    pdf_processor = PDFProcessor()

    # Act
    document = pdf_processor.load_document("data/test.pdf")

    # Assert
    assert document == expected_docs
    mock_loader_class.assert_called_once_with("data/test.pdf")
    mock_loader_class.return_value.load.assert_called_once()
    loger_mock.info.assert_called_once_with("Document loaded successfully from data/test.pdf.")

def test_load_document_failure(mocker) -> None:

    TEST_FILE_PATH = "data/test.pdf"
    # Arrange
    mock_loader_class = mocker.patch("document_processors.pdf_processor.PyMuPDFLoader")
    mock_loader_class.side_effect = Exception(f"Failed to load document from {TEST_FILE_PATH}")
    loger_mock = mocker.patch("document_processors.pdf_processor.logger")
    pdf_processor = PDFProcessor()

    # Act
    result = pdf_processor.load_document(TEST_FILE_PATH)

    # Assert
    assert result is None
    mock_loader_class.assert_called_once_with("data/test.pdf")
    loger_mock.error.assert_called_once_with(f"Failed to load document from {TEST_FILE_PATH}: Failed to load document from {TEST_FILE_PATH}")
