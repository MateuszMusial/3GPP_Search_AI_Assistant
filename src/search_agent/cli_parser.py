import argparse


def get_parser() -> argparse.ArgumentParser:    
    parser = argparse.ArgumentParser(
        description="Search Agent CLI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--ie", type=str, help="Information element or message to find.", required=True)
    parser.add_argument(
        "--model",
        type=str,
        default="gemini-3-pro-preview",
        choices=["gemini-3-pro-preview", "gemini-2.5-flash", "gpt-5-nano", "gpt-4.0-turbo-preview"],
        help="""
        LLM model to use for query execution.
        Options include:
        [gemini-3-pro-preview, gemini-2.5-flash] for Google Generative.
        [gpt-5-nano, gpt-4.0-turbo-preview] for OpenAI.
        """)
    return parser


def parse_cli_args() -> argparse.Namespace:
    return get_parser().parse_args()
