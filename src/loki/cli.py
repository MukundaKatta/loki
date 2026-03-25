"""Command-line interface for Loki browser automation agent."""

import argparse
import json
import sys
from typing import List

from loki.core import BrowserAgent


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="loki",
        description="Loki - AI-powered browser automation via natural language",
    )
    sub = parser.add_subparsers(dest="command")

    # run — interactive REPL
    sub.add_parser("run", help="Start an interactive command loop")

    # execute — run a script file
    exec_p = sub.add_parser("execute", help="Execute a script file of commands")
    exec_p.add_argument("file", help="Path to a script file (one command per line)")

    # history — show action history
    sub.add_parser("history", help="Show action history for the current session")

    return parser


def _interactive_loop(agent: BrowserAgent) -> None:
    """Simple REPL for issuing browser commands."""
    print("Loki interactive shell  (type 'quit' or 'exit' to stop)")
    while True:
        try:
            line = input("loki> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        line = line.strip()
        if line.lower() in ("quit", "exit"):
            break
        if not line:
            continue
        results = agent.run(line)
        for r in results:
            print(json.dumps(r, indent=2))


def _execute_file(agent: BrowserAgent, path: str) -> List:
    """Execute every command in *path*."""
    with open(path) as fh:
        script = fh.read()
    return agent.run_script(script)


def main(argv: "List[str] | None" = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    agent = BrowserAgent()

    if args.command == "run":
        _interactive_loop(agent)
    elif args.command == "execute":
        results = _execute_file(agent, args.file)
        for r in results:
            print(json.dumps(r, indent=2))
    elif args.command == "history":
        if not agent.history:
            print("No actions recorded yet.")
        for entry in agent.history:
            print(json.dumps(entry, indent=2))
    else:
        parser.print_help()

    return 0
