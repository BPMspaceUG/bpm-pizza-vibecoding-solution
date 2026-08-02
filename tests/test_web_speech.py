"""Voice wiring, fully offline: the app boots against a stub speech
service; a headless Chromium with a fake microphone (streaming the real
audio fixture) exercises the genuine push-to-talk path. Asserts wiring —
control visibility, STT round trip, spoken-turn metadata, final-message
TTS, runtime degradation, secure-context gating — never speech quality.

Runs after tests/test_web_e2e.py (module order matters: this module
re-boots the shared app with SPEECH_* configured)."""
from __future__ import annotations

import os
from pathlib import Path

import httpx
import pytest

from tests.stubs import StubGateway, StubPizzaSim, StubSpeech, run_server

PZ1 = "11111111-aaaa-bbbb-cccc-000000000001"
AUDIO = Path(__file__).parent / "fixtures" / "audio"


@pytest.fixture(scope="module")
def stack():
    pizzasim = StubPizzaSim()
    gateway = StubGateway()
    speech = StubSpeech()
    ps_server, ps_url = run_server(pizzasim.app)
    gw_server, gw_url = run_server(gateway.app)
    sp_server, sp_url = run_server(speech.app)
    os.environ.update({
        "PIZZASIM_URL": ps_url,
        "PIZZASIM_API_KEY": "stub-key",
        "PIZZERIA_ID": PZ1,
        "PIZZERIA_LANG": "de",
        "LITELLM_PIZZA_URL": gw_url,
        "LITELLM_PIZZA_KEY": "stub-key",
        "LITELLM_PIZZA_MODEL_1": "scripted-stub",
        "APP_VERSION": "2.0.0",
        "SPEECH_URL": sp_url,
        "SPEECH_STT_MODEL": "stub-stt",
        "SPEECH_TTS_MODEL": "stub-tts",
        "SPEECH_TTS_VOICE": "stub-voice",
    })
    from channels import web  # boots (again) against the speech-enabled env
    app_server, app_url = run_server(web.app)
    yield {"pizzasim": pizzasim, "gateway": gateway, "speech": speech,
           "url": app_url, "web": web}
    for server in (app_server, ps_server, gw_server, sp_server):
        server.should_exit = True
    for var in ("SPEECH_URL", "SPEECH_STT_MODEL", "SPEECH_TTS_MODEL",
                "SPEECH_TTS_VOICE"):
        os.environ.pop(var, None)


@pytest.fixture()
def api(stack):
    with httpx.Client(base_url=stack["url"], timeout=30.0) as client:
        yield client


# --- API surface -----------------------------------------------------------

def test_config_reports_speech_enabled(api):
    assert api.get("/config").json()["speech"] is True


def test_stt_round_trip_uses_session_language(stack, api):
    sid = api.post("/session", json={}).json()["session_id"]
    audio = (AUDIO / "order.de.wav").read_bytes()
    result = api.post(f"/speech/stt?session_id={sid}",
                      files={"audio": ("order.de.wav", audio, "audio/wav")})
    assert result.json() == {"text": "Zwei Margherita bitte"}
    assert stack["speech"].languages[-1] == "de"
    api.post("/language", json={"session_id": sid, "lang": "en"})
    api.post(f"/speech/stt?session_id={sid}",
             files={"audio": ("order.en.wav",
                              (AUDIO / "order.en.wav").read_bytes(),
                              "audio/wav")})
    assert stack["speech"].languages[-1] == "en"


def test_tts_returns_playable_audio(stack, api):
    sid = api.post("/session", json={}).json()["session_id"]
    before = stack["speech"].tts_calls
    result = api.post("/speech/tts", json={"session_id": sid,
                                           "text": "Hallo"})
    assert result.status_code == 200
    assert result.headers["content-type"].startswith("audio/")
    assert result.content[:4] == b"RIFF"  # a real, playable WAV container
    assert stack["speech"].tts_calls == before + 1


def test_speech_failure_maps_to_502(stack, api):
    sid = api.post("/session", json={}).json()["session_id"]
    stack["speech"].mode = "fail"
    try:
        result = api.post("/speech/tts", json={"session_id": sid,
                                               "text": "x"})
        assert result.status_code == 502
    finally:
        stack["speech"].mode = "ok"


def test_stt_unknown_session_404(api):
    assert api.post("/speech/stt?session_id=ghost",
                    files={"audio": ("a.wav", b"x",
                                     "audio/wav")}).status_code == 404


# --- browser E2E: the real push-to-talk path -------------------------------

@pytest.fixture(scope="module")
def voice_page_factory(stack):
    """Firefox with fake media streams: headless Chromium exposes no audio
    device on this host even with --use-fake-device-for-media-capture
    (verified), while Firefox's fake-stream pref needs no audio backend.
    Spec-aligned: the product must work cross-browser, and the offline
    wiring tests don't care about audio content (the stub returns a fixed
    transcript). The recorded WAV fixtures drive the LIVE voice test via
    Chromium's --use-file-for-fake-audio-capture on the voice deployment."""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.firefox.launch(firefox_user_prefs={
            "media.navigator.streams.fake": True,
            "media.navigator.permission.disabled": True,
        })
        context = browser.new_context()
        yield context.new_page
        browser.close()


def open_app(new_page, stack, init_script=None):
    page = new_page()
    if init_script:
        page.add_init_script(init_script)
    page.goto(stack["url"], timeout=30000)
    page.wait_for_selector(".msg.assistant", timeout=30000)
    return page


def test_e2e_voice_push_to_talk_round_trip(voice_page_factory, stack):
    stack["gateway"].mode = "ok"
    stack["gateway"].saw_spoken_note = False
    page = open_app(voice_page_factory, stack)
    # controls visible on a secure context with speech configured
    assert page.locator("#mic").is_visible()
    assert page.locator("#tts-toggle").is_visible()
    # off by default
    assert page.locator("#tts-toggle").get_attribute("aria-pressed") == "false"

    page.click("#mic")  # push-to-talk: start
    page.wait_for_selector("#mic.recording", timeout=10000)  # visible state
    page.wait_for_timeout(1200)
    page.click("#mic")  # stop → upload → stub transcript drives the turn
    page.wait_for_selector("text=Zwei Margherita bitte", timeout=30000)
    page.wait_for_selector("#basket-lines li", timeout=30000)
    assert "2× Margherita" in page.locator("#basket-lines").inner_text()
    assert stack["gateway"].saw_spoken_note  # spoken-style note reached model
    page.close()


def test_e2e_tts_fetched_once_for_final_message_only(voice_page_factory,
                                                     stack):
    stack["gateway"].mode = "ok"
    page = open_app(voice_page_factory, stack)
    page.click("#tts-toggle")
    assert page.locator("#tts-toggle").get_attribute("aria-pressed") == "true"
    assert page.locator("#tts-toggle").inner_text().strip() == "🔊"
    before = stack["speech"].tts_calls
    page.fill("#text", "Was kostet eine Margherita?")
    page.click("#send")
    page.wait_for_selector("text=8.5 €", timeout=30000)
    page.wait_for_function(
        f"() => fetch('/config').then(() => true) && true", timeout=5000)
    page.wait_for_timeout(800)  # allow the TTS fetch to complete
    # the turn contained a tool step AND a final message → exactly one TTS
    assert stack["speech"].tts_calls == before + 1

    # off-path: toggling back off must stop read-aloud — the stub's call
    # counter is the oracle, not the button's own state.
    page.click("#tts-toggle")
    assert page.locator("#tts-toggle").get_attribute("aria-pressed") == "false"
    assert page.locator("#tts-toggle").inner_text().strip() == "🔇"
    page.fill("#text", "Zwei Margherita bitte")
    page.click("#send")
    page.wait_for_selector("text=Wie ist Ihr Vorname?", timeout=30000)
    page.wait_for_timeout(800)  # a TTS fetch would have landed by now
    assert stack["speech"].tts_calls == before + 1
    page.close()


def test_e2e_tts_toggle_header_placement_and_i18n(voice_page_factory, stack):
    stack["gateway"].mode = "ok"
    page = open_app(voice_page_factory, stack)
    assert page.eval_on_selector(
        "#tts-toggle",
        "el => [el.closest('header') !== null, el.previousElementSibling.id,"
        " el.nextElementSibling.id]") == [True, "lang-switch", "start-over"]
    toggle = page.locator("#tts-toggle")
    assert toggle.get_attribute("title") == "Antworten vorlesen"
    assert toggle.get_attribute("aria-label") == "Antworten vorlesen"
    page.click("#lang-switch button[data-lang=en]")
    assert toggle.get_attribute("title") == "Read replies aloud"
    assert toggle.get_attribute("aria-label") == "Read replies aloud"
    assert toggle.get_attribute("aria-pressed") == "false"  # i18n ≠ state
    page.close()


def test_e2e_tts_toggle_keyboard_accessible(voice_page_factory, stack):
    stack["gateway"].mode = "ok"
    page = open_app(voice_page_factory, stack)
    page.focus("#tts-toggle")
    assert page.evaluate("() => document.activeElement.id") == "tts-toggle"
    page.keyboard.press("Space")
    assert page.locator("#tts-toggle").get_attribute("aria-pressed") == "true"
    page.keyboard.press("Enter")
    assert page.locator("#tts-toggle").get_attribute("aria-pressed") == "false"
    page.close()


def test_e2e_runtime_speech_outage_degrades_to_text(voice_page_factory,
                                                    stack):
    stack["gateway"].mode = "ok"
    page = open_app(voice_page_factory, stack)
    stack["speech"].mode = "fail"
    try:
        page.click("#mic")
        page.wait_for_selector("#mic.recording", timeout=10000)
        page.wait_for_timeout(900)
        page.click("#mic")  # upload fails → degrade
        page.wait_for_selector(".notice", timeout=30000)
        page.wait_for_selector("#mic", state="hidden", timeout=10000)
        assert page.locator("#tts-toggle").is_hidden()
        # typed ordering continues untouched
        page.fill("#text", "Zwei Margherita bitte")
        page.click("#send")
        page.wait_for_selector("#basket-lines li", timeout=30000)
    finally:
        stack["speech"].mode = "ok"
    page.close()


# --- live voice acceptance (opt-in, release-gating per SPEC) ---------------

LIVE_VOICE = (os.environ.get("PIZZA_LIVE_VOICE") == "1"
              and bool(os.environ.get("PIZZA_LIVE_VOICE_URL")))


@pytest.mark.skipif(not LIVE_VOICE,
                    reason="live voice test only with PIZZA_LIVE_VOICE=1 "
                           "and PIZZA_LIVE_VOICE_URL=<https deployment>")
@pytest.mark.parametrize("lang,fixture,name_reply,yes", [
    ("de", "order.de.wav", "Ich heiße VoiceTest", "Ja"),
    ("en", "order.en.wav", "My name is VoiceTest", "Yes"),
])
def test_live_voice_acceptance(lang, fixture, name_reply, yes):
    """The voice agent actually works: real browser over HTTPS, real
    microphone capture (fake device streaming the spoken-order fixture),
    real STT, the confirm control, real TTS — then the order is verified
    via the pizzeria's API endpoints. Not a text replay: if STT does not
    produce an order-driving transcript, this test fails."""
    from playwright.sync_api import sync_playwright

    from core.pizzasim import PizzaSim

    base_url = os.environ["PIZZA_LIVE_VOICE_URL"]
    wav = str((AUDIO / fixture).resolve())
    tts_audio = {"bytes": 0}

    with sync_playwright() as p:
        browser = p.chromium.launch(args=[
            "--use-fake-device-for-media-capture",
            "--use-fake-ui-for-media-capture",
            f"--use-file-for-fake-audio-capture={wav}",
        ])
        context = browser.new_context()
        context.grant_permissions(["microphone"], origin=base_url)
        page = context.new_page()

        def sniff(response):
            if response.url.endswith("/speech/tts") and response.ok:
                tts_audio["bytes"] = len(response.body())
        page.on("response", sniff)

        page.goto(base_url, timeout=60000)
        page.wait_for_selector(".msg.assistant", timeout=120000)
        if lang == "en":
            page.locator("#lang-switch button[data-lang=en]").click()
        assert page.locator("#mic").is_visible()  # HTTPS + speech up
        page.click("#tts-toggle")

        page.click("#mic")
        page.wait_for_selector("#mic.recording", timeout=15000)
        page.wait_for_timeout(7000)  # the fixture is ~5.5s of speech
        page.click("#mic")
        # STT must yield an order-driving transcript: the basket fills.
        page.wait_for_selector("#basket-lines li", timeout=120000)

        page.fill("#text", name_reply)
        page.click("#send")
        page.wait_for_selector(".readback button:enabled", timeout=120000)
        page.locator(".readback button:enabled").click()
        page.wait_for_selector("#submitted-banner:not([hidden])",
                               timeout=120000)
        page.wait_for_timeout(2000)  # allow the final TTS fetch
        assert tts_audio["bytes"] > 0  # real, non-empty playable audio
        pizzeria_id = page.locator("#uuid").inner_text().strip()
        banner = page.locator("#submitted-banner").inner_text()
        order_id = banner.split()[-1]
        browser.close()

    # verify via the API: right customer, items present, right tenant
    client = PizzaSim.from_env().for_pizzeria(pizzeria_id)
    listed = {o["id"] for o in client.list_orders()}
    assert order_id in listed
    detail = client.get_order(order_id)
    assert detail["customer"]["first_name"] == "VoiceTest"
    assert detail["items"], "order carries no items"


def test_e2e_insecure_context_renders_no_voice_ui(voice_page_factory,
                                                  stack):
    """Plain HTTP never presents a voice-capable UI — even with speech
    fully configured server-side."""
    stack["gateway"].mode = "ok"
    page = open_app(
        voice_page_factory, stack,
        init_script="Object.defineProperty(window, 'isSecureContext',"
                    " {value: false});")
    assert page.locator("#mic").is_hidden()
    assert page.locator("#tts-toggle").is_hidden()
    page.fill("#text", "Zwei Margherita bitte")  # text ordering works
    page.click("#send")
    page.wait_for_selector("#basket-lines li", timeout=30000)
    page.close()


# --- per-language TTS voice (issue #11) ------------------------------------
# Order matters: the fallback cases run against the base stack FIRST; the
# EN stack then re-boots the shared app object with the EN pair configured
# (replacing app.state for every earlier server), so it comes last.

def _tts(url, speech, lang):
    """One TTS request in a fresh session of the given language; returns
    the (model, voice) pair the stub recorded for it."""
    with httpx.Client(base_url=url, timeout=30.0) as client:
        sid = client.post("/session", json={}).json()["session_id"]
        if lang != "de":
            client.post("/language", json={"session_id": sid, "lang": lang})
        assert client.post("/speech/tts", json={
            "session_id": sid, "text": "Hallo"}).status_code == 200
    return speech.tts_requests[-1]


def test_tts_en_session_without_en_pair_falls_back(stack):
    # The base stack booted without the EN vars: today's behavior, kept.
    assert _tts(stack["url"], stack["speech"], "en") == \
        ("stub-tts", "stub-voice")


def test_tts_half_configured_en_pair_falls_back(stack):
    # ponytail: both-or-neither via a spot re-instantiation of the service
    # (a fourth full app boot would fight the shared app.state for one env
    # permutation; the service object is the unit that owns the rule).
    os.environ["SPEECH_TTS_MODEL_EN"] = "stub-tts-en"
    try:
        from channels.speech import SpeechService
        service = SpeechService()
        service.tts("Hallo", "en")
    finally:
        os.environ.pop("SPEECH_TTS_MODEL_EN", None)
    assert stack["speech"].tts_requests[-1] == ("stub-tts", "stub-voice")


@pytest.fixture(scope="module")
def stack_en(stack):
    os.environ.update({
        "SPEECH_TTS_MODEL_EN": "stub-tts-en",
        "SPEECH_TTS_VOICE_EN": "stub-voice-en",
    })
    from channels import web
    server, url = run_server(web.app)  # re-boots with the EN pair present
    yield {"speech": stack["speech"], "url": url}
    server.should_exit = True
    for var in ("SPEECH_TTS_MODEL_EN", "SPEECH_TTS_VOICE_EN"):
        os.environ.pop(var, None)


def test_tts_en_session_uses_en_pair(stack_en):
    assert _tts(stack_en["url"], stack_en["speech"], "en") == \
        ("stub-tts-en", "stub-voice-en")


def test_tts_de_session_keeps_default_pair(stack_en):
    assert _tts(stack_en["url"], stack_en["speech"], "de") == \
        ("stub-tts", "stub-voice")
