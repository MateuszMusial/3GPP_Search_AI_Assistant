import argparse


def get_parser() -> argparse.ArgumentParser:    
    parser = argparse.ArgumentParser(
        description="Search Agent CLI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--ie", type=str, help="Information element or message to find.", required=True)
    return parser


def parse_cli_args() -> argparse.Namespace:
    return get_parser().parse_args()