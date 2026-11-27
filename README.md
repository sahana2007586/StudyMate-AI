# StudyMate-AI
AI-powered learning and examination preparation platform for Indian students

## AI Study Assistant

The assistant sends chat requests from Flask to an OpenAI-compatible Chat
Completions API. The default provider is OpenAI, using the `gpt-4o-mini` model.
The app uses Python's standard-library HTTP client rather than a provider SDK.
Set the API key in the server's environment or in a root `.env` file; it is
read only by Flask and is never sent to the browser.
You can optionally configure a compatible provider with `STUDYMATE_AI_BASE_URL`
and select another model with `STUDYMATE_AI_MODEL`.

Install the requirements once, then create `.env` in the repository root (the
same folder as `run.py`) with your provider's actual key:

```text
STUDYMATE_AI_API_KEY=replace-this-with-your-real-provider-key
```

`.env` is excluded from Git. Do not commit it or put the key in frontend code.
Environment variables already set in the process take precedence over values
from `.env`.

Install dependencies and start Flask from PowerShell:

```powershell
Set-Location "C:\Users\User\git miniproject 1\StudyMate-AI"
& ".venv\Scripts\python.exe" -m pip install -r requirements.txt
```

After saving `.env`, stop any running Flask process with Ctrl+C and restart it:

```powershell
& ".venv\Scripts\python.exe" run.py
```

Alternatively, set `STUDYMATE_AI_API_KEY` in the current PowerShell session
before starting Flask; it overrides `.env`.

Open `http://127.0.0.1:5000/assistant`. If no API key is configured, the page
still loads and the chat endpoint explains how to configure it; it does not
pretend to generate an answer. Do not put the key in frontend code or commit it.
Messages are kept only in the open browser page and sent to the configured
provider for answer generation.

The assistant supports general questions, simple explanations, short and
detailed notes, topic summaries, practice questions, quizzes, programming help,
and code debugging. Follow-up context is sent with each request; use **New
chat** to clear it.

The application does not yet include student login or API rate limiting. Keep
it available only to trusted local users until authentication and request
throttling are implemented before any public deployment.

Run the automated tests with:

```powershell
& ".venv\Scripts\python.exe" -m unittest discover -s tests -v
```

The tests mock the provider, so they do not require a key or make paid network
requests. To verify a live answer, configure a valid provider key and ask a
question in the assistant page.
