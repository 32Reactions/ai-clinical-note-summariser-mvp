# Clinical Note Summariser (Beginner MVP)

A simple Flask web app that summarises **fictional** clinical notes into a structured output:

- Summary
- Key Issues
- Actions
- Risks
- Suggested Follow-up

## Important safety note

This project includes only **fake sample notes** for testing.
Do not paste real patient data or personally identifiable health information.

## Tech stack

- Backend: Python + Flask
- Frontend: HTML/CSS/JavaScript
- Optional AI: OpenAI API key via environment variable

## Project structure

- `app.py` - Flask backend and summarisation logic
- `templates/index.html` - UI page
- `static/styles.css` - app styles
- `static/app.js` - frontend logic
- `samples/fake_clinical_notes.txt` - test notes
- `.env.example` - environment variable template
- `requirements.txt` - Python dependencies

## Setup (VS Code, local run)

1. Open this folder in VS Code.
2. Open a terminal in VS Code.
3. Create a virtual environment:

```bash
python3 -m venv .venv
```

4. Activate it:

```bash
source .venv/bin/activate
```

5. Install dependencies:

```bash
pip install -r requirements.txt
```

6. Create your env file:

```bash
cp .env.example .env
```

7. (Optional) Add your `OPENAI_API_KEY` inside `.env`.

If no key is set, the app still works using a simple local fallback summariser.

8. Run the app:

```bash
python app.py
```

9. Open your browser to:

- http://127.0.0.1:5000

## How to test quickly

- Click `Load fake sample`
- Or copy a note from `samples/fake_clinical_notes.txt`
- Click `Summarise`

## Screenshot

After running the app, you can take a screenshot and save it at:

- `docs/app-screenshot.png`

Then this README image link will display it:

![App Screenshot](docs/app-screenshot.png)

Quick macOS capture command:

```bash
mkdir -p docs
screencapture -i docs/app-screenshot.png
```

## Notes for beginners

- Backend route: `POST /api/summarise`
- Frontend sends note text as JSON:

```json
{ "note_text": "..." }
```

- Backend returns JSON with the 5 sections used by the UI.
