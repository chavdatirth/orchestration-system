"""Main CLI module for interacting with JARVIS."""

import argparse
import sys


def run_cli(args: list[str] | None = None) -> None:
    """Run the command line interface parser and handle execution.

    Args:
        args: Command line argument overrides for testing.
    """
    parser = argparse.ArgumentParser(
        description="JARVIS AI Orchestration Operating System Command Line Interface."
    )
    parser.add_argument("--version", action="store_true", help="Print version number and exit.")
    parsed = parser.parse_args(args)

    if parsed.version:
        print("JARVIS OS v0.1.0")
        sys.exit(0)

    parser.print_help()


if __name__ == "__main__":
    run_cli()
