#!/usr/bin/env python3
"""CLI chat with tool calling: fetches PizzaSim menu and gets recommendations."""

import json
from agent import run_agent


def main():
    messages = []
    user_input = "What is on the menu? Recommend one pizza and one pasta."

    for event in run_agent(user_input, messages):
        step = event["step"]

        if step == "user":
            print("=== Step 1: Initial request ===")
            print(f"User message: {event['content']!r}")
            print()

        elif step == "assistant":
            print("=== Assistant reasoning ===")
            print(event["content"])
            print()

        elif step == "tool_calls":
            print("=== Step 2: Model response — raw tool_calls array ===")
            print(json.dumps(event["tool_calls"], indent=2))
            print()

        elif step == "tool_result":
            print(f"=== Step 3: Executing tool '{event['name']}' ===")
            print("=== Step 3: Tool result (menu JSON) ===")
            print(json.dumps(event["result"], indent=2))
            print()
            print("=== Step 4: Sending follow-up with tool result ===")
            print()

        elif step == "final":
            print("=== Step 5: Final answer ===")
            print(event["content"])


if __name__ == "__main__":
    main()
