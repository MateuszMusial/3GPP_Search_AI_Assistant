from typing import cast
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from langchain_core.documents.base import Document

from search_agent.rag_pipeline import RAGPipeline, FAISS_INDEX_PATH


# A body of text long enough to force the splitter to produce several chunks.
LONG_TEXT = "3GPP technical specification content. " * 500


@pytest.fixture
def pipeline(mocker: MockerFixture) -> RAGPipeline:
    """Provide a RAGPipeline wired with mocked collaborators."""
    file_processor = mocker.MagicMock()
    file_processor.file_path = "test.pdf"
    embedding_service = mocker.MagicMock()
    return RAGPipeline(file_processor=file_processor, embedding_service=embedding_service)


def test_init_stores_dependencies(mocker: MockerFixture) -> None:
    """Test __init__ keeps references to the processor and embedding service."""
    # Arrange
    file_processor = mocker.MagicMock()
    embedding_service = mocker.MagicMock()

    # Act
    pipeline = RAGPipeline(file_processor=file_processor, embedding_service=embedding_service)

    # Assert
    assert pipeline.file_processor is file_processor
    assert pipeline.embedding_service is embedding_service


@pytest.mark.parametrize(
    "chunk_size, chunk_overlap",
    [
        (1000, 200),
        (500, 100),
        (200, 50),
    ],
)
def test_split_text_produces_multiple_bounded_chunks(
    pipeline: RAGPipeline, chunk_size: int, chunk_overlap: int
) -> None:
    """Test split_text chunks a long document without exceeding chunk_size."""
    # Arrange
    docs = [Document(page_content=LONG_TEXT, metadata={"source": "test.pdf"})]

    # Act
    chunks = pipeline.split_text(docs, chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    # Assert
    assert len(chunks) > 1
    assert all(isinstance(chunk, Document) for chunk in chunks)
    assert all(len(chunk.page_content) <= chunk_size for chunk in chunks)


def test_split_text_configures_splitter(pipeline: RAGPipeline, mocker: MockerFixture) -> None:
    """Test split_text forwards its size/overlap to the underlying splitter."""
    # Arrange
    mock_splitter_cls = mocker.patch("search_agent.rag_pipeline.RecursiveCharacterTextSplitter")
    mock_splitter_cls.return_value.split_documents.return_value = ["chunk"]
    docs = [Document(page_content="content")]

    # Act
    result = pipeline.split_text(docs, chunk_size=512, chunk_overlap=64)

    # Assert
    mock_splitter_cls.assert_called_once_with(chunk_size=512, chunk_overlap=64)
    mock_splitter_cls.return_value.split_documents.assert_called_once_with(docs)
    assert result == ["chunk"]


def test_embed_texts_builds_and_persists_vectorstore(
    pipeline: RAGPipeline, mocker: MockerFixture
) -> None:
    """Test embed_texts creates a FAISS store from chunks and saves it locally."""
    # Arrange
    mock_faiss = mocker.patch("search_agent.rag_pipeline.FAISS")
    mock_vectorstore = mock_faiss.from_documents.return_value
    chunks = [Document(page_content="chunk")]

    # Act
    result = pipeline.embed_texts(chunks, embedding_service=pipeline.embedding_service)

    # Assert
    mock_faiss.from_documents.assert_called_once_with(chunks, pipeline.embedding_service)
    mock_vectorstore.save_local.assert_called_once_with(FAISS_INDEX_PATH, index_name="test.pdf.faiss")
    assert result is mock_vectorstore


def test_start_rag_pipeline_returns_cached_index_when_present(
    pipeline: RAGPipeline, mocker: MockerFixture
) -> None:
    """Test start_rag_pipeline loads the existing index instead of rebuilding."""
    # Arrange
    mocker.patch("pathlib.Path.exists", return_value=True)
    mock_load = mocker.patch.object(pipeline, "load_vectorstore")

    # Act
    result = pipeline.start_rag_pipeline()

    # Assert
    mock_load.assert_called_once()
    assert result is mock_load.return_value


def test_start_rag_pipeline_builds_index_when_absent(
    pipeline: RAGPipeline, mocker: MockerFixture
) -> None:
    """Test start_rag_pipeline loads, splits, and embeds when no index exists."""
    # Arrange
    mocker.patch("pathlib.Path.exists", return_value=False)
    docs = [Document(page_content="content")]
    file_processor = cast(MagicMock, pipeline.file_processor)
    file_processor.load_document.return_value = docs
    mock_split = mocker.patch.object(pipeline, "split_text", return_value=["chunk"])
    mock_embed = mocker.patch.object(pipeline, "embed_texts")

    # Act
    result = pipeline.start_rag_pipeline()

    # Assert
    file_processor.load_document.assert_called_once()
    mock_split.assert_called_once_with(docs)
    mock_embed.assert_called_once_with(["chunk"], embedding_service=pipeline.embedding_service)
    assert result is mock_embed.return_value


def test_start_rag_pipeline_returns_none_when_document_missing(
    pipeline: RAGPipeline, mocker: MockerFixture
) -> None:
    """Test start_rag_pipeline returns None when the document cannot be loaded."""
    # Arrange
    mocker.patch("pathlib.Path.exists", return_value=False)
    file_processor = cast(MagicMock, pipeline.file_processor)
    file_processor.load_document.side_effect = FileNotFoundError("missing")

    # Act
    result = pipeline.start_rag_pipeline()

    # Assert
    assert result is None


def test_start_rag_pipeline_returns_none_when_no_chunks(
    pipeline: RAGPipeline, mocker: MockerFixture
) -> None:
    """Test start_rag_pipeline returns None when splitting yields no chunks."""
    # Arrange
    mocker.patch("pathlib.Path.exists", return_value=False)
    file_processor = cast(MagicMock, pipeline.file_processor)
    file_processor.load_document.return_value = [Document(page_content="content")]
    mocker.patch.object(pipeline, "split_text", return_value=[])

    # Act
    result = pipeline.start_rag_pipeline()

    # Assert
    assert result is None


def test_load_vectorstore_loads_from_disk(pipeline: RAGPipeline, mocker: MockerFixture) -> None:
    """Test load_vectorstore reads the index from disk when it exists."""
    # Arrange
    mocker.patch("pathlib.Path.exists", return_value=True)
    mock_faiss = mocker.patch("search_agent.rag_pipeline.FAISS")

    # Act
    result = pipeline.load_vectorstore()

    # Assert
    mock_faiss.load_local.assert_called_once_with(
        FAISS_INDEX_PATH,
        embeddings=pipeline.embedding_service,
        allow_dangerous_deserialization=True,
    )
    assert result is mock_faiss.load_local.return_value


def test_load_vectorstore_returns_none_when_missing(
    pipeline: RAGPipeline, mocker: MockerFixture
) -> None:
    """Test load_vectorstore returns None when no index is present on disk."""
    # Arrange
    mocker.patch("pathlib.Path.exists", return_value=False)

    # Act
    result = pipeline.load_vectorstore()

    # Assert
    assert result is None
