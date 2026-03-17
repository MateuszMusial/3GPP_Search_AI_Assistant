import os
import pytest
from pytest_mock import MockerFixture

from search_agent.models.google_models import GoogleModelService, EMBEDDING_MODEL_NAME


@pytest.mark.parametrize(
        "model_name, expected",
        [
            ("gemini-3-pro-preview", "gemini-3-pro-preview"),
            ("gemini-2.5-flash", "gemini-2.5-flash"),
        ]
)
def test_init_with_model_name(model_name: str, expected: str) -> None:
    """Test initialization with different model names."""
    # Arrange / Act
    service = GoogleModelService(model_name=model_name)

    # Assert
    assert service.model_name == expected


def test_init_default_model() -> None:
    """Test initialization with default model name."""
    # Arrange / Act
    service = GoogleModelService()

    # Assert
    assert service.model_name == "gemini-3-pro-preview"


def test_get_api_key_success(mocker: MockerFixture) -> None:
    """Test _get_api_key returns the API key from environment."""
    # Arrange
    mocker.patch.dict(os.environ, {"GOOGLE_API_KEY": "test_api_key"})
    service = GoogleModelService()

    # Act
    api_key = service._get_api_key()

    # Assert
    assert api_key == "test_api_key"


def test_get_api_key_missing(mocker: MockerFixture) -> None:
    """Test _get_api_key raises ValueError when API key is missing."""
    # Arrange
    mocker.patch.dict(os.environ, {}, clear=True)
    service = GoogleModelService()

    # Act / Assert
    with pytest.raises(ValueError, match="GOOGLE_API_KEY not found in environment variables."):
        service._get_api_key()


@pytest.mark.parametrize(
        "temperature",
        [
            0.1, 0.5, 0.9
        ]
)
def test_create_llm_model_with_temperature(mocker: MockerFixture, temperature: float) -> None:
    """Test create_llm_model with different temperatures."""
    # Arrange
    mocker.patch.dict(os.environ, {"GOOGLE_API_KEY": "test_api_key"})
    mock_google_ai = mocker.patch("search_agent.models.google_models.GoogleGenerativeAI")
    service = GoogleModelService(model_name="gemini-3-pro-preview")

    # Act
    service.create_llm_model(temperature=temperature)

    # Assert
    mock_google_ai.assert_called_once_with(
        model="gemini-3-pro-preview",
        temperature=temperature,
        api_key="test_api_key"
    )


def test_create_llm_model_default_temperature(mocker: MockerFixture) -> None:
    """Test create_llm_model with default temperature."""
    # Arrange
    mocker.patch.dict(os.environ, {"GOOGLE_API_KEY": "test_api_key"})
    mock_google_ai = mocker.patch("search_agent.models.google_models.GoogleGenerativeAI")
    service = GoogleModelService()

    # Act
    service.create_llm_model()

    # Assert
    mock_google_ai.assert_called_once_with(
        model="gemini-3-pro-preview",
        temperature=0.1,
        api_key="test_api_key"
    )


def test_create_embedding_model(mocker: MockerFixture) -> None:
    """Test create_embedding_model creates embedding model correctly."""
    # Arrange
    mocker.patch.dict(os.environ, {"GOOGLE_API_KEY": "test_api_key"})
    mock_embeddings = mocker.patch("search_agent.models.google_models.GoogleGenerativeAIEmbeddings")
    service = GoogleModelService()

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
    service = GoogleModelService()

    # Act / Assert
    with pytest.raises(ValueError, match="GOOGLE_API_KEY not found in environment variables."):
        service.create_llm_model()


def test_create_embedding_model_missing_api_key(mocker: MockerFixture) -> None:
    """Test create_embedding_model raises ValueError when API key is missing."""
    # Arrange
    mocker.patch.dict(os.environ, {}, clear=True)
    service = GoogleModelService()

    # Act / Assert
    with pytest.raises(ValueError, match="GOOGLE_API_KEY not found in environment variables."):
        service.create_embedding_model()
