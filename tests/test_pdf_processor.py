import pytest
from pathlib import Path
from pytest_mock import MockerFixture
from document_processors.pdf_processor import PDFProcessor



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
