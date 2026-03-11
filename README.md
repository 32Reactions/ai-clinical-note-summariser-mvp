⚠️ This project uses synthetic clinical notes only and does not process real patient data.

# Clinical Note Summariser (AI MVP)

## Overview

This project is a simple AI-assisted tool for summarising clinical notes into structured outputs.

The goal of the project was to explore how AI could reduce cognitive load when reviewing long clinical notes by automatically structuring key information such as:

- Summary
- Key Issues
- Actions
- Risks
- Suggested Follow-up

This project was built as a beginner MVP to demonstrate product thinking and rapid prototyping, rather than a production healthcare system.

---

# Problem

Clinical notes and meeting summaries can often be:

- long
- inconsistent in structure
- difficult to scan quickly

Clinicians, coordinators and administrators frequently need to extract the key points quickly, especially when reviewing multiple notes or preparing follow-up actions.

This creates a simple question:

Can AI help turn unstructured notes into structured summaries to support faster review?

---

# Target Users

Potential users of this workflow could include:

- Clinicians reviewing patient notes
- MDT coordinators preparing summaries
- Administrators reviewing clinical documentation
- Analysts reviewing large volumes of notes

The common need across these users is:

Quickly identifying the most important information from unstructured text.

---

# Product Hypothesis

If clinical notes can be automatically structured into consistent sections, users may be able to:

- review notes faster
- identify key issues more easily
- reduce cognitive load when scanning documentation

This MVP explores whether a simple AI summarisation interface could support that workflow.

---

# MVP Scope

To keep the project intentionally simple, the MVP includes only:

### Included

- Paste clinical note text into a textbox
- Click **Summarise**
- Generate structured output with:
  - Summary
  - Key Issues
  - Actions
  - Risks
  - Suggested Follow-up

### Excluded (future scope)

- Speech-to-text transcription
- Integration with Electronic Patient Records
- File uploads
- Authentication
- Secure storage
- Clinical safety validation

---

# Solution

The MVP provides a minimal interface where a user can:

1. Paste a block of clinical text
2. Click **Summarise**
3. Receive a structured output organised into consistent sections

This structure was chosen because it mirrors how clinicians often review documentation:

- What happened?
- What are the key issues?
- What actions are required?
- What risks exist?
- What should happen next?

---

## System Flow

The diagram below shows how the application processes a clinical note.

```mermaid
flowchart LR

A[User pastes clinical note] --> B[Frontend UI<br>HTML / JS]
B --> C[Flask Backend API<br>/api/summarise]
C --> D{AI Available?}

D -->|Yes| E[OpenAI API summarisation]
D -->|No| F[Local fallback summariser]

E --> G[Structured output]
F --> G

G --> H[Displayed in UI<br>Summary / Issues / Actions / Risks / Follow-up]

---

# Example Workflow

1. User pastes a clinical note into the text area
2. The frontend sends the note text to a backend API
3. The backend processes the text using either:
   - an AI model (if API key is provided)
   - a simple fallback summariser
4. The structured output is returned to the interface

---

# Tech Stack

Backend  
Python + Flask

Frontend  
HTML + CSS + JavaScript

AI (optional)  
OpenAI API via environment variable

The application is designed to run locally for demonstration purposes.

---

# Project Structure

app.py                Flask backend and summarisation logic  
templates/index.html  User interface  
static/styles.css     Application styling  
static/app.js         Frontend logic  
samples/              Fake clinical notes for testing  
.env.example          Environment variable template  
requirements.txt      Python dependencies  

---

# Running Locally

Open the project folder in VS Code.

Create a virtual environment:

python3 -m venv .venv

Activate it:

source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Create environment variables:

cp .env.example .env

(Optional) Add your OpenAI API key to `.env`.

Run the application:

python app.py

Open your browser at:

http://127.0.0.1:5000

---

# Testing the App

You can test quickly by:

- Clicking **Load fake sample**
- Or copying a note from:

samples/fake_clinical_notes.txt

Then click **Summarise**.

---

# Safety Note

This project uses only fictional sample clinical notes.

It should not be used with real patient data or any personally identifiable health information.

The project is intended purely for learning and prototyping.

---

# Future Improvements

Possible next iterations could include:

- Speech-to-text note capture
- Specialty-specific summarisation templates
- Risk flag detection
- Integration with Electronic Patient Records
- Human feedback loop for improving summaries
- Audit logs for generated summaries

---

# Learning Goals

This project was created to explore:

- rapid MVP development
- AI-assisted workflows
- product thinking in healthcare tooling
- building and shipping small prototypes

"""
