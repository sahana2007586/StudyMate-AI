# 🎓 StudyMate AI
### An Intelligent Learning & Examination Preparation Platform

StudyMate AI is an AI-powered learning assistant designed to help students understand concepts, prepare for examinations, generate study notes, practise questions, and improve their programming skills.

Built using Python and Flask, the platform connects a web-based interface to an AI model through an OpenAI-compatible API. It can run locally using Ollama and Qwen 2.5.

---

## ✨ Features

- **AI Study Assistant:** Ask academic questions and receive AI-generated responses.
- **Simple Explanations:** Understand difficult concepts in beginner-friendly language.
- **Smart Notes:** Generate short and detailed study notes.
- **Topic Summarization:** Convert topics into concise summaries.
- **Practice Questions:** Generate questions for self-assessment.
- **AI Quiz Support:** Practise topics through AI-generated quizzes.
- **Programming Assistance:** Get help understanding programming concepts.
- **Code Debugging:** Ask for help identifying and correcting programming errors.
- **Context-Aware Conversations:** Continue discussions with previous conversation context.
- **New Chat:** Clear the current conversation and start again.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| HTML5 | Frontend structure |
| CSS3 | User interface styling |
| JavaScript | Frontend interactions |
| Ollama | Local AI model runtime |
| Qwen 2.5 (1.5B) | AI language model |
| Git & GitHub | Version control and project hosting |

## 🏗️ Project Structure

```text
StudyMate-AI/
│
├── app/
│   ├── routes/
│   │   ├── assistant.py
│   │   └── main.py
│   │
│   ├── services/
│   │   └── ai_service.py
│   │
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   │
│   └── templates/
│       ├── assistant.html
│       └── index.html
│
├── tests/
│   └── test_assistant.py
│
├── config.py
├── requirements.txt
├── run.py
├── README.md
└── .gitignore
```

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.10 or newer
- Visual Studio Code (recommended)
- Git
- Ollama

### Step 1: Clone the Repository

```bash
git clone https://github.com/sahana2007586/StudyMate-AI.git
cd StudyMate-AI
```

### Step 2: Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 4: Set Up Ollama

Install Ollama and download the Qwen model:

```bash
ollama pull qwen2.5:1.5b
```

Make sure Ollama is running on your computer.

### Step 5: Configure Environment Variables

Create a file named `.env` in the project root directory.

Add:

```env
SECRET_KEY=replace-with-a-long-random-secret
STUDYMATE_AI_API_KEY=ollama-local
STUDYMATE_AI_BASE_URL=http://localhost:11434/v1
STUDYMATE_AI_MODEL=qwen2.5:1.5b
FLASK_DEBUG=1
```

The `.env` file is excluded from Git to protect configuration values. Never upload your actual secrets.

### Step 6: Run the Application

```bash
python run.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000/
```

Open the AI Study Assistant:

```text
http://127.0.0.1:5000/assistant
```

## 🧪 Running Tests

Run the automated tests using:

```bash
python -m unittest discover -s tests -v
```

The tests mock the AI provider and do not require paid API requests.

## 🔐 Security & Current Limitations

- Environment variables are used for AI configuration.
- API credentials are not intended to be exposed in frontend code.
- The application currently does not include student authentication or API rate limiting.
- The current version is intended for local development and testing, not unrestricted public deployment.

## 🚀 Future Enhancements

- Student registration and login.
- Subject-wise learning support.
- Previous Year Question (PYQ) analysis.
- Repeated examination question identification.
- Subject and subject-code selection.
- Personalized study plans.
- Progress tracking and performance analytics.
- Document and PDF-based learning.
- Improved quiz and assessment functionality.
- Cloud deployment.

## 🎯 Project Objective

The objective of StudyMate AI is to make learning more accessible, interactive, and efficient through artificial intelligence.

It aims to provide students with a centralized learning assistant that supports concept understanding, examination preparation, and programming practice.

## 👩‍💻 Developer

**Sahana**

First-Year Engineering Student | Artificial Intelligence & Machine Learning

---

⭐ If you find this project interesting, consider giving the repository a star!