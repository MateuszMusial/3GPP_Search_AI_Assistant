import os
import pytest
from pytest_mock import MockerFixture

from search_agent.models.openai_models import OpenAIModelService, EMBEDDING_MODEL_NAME


def test_OpenAIModelService_initialization(mocker: MockerFixture) -> None:
    """
    Test OpenAIModelService initialization with default model name.
    """
    # Arrange
    logger_mock = mocker.patch("search_agent.models.openai_models.logger.info")
    # Act
    test_openAI_service = OpenAIModelService()
    # Assert
    assert test_openAI_service.model_name == "gpt-5-nano"
    logger_mock.assert_called_once_with("Initializing OpenAIModelService...")


@pytest.mark.parametrize(
    "model_name, expected",
    [
        ("gpt-5-nano", "gpt-5-nano"),
        ("gpt-4.0-turbo-preview", "gpt-4.0-turbo-preview"),
    ]
)
def test_init_with_model_name(model_name: str, expected: str) -> None:
    """Test initialization with different model names."""
    # Arrange / Act
    service = OpenAIModelService(model_name=model_name)
    # Assert
    assert service.model_name == expected


def test_get_api_key_success(mocker: MockerFixture) -> None:
    """Test _get_api_key returns the API key from environment."""
    # Arrange
    mocker.patch.dict(os.environ, {"OPENAI_API_KEY": "test_api_key"})
    service = OpenAIModelService()
    # Act
    api_key = service._get_api_key()
    # Assert
    assert api_key == "test_api_key"


def test_get_api_key_missing(mocker: MockerFixture) -> None:
    """Test _get_api_key raises ValueError when API key is missing."""
    # Arrange
    mocker.patch.dict(os.environ, {}, clear=True)
    service = OpenAIModelService()
    # Act / Assert
    with pytest.raises(ValueError, match="OPENAI_API_KEY not found in environment variables."):
        service._get_api_key()


@pytest.mark.parametrize("temperature", [0.1, 0.5, 0.9])
def test_create_llm_model_with_temperature(mocker: MockerFixture, temperature: float) -> None:
    """Test create_llm_model with different temperatures."""
    # Arrange
    mocker.patch.dict(os.environ, {"OPENAI_API_KEY": "test_api_key"})
    mock_openai = mocker.patch("search_agent.models.openai_models.OpenAI")
    service = OpenAIModelService(model_name="gpt-5-nano")
    # Act
    service.create_llm_model(temperature=temperature)
    # Assert
    mock_openai.assert_called_once_with(
        model="gpt-5-nano",
        temperature=temperature,
        api_key="test_api_key"
    )


def test_create_llm_model_default_temperature(mocker: MockerFixture) -> None:
    """Test create_llm_model with default temperature."""
    # Arrange
    mocker.patch.dict(os.environ, {"OPENAI_API_KEY": "test_api_key"})
    mock_openai = mocker.patch("search_agent.models.openai_models.OpenAI")
    service = OpenAIModelService()
    # Act
    service.create_llm_model()
    # Assert
    mock_openai.assert_called_once_with(
        model="gpt-5-nano",
        temperature=0.1,
        api_key="test_api_key"
    )


def test_create_embedding_model(mocker: MockerFixture) -> None:
    """Test create_embedding_model creates embedding model correctly."""
    # Arrange
    mocker.patch.dict(os.environ, {"OPENAI_API_KEY": "test_api_key"})
    mock_embeddings = mocker.patch("search_agent.models.openai_models.OpenAIEmbeddings")
    service = OpenAIModelService()
    # Act
    service.create_embedding_model()
    # Assert
    mock_embeddings.assert_called_once_with(
        model=EMBEDDING_MODEL_NAME,
        api_key="test_api_key"
    )


def test_create_llm_model_missing_api_key(mocker: MockerFixture) -> None:
    """Test create_llm_model raises ValueError when API key is missing."""
    # Arrange
    mocker.patch.dict(os.environ, {}, clear=True)
    service = OpenAIModelService()
    # Act / Assert
    with pytest.raises(ValueError, match="OPENAI_API_KEY not found in environment variables."):
        service.create_llm_model()


def test_create_embedding_model_missing_api_key(mocker: MockerFixture) -> None:
    """Test create_embedding_model raises ValueError when API key is missing."""
    # Arrange
    mocker.patch.dict(os.environ, {}, clear=True)
    service = OpenAIModelService()
    # Act / Assert
    with pytest.raises(ValueError, match="OPENAI_API_KEY not found in environment variables."):
        service.create_embedding_model()


if __name__ == "__main__":
    pytest.main()
