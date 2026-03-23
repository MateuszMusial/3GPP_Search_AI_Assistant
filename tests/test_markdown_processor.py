import pytest
from pytest_mock import MockerFixture

from search_agent.document_processors.markdown_processor import MarkdownProcessor


def test_init_success(mocker: MockerFixture) -> None:
    """
        Test whether get_3gpp_document_path behaves as expected.
    """
    # Arrange
    mock_exists = mocker.patch("pathlib.Path.exists", return_value=True)
    processor = MarkdownProcessor("data/test.md")
    # Act & Assert
    assert processor.file_path == "data/test.md"
    mock_exists.assert_called_once()
        

def test_init_folder_not_exists(mocker: MockerFixture) -> None:
    """
        Test whether get_3gpp_document_path raises FileNotFoundError when folder does not exist.
    """
    # Arrange
    mock_exists = mocker.patch("pathlib.Path.exists", return_value=False)
    # Act & Assert
    with pytest.raises(FileNotFoundError, match="Folder .* does not exist."):
        MarkdownProcessor("data/test.md")
    mock_exists.assert_called_once()


def test_load_document_success(mocker) -> None:
    """
    Test whether load_document successfully loads a Markdown document.
    """
    # Arrange
    loger_mock = mocker.patch("search_agent.document_processors.markdown_processor.logger")
    mock_open = mocker.patch("builtins.open", mocker.mock_open(read_data="# Test Content"))
    processor = MarkdownProcessor("data/test.md")
    # Act
    content = processor.load_document()
    # Assert
    assert len(content) == 1
    assert content[0].page_content == "# Test Content"
    assert content[0].metadata["source"] == "data/test.md"
    loger_mock.info.assert_called_once_with("Document loaded successfully from data/test.md.")
    mock_open.assert_called_once_with("data/test.md", "r", encoding="utf-8")

def test_load_document_failure(mocker) -> None:

    TEST_FILE_PATH = "data/test.md"
    # Arrange
    mock_open = mocker.patch("builtins.open", side_effect=Exception(f"Failed to load document from {TEST_FILE_PATH}"))
    loger_mock = mocker.patch("search_agent.document_processors.markdown_processor.logger")
    processor = MarkdownProcessor("data/test.md")
    # Act
    with pytest.raises(FileNotFoundError, match="Failed to load document from data/test.md:"):
        processor.load_document()
    # Assert
    loger_mock.error.assert_called_once()
    mock_open.assert_called_once_with("data/test.md", "r", encoding="utf-8")
