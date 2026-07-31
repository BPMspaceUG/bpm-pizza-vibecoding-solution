# PizzaSim Chatbot - AI Pizza Ordering Assistant

A multilingual AI-powered pizza ordering assistant for PizzaSim.

## Overview

This project implements a chatbot that accepts pizza orders through the PizzaSim API. The bot understands natural language and can process orders directly.

## Features

- 🍕 **Natural Language Processing**: Understands orders like "I am Marco, 2 salami please"
- 🇩🇪/🇬🇧 **Multilingual**: Supports both German and English
- 💻 **Web Interface**: Modern chat UI with FastAPI
- 🎤 **Voice Input**: Browser-based Speech-to-Text support
- 🔄 **Multi-Pizzeria**: Supports multiple pizzerias (Leonardo, Giovanni, Marco, Antonio)
- 📱 **Responsive Design**: Works on desktop and mobile

## Quick Start

```bash
# Install dependencies
pip install fastapi uvicorn

# Start server
python web.py
```

The server runs at: http://127.0.0.1:8888

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | Main page with chat interface |
| `POST /api/chat` | Chat API for messages |
| `GET /{pizzeria}` | Pizzeria-specific page |

## Available Pizzerias

- `/` - PizzaSim (Default)
- `/leonardo` - Pizzeria Leonardo
- `/giovanni` - Pizzeria Giovanni
- `/marco` - Pizzeria Marco
- `/antonio` - Pizzeria Antonio

## Project Structure

```
.
├── agent.py      # Core logic: Tool-calling, order processing
├── web.py        # FastAPI web server and frontend
├── chat.py       # CLI version for testing
├── .env          # Environment variables
└── README.md     # This file
```

## Environment Variables

Create a `.env` file:

```bash
LITELLM_PIZZA_URL=https://your-litellm-instance.com
LITELLM_PIZZA_KEY=your-api-key
PIZZASIM_URL=https://www.aipizzasim.com
PIZZASIM_API_KEY=optional-api-key
```

## Example Orders

The chatbot understands various phrasings:

**German:**
- "Ich bin Marco. Die Straße kennst du. 2 Salami."
- "Hier ist Anna. Ich hätte gerne eine Margherita und 2 Pasta Pesto."
- "Ich heiße Hans. Eine Hawaii und 3 Pasta Tonno bitte."

**English:**
- "My name is John, I want 2 Hawaii pizzas"
- "This is Lisa. I'd like 1 Margherita and 2 Pasta Pesto."
- "I'm Peter. Give me 3 Salami please."

## Technical Details

### Direct Order Parser

For fast orders without LLM latency, a regex-based parser is used:

1. **Name Extraction**: Recognizes "Ich bin...", "Hier ist...", "My name is...", "I am..."
2. **Quantity Parsing**: Understands "2", "two", "2x", "one", "eine", "ein"
3. **Product Recognition**: Matches against dynamically loaded menu

### LLM Fallback

When the direct parser doesn't recognize an order, the LLM with tool-calling is used.

### Tool Schema

```json
{
  "get_menu": "Fetches current menu from PizzaSim",
  "place_order": "Places order with pid, customer, and items"
}
```

## Bug Fixes & Improvements

### Fixed Issues

| Issue | Solution |
|-------|----------|
| Missing `run_in_threadpool` import | Added `from fastapi.concurrency import run_in_threadpool` |
| Async generator in ThreadPool failure | Implemented custom thread + asyncio.Queue solution |
| Pasta orders not recognized | Added optional "pasta" prefix in regex pattern |
| "Hier ist Peter" not recognized | Added new name extraction patterns |
| Hardcoded menu | Menu now loads dynamically from server |
| Duplicate item matches | Added position tracking to prevent duplicates |

## Testing

Run CLI tests:
```bash
python chat.py
```

Test the web interface:
1. Start server: `python web.py`
2. Open browser: http://127.0.0.1:8888
3. Try: "Ich bin Test. 1 Salami."

## Troubleshooting

**Problem**: Server won't start
**Solution**: Check that `.env` file exists with required variables

**Problem**: Orders not being placed
**Solution**: Verify `PIZZASIM_URL` is reachable and API key is correct

**Problem**: Speech input not working
**Solution**: Browser must support Web Speech API (Chrome recommended)

## License

Created as an example solution for students.
