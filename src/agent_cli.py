"""Console script helpers for the OpenAI agent."""
from __future__ import annotations

import argparse
import sys

from openai_agent import OpenAIAgent


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate text using OpenAI")
    parser.add_argument("prompt", help="The prompt to send to the OpenAI model")
    parser.add_argument(
        "--model",
        default="gpt-4o-mini",
        help="Model identifier to use (default: gpt-4o-mini)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])

    try:
        agent = OpenAIAgent()
        response = agent.generate_response(args.prompt, model=args.model)
    except Exception as exc:  # pragma: no cover - CLI error propagation
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(response)
    return 0


__all__ = ["main", "parse_args"]


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
