from typing import cast
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from langchain_core.documents.base import Document

from search_agent.query_executor import QueryExecutor


@pytest.fixture
def query_executor(mocker: MockerFixture) -> QueryExecutor:
    """Provide a QueryExecutor whose pipeline and model are mocked.

    The pipeline yields a mock vectorstore so individual tests can configure
    its ``similarity_search`` behaviour.
    """
    file_processor = mocker.MagicMock()
    llm_model = mocker.MagicMock()
    pipeline = mocker.MagicMock()
    pipeline.start_rag_pipeline.return_value = mocker.MagicMock()
    return QueryExecutor(file_processor=file_processor, llm_model=llm_model, pipeline=pipeline)


def test_init_wires_vectorstore_and_model(mocker: MockerFixture) -> None:
    """Test __init__ builds the vectorstore from the pipeline and the LLM model."""
    # Arrange
    file_processor = mocker.MagicMock()
    llm_model = mocker.MagicMock()
    pipeline = mocker.MagicMock()
    sentinel_vectorstore = mocker.MagicMock()
    pipeline.start_rag_pipeline.return_value = sentinel_vectorstore

    # Act
    executor = QueryExecutor(file_processor=file_processor, llm_model=llm_model, pipeline=pipeline)

    # Assert
    assert executor.vectorstore is sentinel_vectorstore
    assert executor.model is llm_model.create_llm_model.return_value
    pipeline.start_rag_pipeline.assert_called_once()
    llm_model.create_llm_model.assert_called_once()


def test_execute_query_returns_model_response(
    query_executor: QueryExecutor, mocker: MockerFixture
) -> None:
    """Test execute_query retrieves context and returns the chain's answer."""
    # Arrange
    docs = [Document(page_content="chunk one"), Document(page_content="chunk two")]
    vectorstore = cast(MagicMock, query_executor.vectorstore)
    vectorstore.similarity_search.return_value = docs
    mock_prompt = mocker.MagicMock()
    mock_chain = mock_prompt.__or__.return_value
    mock_chain.invoke.return_value = "Generated answer"
    mocker.patch("search_agent.query_executor.get_prompt_template", return_value=mock_prompt)

    # Act
    result = query_executor.execute_query("RLF timer")

    # Assert
    assert result == "Generated answer"
    vectorstore.similarity_search.assert_called_once_with("RLF timer", k=4)
    mock_chain.invoke.assert_called_once_with(
        {"context": "chunk one\n\nchunk two", "target_ie": "RLF timer"}
    )


def test_execute_query_without_vectorstore_returns_error(query_executor: QueryExecutor) -> None:
    """Test execute_query reports an error when the vectorstore failed to load."""
    # Arrange
    query_executor.vectorstore = None

    # Act
    result = query_executor.execute_query("RLF timer")

    # Assert
    assert result == "Error: Vectorstore could not be loaded."


def test_execute_query_without_matches_returns_message(query_executor: QueryExecutor) -> None:
    """Test execute_query returns a friendly message when retrieval finds nothing."""
    # Arrange
    vectorstore = cast(MagicMock, query_executor.vectorstore)
    vectorstore.similarity_search.return_value = []

    # Act
    result = query_executor.execute_query("unknown IE")

    # Assert
    assert result == "No relevant information found in the documents."
