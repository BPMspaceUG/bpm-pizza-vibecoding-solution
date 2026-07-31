#!/usr/bin/env python3
"""FastAPI web server for PizzaSim chat with tool calling."""

import asyncio
import json
import re
import socket
import time
from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse

from agent import run_agent

# Thread pool for running sync code
executor = ThreadPoolExecutor(max_workers=10)

# Session storage with expiration
default_session = {"messages": [], "last_access": time.time()}
sessions = {}
SESSION_TIMEOUT_SECONDS = 3600  # 1 hour
MAX_SESSIONS = 10000

def get_session(sid):
    """Get or create a session with expiration check."""
    now = time.time()
    # Clean up expired sessions periodically
    if len(sessions) > MAX_SESSIONS:
        expired = [k for k, v in sessions.items() if now - v.get("last_access", 0) > SESSION_TIMEOUT_SECONDS]
        for k in expired:
            del sessions[k]

    if sid not in sessions:
        sessions[sid] = {"messages": [], "last_access": now}
    sessions[sid]["last_access"] = now
    return sessions[sid]

def validate_session_id(sid):
    """Validate session ID format to prevent injection."""
    if not isinstance(sid, str):
        return False
    # Allow alphanumeric, hyphens, underscores only
    return bool(re.match(r'^[a-zA-Z0-9_-]{1,64}$', sid))

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{pizzeria_name}} - PizzaSim Chat</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }
        .header {
            background: #1a1a1a;
            color: white;
            padding: 1rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            flex-wrap: wrap;
        }
        .header-left {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        .header h1 { font-size: 1.25rem; font-weight: 600; }
        .header-center { display: flex; gap: 0.75rem; align-items: center; }
        .pizzeria-select {
            background: #333;
            color: white;
            border: 1px solid #555;
            padding: 0.4rem 0.6rem;
            border-radius: 6px;
            font-size: 0.9rem;
            cursor: pointer;
            min-width: 200px;
        }
        .header-right {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        .reset-btn {
            background: #dc3545;
            color: white;
            border: none;
            padding: 0.4rem 0.75rem;
            border-radius: 6px;
            font-size: 0.85rem;
            cursor: pointer;
            transition: all 0.2s;
        }
        .reset-btn:hover { background: #c82333; }
        .lang-select {
            background: #333;
            color: white;
            border: 1px solid #555;
            padding: 0.4rem 0.6rem;
            border-radius: 6px;
            font-size: 0.9rem;
            cursor: pointer;
        }
        .toggle-btn {
            background: #333;
            color: #aaa;
            border: 1px solid #555;
            padding: 0.4rem 0.75rem;
            border-radius: 6px;
            font-size: 0.85rem;
            cursor: pointer;
            transition: all 0.2s;
        }
        .toggle-btn.active {
            background: #2d5a3d;
            color: #90d4a3;
            border-color: #4a9c5e;
        }
        .chat-container {
            flex: 1;
            overflow-y: auto;
            padding: 1rem;
            max-width: 800px;
            width: 100%;
            margin: 0 auto;
        }
        .message {
            margin-bottom: 1rem;
            display: flex;
            gap: 0.75rem;
            animation: fadeIn 0.3s ease;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .message.user { flex-direction: row-reverse; }
        .avatar {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.85rem;
            flex-shrink: 0;
        }
        .message.assistant .avatar { background: #10a37f; color: white; }
        .message.user .avatar { background: #5436da; color: white; }
        .bubble {
            background: white;
            padding: 0.75rem 1rem;
            border-radius: 12px;
            max-width: 70%;
            box-shadow: 0 1px 2px rgba(0,0,0,0.1);
            line-height: 1.5;
        }
        .message.user .bubble {
            background: #5436da;
            color: white;
        }
        .input-area {
            background: white;
            border-top: 1px solid #e0e0e0;
            padding: 1rem;
        }
        .input-container {
            max-width: 800px;
            margin: 0 auto;
            display: flex;
            gap: 0.5rem;
            align-items: flex-end;
        }
        .mic-btn {
            background: #f0f0f0;
            border: none;
            width: 44px;
            height: 44px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-size: 1.2rem;
            transition: all 0.2s;
        }
        .mic-btn:hover { background: #e0e0e0; }
        .mic-btn.recording {
            background: #dc3545;
            color: white;
            animation: pulse 1s infinite;
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
        .mic-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        textarea {
            flex: 1;
            border: 1px solid #d0d0d0;
            border-radius: 20px;
            padding: 0.75rem 1rem;
            font-size: 1rem;
            resize: none;
            min-height: 44px;
            max-height: 120px;
            font-family: inherit;
        }
        textarea:focus {
            outline: none;
            border-color: #10a37f;
        }
        .send-btn {
            background: #10a37f;
            color: white;
            border: none;
            width: 44px;
            height: 44px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-size: 1.1rem;
        }
        .send-btn:hover { background: #0d8c6a; }
        .send-btn:disabled { background: #ccc; cursor: not-allowed; }
        .typing {
            font-style: italic;
            color: #666;
        }
        .footer {
            background: #1a1a1a;
            color: #888;
            padding: 0.5rem 1rem;
            font-size: 0.75rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .footer-left { display: flex; gap: 0.75rem; align-items: center; }
        .version-badge {
            background: #10a37f;
            color: white;
            padding: 0.15rem 0.4rem;
            border-radius: 4px;
            font-weight: 600;
            font-size: 0.7rem;
        }
        .footer-right { display: flex; gap: 0.75rem; }
        .footer a { color: #10a37f; text-decoration: none; }
        .footer a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-left">
            <h1>🍕 {{pizzeria_name}}</h1>
        </div>
        <div class="header-center">
            <select class="pizzeria-select" id="pizzeriaSelect">
                <option value="/">🍕 PizzaSim</option>
                <option value="/leonardo">🍕 Pizzeria Leonardo</option>
                <option value="/giovanni">🍕 Pizzeria Giovanni</option>
                <option value="/marco">🍕 Pizzeria Marco</option>
                <option value="/antonio">🍕 Pizzeria Antonio</option>
            </select>
        </div>
        <div class="header-right">
            <button class="reset-btn" id="resetBtn" title="Neue Session starten (bei Problemen)">🔄 Reset</button>
            <select class="lang-select" id="langSelect">
                <option value="en-US">🇺🇸 English</option>
                <option value="de-DE" selected>🇩🇪 Deutsch</option>
            </select>
            <button class="toggle-btn" id="ttsToggle">🔊 Off</button>
        </div>
    </div>

    <div class="chat-container" id="chatContainer">
        <div class="message assistant">
            <div class="avatar">AI</div>
            <div class="bubble" id="welcomeMessage">{{welcome_message}}</div>
        </div>
    </div>

    <div class="input-area">
        <div class="input-container">
            <button class="mic-btn" id="micBtn" title="Spracheingabe">🎤</button>
            <textarea id="messageInput" placeholder="{{placeholder}}" rows="1"></textarea>
            <button class="send-btn" id="sendBtn">➤</button>
        </div>
    </div>

    <div class="footer">
        <div class="footer-left">
            <span>🍕 PizzaSim Chat</span>
            <span class="version-badge" id="versionBadge">v1.2</span>
            <span id="footerStatus" style="color: #4a9c5e;">● Online</span>
        </div>
        <div class="footer-right">
            <a href="https://www.aipizzasim.com/swagger.html" target="_blank">API Docs</a>
            <span id="footerLang">🇩🇪 Deutsch</span>
        </div>
    </div>

    <script>
        const CONFIG = {
            pizzeria: "{{pizzeria_name}}",
            lang: "{{lang}}",
            pizzeriaPath: "{{pizzeria_path}}"
        };

        const chatContainer = document.getElementById('chatContainer');
        const messageInput = document.getElementById('messageInput');
        const sendBtn = document.getElementById('sendBtn');
        const micBtn = document.getElementById('micBtn');
        const langSelect = document.getElementById('langSelect');
        const ttsToggle = document.getElementById('ttsToggle');
        const pizzeriaSelect = document.getElementById('pizzeriaSelect');

        let sessionId = localStorage.getItem('pizzasim_session_' + CONFIG.pizzeriaPath) || Date.now().toString(36);
        localStorage.setItem('pizzasim_session_' + CONFIG.pizzeriaPath, sessionId);
        let isRecording = false;
        let recognition = null;
        let ttsEnabled = localStorage.getItem('tts_enabled') === 'true';

        const TRANSLATIONS = {
            'de-DE': { thinking: 'Denke nach...', error: 'Fehler: ', you: 'Du', ai: 'KI' },
            'en-US': { thinking: 'Thinking...', error: 'Error: ', you: 'You', ai: 'AI' }
        };

        function t(key) {
            return (TRANSLATIONS[langSelect.value] || TRANSLATIONS['de-DE'])[key];
        }

        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        function addMessage(role, content, isHtml=false) {
            const msg = document.createElement('div');
            msg.className = `message ${role}`;
            msg.innerHTML = `<div class="avatar">${t(role === 'user' ? 'you' : 'ai')}</div><div class="bubble">${isHtml ? content : escapeHtml(content)}</div>`;
            chatContainer.appendChild(msg);
            chatContainer.scrollTop = chatContainer.scrollHeight;
            return msg;
        }

        async function sendMessage() {
            const text = messageInput.value.trim();
            if (!text) return;

            addMessage('user', text);
            messageInput.value = '';
            messageInput.style.height = 'auto';
            sendBtn.disabled = true;

            const thinking = addMessage('assistant', t('thinking'));
            thinking.querySelector('.bubble').className = 'bubble typing';

            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ session_id: sessionId, message: text, lang: langSelect.value })
                });

                if (!response.ok) throw new Error('HTTP ' + response.status);

                thinking.remove();
                const assistantMsg = document.createElement('div');
                assistantMsg.className = 'message assistant';
                assistantMsg.innerHTML = `<div class="avatar">${t('ai')}</div><div class="bubble"></div>`;
                const bubble = assistantMsg.querySelector('.bubble');
                chatContainer.appendChild(assistantMsg);

                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                let fullResponse = '';

                while (true) {
                    const { done, value } = await reader.read();
                    if (done) break;
                    const lines = decoder.decode(value).split('\\n');
                    for (const line of lines) {
                        if (!line.trim()) continue;
                        try {
                            const event = JSON.parse(line);
                            if (event.step === 'final' && event.content) {
                                fullResponse = event.content;
                                bubble.textContent = fullResponse;
                                chatContainer.scrollTop = chatContainer.scrollHeight;
                                if (ttsEnabled && 'speechSynthesis' in window) {
                                    const u = new SpeechSynthesisUtterance(event.content);
                                    u.lang = langSelect.value;
                                    window.speechSynthesis.speak(u);
                                }
                            }
                        } catch (e) {
                            console.error('JSON parse error:', e, 'Line:', line);
                        }
                    }
                }
            } catch (err) {
                thinking.remove();
                addMessage('assistant', t('error') + err.message);
            } finally {
                sendBtn.disabled = false;
            }
        }

        function initSpeech() {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            if (!SpeechRecognition) { micBtn.style.display = 'none'; return; }
            recognition = new SpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = true;
            recognition.onstart = () => { isRecording = true; micBtn.classList.add('recording'); };
            recognition.onend = () => { isRecording = false; micBtn.classList.remove('recording'); };
            recognition.onresult = (e) => {
                let transcript = '';
                for (let i = e.resultIndex; i < e.results.length; i++) transcript += e.results[i][0].transcript;
                messageInput.value = transcript;
                messageInput.style.height = Math.min(messageInput.scrollHeight, 120) + 'px';
                if (e.results[0].isFinal) sendMessage();
            };
            recognition.onerror = () => { isRecording = false; micBtn.classList.remove('recording'); };
        }

        sendBtn.addEventListener('click', sendMessage);
        messageInput.addEventListener('keydown', (e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); } });
        messageInput.addEventListener('input', () => { messageInput.style.height = 'auto'; messageInput.style.height = Math.min(messageInput.scrollHeight, 120) + 'px'; });
        micBtn.addEventListener('click', () => { if (!recognition) initSpeech(); if (!recognition) return; if (isRecording) recognition.stop(); else { recognition.lang = langSelect.value; recognition.start(); } });
        langSelect.addEventListener('change', () => {
    localStorage.setItem('preferred_lang', langSelect.value);
    localStorage.removeItem('pizzasim_session_' + CONFIG.pizzeriaPath);
    location.reload();
});
        ttsToggle.addEventListener('click', () => { ttsEnabled = !ttsEnabled; localStorage.setItem('tts_enabled', ttsEnabled); ttsToggle.textContent = ttsEnabled ? '🔊 On' : '🔊 Off'; ttsToggle.classList.toggle('active', ttsEnabled); });

        pizzeriaSelect.addEventListener('change', () => {
            if (pizzeriaSelect.value !== CONFIG.pizzeriaPath) {
                localStorage.removeItem('pizzasim_session_' + CONFIG.pizzeriaPath);
                location.href = pizzeriaSelect.value;
            }
        });

        document.getElementById('resetBtn').addEventListener('click', () => {
            localStorage.removeItem('pizzasim_session_' + CONFIG.pizzeriaPath);
            location.reload();
        });

        // Footer language & version display
        const footerLang = document.getElementById('footerLang');
        if (footerLang) {
            footerLang.textContent = CONFIG.lang === 'de-DE' ? '🇩🇪 Deutsch' : '🇺🇸 English';
        }

        ttsToggle.textContent = ttsEnabled ? '🔊 On' : '🔊 Off';
        ttsToggle.classList.toggle('active', ttsEnabled);
        if (pizzeriaSelect) pizzeriaSelect.value = CONFIG.pizzeriaPath;
        initSpeech();
    </script>
</body>
</html>
'''

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS: only allow specific origins, not wildcard with credentials
ALLOWED_ORIGINS = [
    "http://localhost:8888",
    "http://127.0.0.1:8888",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

PIZZERIAS = {
    '/': ('PizzaSim', '86517183-e1a5-4bd7-b915-e0db8f8b2131'),
    '/leonardo': ('Pizzeria Leonardo', 'leonardo-uuid-123'),
    '/giovanni': ('Pizzeria Giovanni', 'giovanni-uuid-456'),
    '/marco': ('Pizzeria Marco', 'marco-uuid-789'),
    '/antonio': ('Pizzeria Antonio', 'antonio-uuid-abc')
}

def render_html(pizzeria_path='/', lang='de-DE'):
    pizzeria_data = PIZZERIAS.get(pizzeria_path, ('PizzaSim', '86517183-e1a5-4bd7-b915-e0db8f8b2131'))
    name = pizzeria_data[0]
    pizzeria_id = pizzeria_data[1]
    welcome = f'Willkommen bei {name}! Ich kann dir helfen, das Menü zu erkunden. Was möchtest du wissen?' if lang == 'de-DE' else f'Welcome to {name}! I can help you explore the menu. What would you like to know?'
    placeholder = 'Nachricht schreiben...' if lang == 'de-DE' else 'Type a message...'
    html = HTML_TEMPLATE.replace('{{pizzeria_name}}', name).replace('{{pizzeria_id}}', pizzeria_id).replace('{{pizzeria_path}}', pizzeria_path).replace('{{lang}}', lang).replace('{{welcome_message}}', welcome).replace('{{placeholder}}', placeholder)
    return HTMLResponse(content=html)

def get_pid_from_path(path):
    pizzeria_data = PIZZERIAS.get(path, ('PizzaSim', '86517183-e1a5-4bd7-b915-e0db8f8b2131'))
    return pizzeria_data[1]

@app.post("/api/chat")
async def chat_root(request: Request):
    data = await request.json()
    sid = data.get("session_id")
    msg = data.get("message")
    lang = data.get("lang", "de-DE")

    # Validate session_id
    if not sid or not validate_session_id(sid):
        raise HTTPException(status_code=400, detail="Invalid or missing session_id")
    # Validate message is a string
    if not msg or not isinstance(msg, str):
        raise HTTPException(status_code=400, detail="Invalid or missing message")
    # Enforce message size limit
    if len(msg) > 10000:
        raise HTTPException(status_code=400, detail="Message too long (max 10000 chars)")

    session = get_session(sid)
    msgs = session["messages"]
    pid = get_pid_from_path('/')

    async def gen():
        # Run sync generator in threadpool to avoid blocking event loop
        try:
            async for ev in run_in_threadpool(lambda: iter(run_agent(msg, msgs, pid=pid, lang=lang))):
                yield json.dumps(ev) + "\n"
        except Exception as e:
            yield json.dumps({"step": "error", "content": str(e)}) + "\n"
        finally:
            session["messages"] = msgs

    return StreamingResponse(gen(), media_type="application/x-ndjson")

@app.post("/{pizzeria}/api/chat")
async def chat_pizzeria(pizzeria: str, request: Request):
    data = await request.json()
    sid = data.get("session_id")
    msg = data.get("message")
    lang = data.get("lang", "de-DE")

    # Validate session_id
    if not sid or not validate_session_id(sid):
        raise HTTPException(status_code=400, detail="Invalid or missing session_id")
    # Validate message is a string
    if not msg or not isinstance(msg, str):
        raise HTTPException(status_code=400, detail="Invalid or missing message")
    # Enforce message size limit
    if len(msg) > 10000:
        raise HTTPException(status_code=400, detail="Message too long (max 10000 chars)")

    session = get_session(sid)
    msgs = session["messages"]
    pid = get_pid_from_path(f'/{pizzeria}')

    async def gen():
        # Run sync generator in threadpool to avoid blocking event loop
        try:
            async for ev in run_in_threadpool(lambda: iter(run_agent(msg, msgs, pid=pid, lang=lang))):
                yield json.dumps(ev) + "\n"
        except Exception as e:
            yield json.dumps({"step": "error", "content": str(e)}) + "\n"
        finally:
            session["messages"] = msgs

    return StreamingResponse(gen(), media_type="application/x-ndjson")

@app.get("/")
async def index_root(request: Request):
    return render_html('/', request.query_params.get('lang', 'de-DE'))

@app.get("/{pizzeria}")
async def index_pizzeria(pizzeria: str, request: Request):
    path = f'/{pizzeria}'
    if path not in PIZZERIAS:
        path = '/'
    return render_html(path, request.query_params.get('lang', 'de-DE'))

def get_free_port(preferred=8888):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("127.0.0.1", preferred))
            s.listen(1)
            return s.getsockname()[1]
        except OSError:
            s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s2.bind(("127.0.0.1", 0))
            s2.listen(1)
            port = s2.getsockname()[1]
            s2.close()
            return port

if __name__ == "__main__":
    import uvicorn
    PORT = 8888
    print(f"🍕 PizzaSim: http://127.0.0.1:{PORT}")
    print(f"   Leonardo: http://127.0.0.1:{PORT}/leonardo")
    print(f"   Giovanni: http://127.0.0.1:{PORT}/giovanni")
    uvicorn.run(app, host="127.0.0.1", port=PORT, log_level="warning")
