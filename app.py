"""Flask MVP for summarising clinical notes.

This app is intentionally beginner-friendly and heavily commented.
"""

from __future__ import annotations

import os
import re
from typing import Dict, List

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

# Load variables from a local .env file into environment variables.
# This lets beginners keep API keys out of source code.
load_dotenv()

app = Flask(__name__)


def _sentences(text: str) -> List[str]:
    """Split text into simple sentences for fallback summarisation."""
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]


def fallback_summarise(note_text: str) -> Dict[str, List[str] | str]:
    """Create a basic structured summary without any external API.

    This is intentionally simple so the app still works without an API key.
    """
    lines = [line.strip(" -\t") for line in note_text.splitlines() if line.strip()]
    sents = _sentences(note_text)

    summary = " ".join(sents[:2]) if sents else "No content provided."

    issue_keywords = ("pain", "fever", "bp", "blood pressure", "diagnosis", "symptom", "cough")
    action_keywords = ("start", "continue", "stop", "monitor", "refer", "prescribe", "advise")
    risk_keywords = ("risk", "allergy", "fall", "worse", "warning", "urgent", "red flag")
    followup_keywords = ("follow-up", "review", "recheck", "return", "next visit")

    def pick_lines(keywords: tuple[str, ...], default: str) -> List[str]:
        found = [l for l in lines if any(k in l.lower() for k in keywords)]
        return found[:4] if found else [default]

    return {
        "summary": summary,
        "key_issues": pick_lines(issue_keywords, "No clear issues identified in the note."),
        "actions": pick_lines(action_keywords, "No explicit actions documented."),
        "risks": pick_lines(risk_keywords, "No explicit risks documented."),
        "suggested_follow_up": pick_lines(
            followup_keywords,
            "Schedule a routine follow-up and monitor symptoms."
        ),
    }


def ai_summarise(note_text: str) -> Dict[str, List[str] | str]:
    """Use OpenAI if OPENAI_API_KEY exists; otherwise fallback to local logic."""
    api_key = os.getenv("OPENAI_API_KEY")

    # If there is no key, keep app usable by returning fallback output.
    if not api_key:
        return fallback_summarise(note_text)

    # Import here so the app can still run if openai package is missing in early setup.
    from openai import OpenAI

    client = OpenAI(api_key=api_key)

    prompt = (
        "You are helping summarise fictional clinical notes for testing software. "
        "Never include any private identifiers. Return strict JSON with keys: "
        "summary (string), key_issues (array of strings), actions (array of strings), "
        "risks (array of strings), suggested_follow_up (array of strings). "
        "Keep output concise and professional.\n\n"
        f"Clinical note:\n{note_text}"
    )

    # This uses a broadly available chat model; can be swapped in .env by editing MODEL_NAME.
    model_name = os.getenv("MODEL_NAME", "gpt-4o-mini")

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You output valid JSON only."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        response_format={"type": "json_object"},
    )

    # The model returns JSON text in message content.
    raw_json = response.choices[0].message.content

    # Use Flask's JSON loader for a small dependency footprint.
    # If parsing fails for any reason, fallback to local summariser.
    try:
        parsed = app.json.loads(raw_json)
        return {
            "summary": parsed.get("summary", ""),
            "key_issues": parsed.get("key_issues", []),
            "actions": parsed.get("actions", []),
            "risks": parsed.get("risks", []),
            "suggested_follow_up": parsed.get("suggested_follow_up", []),
        }
    except Exception:
        return fallback_summarise(note_text)


@app.route("/")
def index():
    """Serve the main page."""
    return render_template("index.html")


@app.route("/api/summarise", methods=["POST"])
def summarise():
    """Receive note text and return a structured summary as JSON."""
    payload = request.get_json(silent=True) or {}
    note_text = (payload.get("note_text") or "").strip()

    if not note_text:
        return jsonify({"error": "Please paste some clinical note text first."}), 400

    # Basic input limit to keep requests manageable.
    if len(note_text) > 12000:
        return jsonify({"error": "Please keep notes under 12,000 characters."}), 400

    result = ai_summarise(note_text)
    return jsonify(result)


if __name__ == "__main__":
    # debug=True is useful for beginners in local development only.
    app.run(debug=True)
