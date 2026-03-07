from search_agent.cli_parser import get_parser


def test_get_parser() -> None:
    """
    @brief Test whether the CLI parser is created correctly.
    """
    # Arrange
    # Act
    test_parser = get_parser()
    # Assert
    assert test_parser is not None
    assert test_parser.description == "Search Agent CLI"
    

def test_parse_cli_args() -> None:
    """
    @brief Test whether CLI arguments are parsed correctly.
    """

    # Arrange
    test_parser = get_parser()
    test_args = ["--ie", "Test Information Element", "--model", "gpt-5-nano"]
    # Act
    parsed_args = test_parser.parse_args(test_args)
    # Assert
    assert parsed_args.ie is not None
    assert parsed_args.ie == "Test Information Element"
    assert parsed_args.model == "gpt-5-nano"
