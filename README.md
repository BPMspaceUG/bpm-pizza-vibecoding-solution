# PizzaSim Ordering Agent

An ordering agent for the PizzaSim demo kitchen. The order is a state
machine owned by the code; the model only turns customer language into tool
calls. See <a href="SPEC.md">SPEC.md</a> for the full specification and
<a href="PLAN.md">PLAN.md</a> for the design.

## Setup

```bash
python3 -m venv venv
venv/bin/pip install -r requirements.txt
venv/bin/python -m playwright install chromium   # for the browser E2E tests
```

Configuration comes from the environment (or `~/.env`); every variable in
`.env.example` except the four `SPEECH_*` ones is required — including
`PIZZERIA_LANG` (initial language, `de`/`en`) and `APP_VERSION` (`x.y.z`,
shown in the web footer, raised on every release). The process refuses to
start when one is missing, naming the variable. No values are ever printed
or logged.

## CLI channel

```bash
venv/bin/python -m channels.cli            # plain chat
venv/bin/python -m channels.cli --verbose  # + tool calls and states
```

One CLI process serves the preselected `PIZZERIA_ID` in `PIZZERIA_LANG`.
The agent greets first and answers each turn in the language you used
(German or English). Prices and the basket total come verbatim from the
menu. End with Ctrl-D.

## Web channel

```bash
venv/bin/python -m channels.web
```

Then open <a href="http://127.0.0.1:8888" target="_blank">http://127.0.0.1:8888</a>.

- **Header:** the pizzeria you are ordering from, a selector filled live
  from `GET /pizzerias` (name + short UUID; changing it starts a fresh
  conversation — a basket never crosses a tenant boundary), a link to that
  pizzeria's dashboard, a DE/EN language switch, and "Start over".
- **Basket panel:** live from the code-owned order state — quantities,
  line totals, basket total; locked once submitted.
- **Read-back:** a visually distinct panel with an explicit confirm
  button. Confirmation is your click, tied to the exact basket revision
  that was read back.
- **Footer:** `APP_VERSION`, the full pizzeria UUID (selectable),
  connection badges for the ordering API and the model gateway, and a
  link to the API documentation.
- Every message gets an answer: intermediate tool steps stream visibly,
  and any error, timeout, or unanswered turn leaves a plain-language
  notice with a resend button.

## Voice deployment

Voice is a required capability of a production release (SPEC); text-only
is the degraded mode for dev/test and outages. To deploy voice:

1. Provision the self-hosted speech service next to the app —
   `deploy/speech-service.compose.yml` is the neutral definition; the
   image and models are operator configuration (`SPEECH_IMAGE`,
   `SPEECH_*`), never named in this repository.
2. Serve the app over **HTTPS on a real host name** (e.g. via the
   platform's proxy). Microphone capture does not exist on plain HTTP —
   the UI hides all voice controls outside a secure context.
3. Set `SPEECH_URL`, `SPEECH_STT_MODEL`, `SPEECH_TTS_MODEL`,
   `SPEECH_TTS_VOICE` on the app. STT/TTS use the session language.
   If the default voice is monolingual (e.g. a German voice), also set
   `SPEECH_TTS_MODEL_EN` + `SPEECH_TTS_VOICE_EN` (both or neither) so
   English sessions are spoken by an English voice; without the pair,
   English falls back to the default voice. If the speech service
   requires a bearer token, set `SPEECH_API_KEY` as well; unset means no
   `Authorization` header is sent.
4. Release-gating proof: run the live voice acceptance test against the
   deployment —
   `PIZZA_LIVE_VOICE=1 PIZZA_LIVE_VOICE_URL=https://<domain> venv/bin/python -m pytest tests/test_web_speech.py -k live_voice`
   (drives the real page with recorded spoken-order fixtures through
   microphone capture, real STT, the confirm control and real TTS, then
   verifies the order via the API).

## Speech (web only, optional in dev)

Set `SPEECH_URL`, `SPEECH_STT_MODEL`, `SPEECH_TTS_MODEL` and
`SPEECH_TTS_VOICE` to a self-hosted OpenAI-compatible speech service. The
mic button is push-to-talk (click to start, click to stop; recording state
is always visible); the read-aloud toggle is off by default and speaks
only final answers. STT and TTS use the session language. With
`SPEECH_URL` unset — or the service down at startup — mic and toggle are
not rendered and the page is fully usable as text chat.

Manual speech checklist: dictate an order; dictate a name that needs
correcting (the agent repeats the name back before submitting); ask a menu
question; and one run with `SPEECH_URL` unset placing an order as text.

## Tests

```bash
venv/bin/python -m pytest tests/                 # offline: no network, no LLM
PIZZA_LIVE_TEST=1 venv/bin/python -m pytest tests/test_tools.py -k live
```

The offline suite includes `tests/test_web_e2e.py`: a headless Chromium
drives the real page against a stub PizzaSim and a stub scripted gateway —
full order to submission, pizzeria switch, and three failure paths (tool
error, gateway unreachable, stream without a final answer), all asserted
against the DOM. The second command is the one opt-in live acceptance test:
it places a real order and verifies customer, items and quantities through
the pizzeria's order endpoints.

## Logs

One JSON line per event (user text, tool calls, tool results, state
transitions) in `logs/agent-<session>.jsonl`. Secrets never appear there.
