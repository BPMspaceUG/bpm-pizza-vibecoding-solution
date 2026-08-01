"""Interactive terminal chat over the core. A transport only: words in,
words out, no order logic.

Run:  python -m channels.cli [--verbose]
"""
from __future__ import annotations

import argparse
import sys

from core.agent import Agent, AgentConfig, create_session, startup
from core.pizzasim import ConfigError, PizzaSimError


def make_emit(verbose: bool):
    def emit(event: dict) -> None:
        if not verbose:
            return
        kind = event["type"]
        if kind == "tool_call":
            print(f"  ⚙ {event['tool']} {event['args']}", file=sys.stderr)
        elif kind == "tool_result":
            print(f"  ← {event['result']}", file=sys.stderr)
        elif kind == "state":
            print(f"  ▸ {event['state']} r{event['revision']}",
                  file=sys.stderr)
    return emit


def main() -> int:
    parser = argparse.ArgumentParser(description="PizzaSim ordering agent")
    parser.add_argument("--verbose", action="store_true",
                        help="show tool calls and state transitions")
    args = parser.parse_args()

    try:
        config = AgentConfig.from_env()
        client, pizzeria_name, _menu = startup(config)
        # One CLI process = one session at the preselected pizzeria in
        # PIZZERIA_LANG (no switching in this channel, per SPEC).
        session = create_session(config, client)
    except (ConfigError, ValueError) as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        return 1
    except PizzaSimError as exc:
        print(f"Startup check against PizzaSim failed: {exc}\n"
              "We're not taking orders right now.", file=sys.stderr)
        return 1

    agent = Agent(config)
    emit = make_emit(args.verbose)

    print(f"[{pizzeria_name} — type your order, Ctrl-D to hang up]")
    print(agent.run_turn(session, None, emit))  # agent greets first
    while True:
        try:
            text = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if not text:
            continue
        print(agent.run_turn(session, text, emit))


if __name__ == "__main__":
    sys.exit(main())
