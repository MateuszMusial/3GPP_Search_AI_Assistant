import pytest
from pytest_mock import MockerFixture

from search_agent.models.openai_models import OpenAIModelService



def test_OpenAIModelService_initialization(mocker: MockerFixture):
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



if __name__ == "__main__":
    pytest.main()