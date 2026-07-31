#!/usr/bin/env python3
"""Shared agent loop for PizzaSim chat (CLI + web)."""

import json
import os
import re
import subprocess


def load_env_file(path, override=False):
    """Load KEY=VALUE pairs from a .env file into os.environ."""
    if not os.path.exists(path):
        return
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip()
                if key:
                    if override or key not in os.environ:
                        os.environ[key] = value


def _bootstrap_env():
    """Load .env files and return (LLM_URL, LLM_KEY, PIZZASIM_URL)."""
    load_env_file(".env", override=True)
    load_env_file(os.path.expanduser("~/.env"))

    llm_url = os.environ.get("LITELLM_PIZZA_URL", "").rstrip("/")
    llm_key = os.environ.get("LITELLM_PIZZA_KEY", "")
    pizzasim_url = os.environ.get("PIZZASIM_URL", "").rstrip("/")

    if not llm_url or not llm_key:
        raise ValueError("LITELLM_PIZZA_URL and LITELLM_PIZZA_KEY must be set")
    if not pizzasim_url:
        raise ValueError("PIZZASIM_URL must be set (checked .env in current directory, then ~/.env)")

    return llm_url, llm_key, pizzasim_url


LLM_URL, LLM_KEY, PIZZASIM_URL = _bootstrap_env()
PIZZASIM_API_KEY = os.environ.get("PIZZASIM_API_KEY", "")
CHAT_ENDPOINT = f"{LLM_URL}/chat/completions"


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

def get_menu():
    """Fetch the PizzaSim menu (public endpoint)."""
    result = subprocess.run(
        ["curl", "-s", f"{PIZZASIM_URL}/menu"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"error": result.stdout or result.stderr}


def place_order(pid: str, customer: dict, items: list):
    """Place an order at PizzaSim for a customer."""
    # Validate pid is a valid UUID format to prevent injection
    if not re.match(r'^[a-zA-Z0-9-]+$', pid):
        return {"error": "Invalid pizzeria ID format"}
    payload = {
        "customer": customer,
        "items": items
    }
    cmd = [
        "curl", "-s", "-X", "POST",
        f"{PIZZASIM_URL}/pizzerias/{pid}/orders",
        "-H", "Content-Type: application/json",
    ]
    if PIZZASIM_API_KEY:
        cmd.extend(["-H", f"X-API-Key: {PIZZASIM_API_KEY}"])
    cmd.extend(["-d", json.dumps(payload)])

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"error": result.stdout or result.stderr}


TOOL_REGISTRY = {
    "get_menu": get_menu,
    "place_order": place_order,
}

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "get_menu",
            "description": "Fetches the current PizzaSim restaurant menu (pizzas and pasta) from the public API. No parameters required.",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "place_order",
            "description": "Places a food order at PizzaSim for a customer. Creates or matches customer by name within the pizzeria.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pid": {
                        "type": "string",
                        "description": "Pizzeria UUID (tenant scope)"
                    },
                    "customer": {
                        "type": "object",
                        "description": "Customer information",
                        "properties": {
                            "first_name": {"type": "string"},
                            "street_one": {"type": "string"}
                        },
                        "required": ["first_name"]
                    },
                    "items": {
                        "type": "array",
                        "description": "Order items",
                        "items": {
                            "type": "object",
                            "properties": {
                                "type": {"type": "string", "enum": ["pizza", "pasta"]},
                                "code": {"type": "string"},
                                "qty": {"type": "integer"},
                                "extras": {"type": "array", "items": {"type": "string"}}
                            },
                            "required": ["type", "code", "qty"]
                        }
                    }
                },
                "required": ["pid", "customer", "items"]
            }
        }
    }
]


# ---------------------------------------------------------------------------
# Completion helper
# ---------------------------------------------------------------------------

def chat_completion(messages, tools=None):
    """Send a chat completion request and return parsed JSON."""
    payload = {
        "model": "openrouter/moonshotai/kimi-k2.5",
        "messages": messages,
    }
    if tools:
        payload["tools"] = tools
        payload["tool_choice"] = "auto"

    result = subprocess.run(
        [
            "curl", "-s", "-X", "POST", CHAT_ENDPOINT,
            "-H", f"Authorization: Bearer {LLM_KEY}",
            "-H", "Content-Type: application/json",
            "-d", json.dumps(payload),
        ],
        capture_output=True,
        text=True,
        check=True,
        timeout=60,
    )
    return json.loads(result.stdout)


# ---------------------------------------------------------------------------
# Agent loop — yields intermediate steps
# ---------------------------------------------------------------------------

SYSTEM_PROMPT_TEMPLATE = """Du bist ein freundlicher Pizza-Bestell-Assistent für PizzaSim.

{{LANG}}

PIZZERIA ID: {{PID}}

DEINE AUFGABE: Bestellungen aufgeben. Immer. KEINE Ausreden.

WICHTIGSTE REGEL - NIEMALS BRECHEN:
Wenn ein Kunde irgendetwas bestellt (Pizza, Pasta, Getränke), RUFE SOFORT die Funktion `place_order` auf!
- Nie fragen ob er sicher ist.
- Nie nach Adresse fragen wenn er sagt "kennst du" oder "Adresse folgt".
- Nie "Ich kann nicht bestellen" sagen.
- IMMER place_order aufrufen mit: pid="{{PID}}", customer, items.

WIE place_order AUFRUFEN:
- pid: stets "{{PID}}"
- customer: {"first_name": "MARCO"} (Straße optional - nur wenn bekannt)
- items: Liste der Artikel. WICHTIG: `qty` = Anzahl als ZAHL (2, nicht "zwei")

KEINE Konversation. KEINE Erklärung. Einfach place_order aufrufen.

Beispiel-Kunde: "Ich bin Marco. Die Straße kennst du. 2 Salami."
→ SOFORT place_order aufrufen mit:
  pid: "{{PID}}"
  customer: {"first_name": "Marco"}
  items: [{"type": "pizza", "code": "salami", "qty": 2, "extras": []}]
"""

def build_system_prompt(pid, lang="de"):
    language_hint = "ANSWER IN ENGLISH." if lang.startswith("en") else "SPRACHE: ANTWORTE IMMER AUF DEUTSCH. NIE ENGLISCH."
    return SYSTEM_PROMPT_TEMPLATE.replace("{{PID}}", pid).replace("{{LANG}}", language_hint)

MENU = {
    "pizzas": ["margherita", "prosciutto", "salami", "funghi", "regina", "mista",
               "hawaii", "tonno", "papa", "diavolo", "grandiosa"],
    "pasta": ["aglioolio", "tonno", "funghi", "pesto"]
}


def parse_qty(text):
    """Konvertiere Wörter wie 'zwei', '2x' -> 2."""
    t = text.strip().lower()
    mapping = {"ein": 1, "eine": 1, "einen": 1, "one": 1,
               "zwei": 2, "two": 2, "drei": 3, "three": 3, "vier": 4, "four": 4,
               "fünf": 5, "five": 5}
    if t in mapping:
        return mapping[t]
    m = re.search(r'\d+', t)
    if m:
        return int(m.group())
    return 1


def extract_name(msg):
    """Extrahiere Vornamen aus 'Ich bin Marco' o.ä."""
    patterns = [
        r'(?:ich bin|mein name ist|ich heiße|i am|my name is)\s+([A-ZÄÖÜ][a-zäöü]+)',
        r'^([A-ZÄÖÜ][a-zäöü]+)(?:\s+hier|$)',
    ]
    for pat in patterns:
        m = re.search(pat, msg, re.I)
        if m:
            return m.group(1)
    return None


def try_parse_order(user_message, menu_items):
    """
    Versuche, eine Bestellung aus der Nachricht zu parsen.
    Gibt (customer_name, items_list) oder (None, None) zurück.
    """
    msg_lower = user_message.lower()

    # Name
    name = extract_name(user_message)
    if not name:
        return None, None

    items = []
    codes = menu_items["pizzas"] + menu_items["pasta"]

    # Regex: Zahl + Code, z.B. "2 salami", "eine margherita"
    for code in codes:
        item_type = "pizza" if code in menu_items["pizzas"] else "pasta"
        # Suche nach "2x salami", "eine Salami", "zwei salami"
        pattern = rf'(\d+x?|\w+)\s+{re.escape(code)}[sb]*'
        matches = re.finditer(pattern, msg_lower, re.I)
        for m in matches:
            qty_str = m.group(1)
            qty = parse_qty(qty_str)
            items.append({"type": item_type, "code": code, "qty": qty, "extras": []})

    # Auch "2 Pizzen" -> fallback
    # Extras: mit pepperoni -> extrahieren
    # TODO: extras parsing

    if not items:
        return None, None

    return {"first_name": name}, items


def run_agent(user_message: str, messages: list | None = None, pid: str = "86517183-e1a5-4bd7-b915-e0db8f8b2131", lang: str = "de"):
    """
    Run the agent loop for *user_message*.

    Yields dicts with shape:
      {"step": "assistant", "content": str}                -- assistant reasoning / text
      {"step": "tool_calls", "tool_calls": [...]}           -- raw tool_calls from model
      {"step": "tool_result", "name": str,"id":str,"result":...}  -- tool execution result
      {"step": "final", "content": str}                    -- final answer (no tool use)
    """
    if messages is None:
        system_prompt = build_system_prompt(pid, lang)
        messages = [{"role": "system", "content": system_prompt}]

    messages.append({"role": "user", "content": user_message})
    yield {"step": "user", "content": user_message}

    # ------------------------------------------------------------------
    # DIREKTER ORDER-PARSER: wenn der Kunde einen Namen + Items nennt,
    # rufen wir place_order SOFORT auf — ohne auf das LLM zu warten.
    # ------------------------------------------------------------------
    customer, items = try_parse_order(user_message, MENU)
    if customer and items:
        result = place_order(pid=pid, customer=customer, items=items)
        yield {"step": "tool_result", "name": "place_order", "id": "auto", "result": result}

        # Bestätigungsmelung zusammenbauen
        lang_prefix = "de" if lang.startswith("de") else "en"
        if "id" in result or "status" in result or "customer_id" in result:
            items_text = ", ".join(
                f"{it['qty']}x {it['code']}" for it in items
            )
            if lang_prefix == "de":
                confirmation = (f"🍕 Bestellung aufgenommen, {customer['first_name']}!\n\n"
                                f"Artikel: {items_text}\n"
                                f"Status: {result.get('status', 'ordered')}")
            else:
                confirmation = (f"🍕 Order placed, {customer['first_name']}!\n\n"
                                f"Items: {items_text}\n"
                                f"Status: {result.get('status', 'ordered')}")
        else:
            confirmation = json.dumps(result, indent=2, ensure_ascii=False)

        # Tool-Nachricht ins Chat-History einfügen, damit die Session konsistent bleibt
        messages.append({
            "role": "assistant",
            "content": confirmation,
        })
        yield {"step": "final", "content": confirmation}
        return

    # ------------------------------------------------------------------
    # FALLBACK: normales LLM + Tool-Calling
    # ------------------------------------------------------------------
    response = chat_completion(messages, tools=TOOLS_SCHEMA)
    assistant_msg = response["choices"][0]["message"]
    messages.append(assistant_msg)

    # Assistant may contain *both* text and tool_calls.
    content = assistant_msg.get("content")
    tool_calls = assistant_msg.get("tool_calls")

    if content:
        yield {"step": "assistant", "content": content}

    if tool_calls:
        yield {"step": "tool_calls", "tool_calls": tool_calls}

        # Execute every tool call
        for tc in tool_calls:
            name = tc["function"]["name"]
            tool_id = tc["id"]
            func = TOOL_REGISTRY.get(name)
            if func is None:
                raise ValueError(f"Unknown tool: {name}")

            # Parse arguments with error handling
            try:
                args = json.loads(tc["function"].get("arguments", "{}"))
            except json.JSONDecodeError as e:
                yield {"step": "tool_result", "name": name, "id": tool_id, "result": {"error": f"Invalid JSON arguments: {e}"}}
                continue

            # Validate required arguments for place_order
            if name == "place_order":
                required = ["pid", "customer", "items"]
                missing = [r for r in required if r not in args]
                if missing:
                    yield {"step": "tool_result", "name": name, "id": tool_id, "result": {"error": f"Missing required arguments: {missing}"}}
                    continue
                result = func(**args)
            elif name == "get_menu":
                result = func()
            else:
                result = func(**args)

            yield {"step": "tool_result", "name": name, "id": tool_id, "result": result}
            messages.append({
                "role": "tool",
                "tool_call_id": tool_id,
                "name": name,
                "content": json.dumps(result),
            })

        # Follow-up request
        follow_up = chat_completion(messages)
        final_content = follow_up["choices"][0]["message"]["content"]
        yield {"step": "final", "content": final_content}
    else:
        # Assistant had no tool calls — its content *is* the final answer
        if content:
            yield {"step": "final", "content": content}
        else:
            yield {"step": "final", "content": "(no response)"}
