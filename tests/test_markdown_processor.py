import pytest
from pathlib import Path
from pytest_mock import MockerFixture

from search_agent.document_processors.markdown_processor import MarkdownProcessor


def test_get_3gpp_document_path(mocker: MockerFixture) -> None:
    """
        Test whether get_3gpp_document_path behaves as expected.
    """
    # Arrange
    mock_exists = mocker.patch("pathlib.Path.exists", return_value=True)
    mock_glob = mocker.patch("pathlib.Path.glob", return_value=[Path("data/3GPP_TS_24.501.md")])
    md_processor = MarkdownProcessor()

    # Act & Assert
    assert md_processor.get_3gpp_document_path() == "data/3GPP_TS_24.501.md"
    mock_exists.assert_called_once()
    mock_glob.assert_called_once()
        

def test_get_3gpp_document_path_no_folder(mocker: MockerFixture) -> None:
    """
        Test whether get_3gpp_document_path raises FileNotFoundError when folder does not exist.
    """
    # Arrange
    mock_exists = mocker.patch("pathlib.Path.exists", return_value=False)
    md_processor = MarkdownProcessor()
    
    # Act & Assert
    with pytest.raises(FileNotFoundError, match="Folder data does not exist."):
        md_processor.get_3gpp_document_path()
    
    mock_exists.assert_called_once()


def test_get_3gpp_document_path_no_markdown_files(mocker: MockerFixture) -> None:
    """
        Test whether get_3gpp_document_path raises FileNotFoundError when no Markdown files are found.
    """
    # Arrange
    mock_exist = mocker.patch("pathlib.Path.exists", return_value=True)
    mock_glob = mocker.patch("pathlib.Path.glob", return_value=[])
    md_processor = MarkdownProcessor()

    # Act & Assert
    with pytest.raises(FileNotFoundError, match="No Markdown files found in the specified directory."):
        md_processor.get_3gpp_document_path()

    mock_exist.assert_called_once()
    mock_glob.assert_called_once()


def test_load_document_success(mocker) -> None:
    """
    Test whether load_document successfully loads a Markdown document.
    """
    # Arrange
    mock_open = mocker.patch("builtins.open", mocker.mock_open(read_data="# Test Content"))
    loger_mock = mocker.patch("search_agent.document_processors.markdown_processor.logger")
    md_processor = MarkdownProcessor()

    # Act
    content = md_processor.load_document("data/test.md")

    # Assert
    assert content == "# Test Content"
    mock_open.assert_called_once_with("data/test.md", "r", encoding="utf-8")
    loger_mock.info.assert_called_once_with("Document loaded successfully from data/test.md.")

def test_load_document_failure(mocker) -> None:

    TEST_FILE_PATH = "data/test.md"
    # Arrange
    mock_open = mocker.patch("builtins.open", side_effect=Exception(f"Failed to load document from {TEST_FILE_PATH}"))
    loger_mock = mocker.patch("search_agent.document_processors.markdown_processor.logger")
    md_processor = MarkdownProcessor()

    # Act
    result = md_processor.load_document(TEST_FILE_PATH)

    # Assert
    assert result is None
    mock_open.assert_called_once_with("data/test.md", "r", encoding="utf-8")
    loger_mock.error.assert_called_once_with(f"Failed to load document from {TEST_FILE_PATH}: Failed to load document from {TEST_FILE_PATH}")
