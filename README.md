# AI Reflection Agent 🤖📝

A multi-agent LinkedIn post generator and refiner built with **LangGraph**, offering a professional web interface via **Streamlit** and a mobile interface via **Telegram Bot**.

## 🚀 Features

- **Agentic Workflow**: Uses a "Generator" and a "Critique" agent loop in LangGraph to iteratively improve posts.
- **Streamlit Web UI**: A beautiful, interactive dashboard for real-time post generation and visual workflow tracking.
- **Telegram Bot**: Full mobile control—generate, refine, and approve posts directly from your chat.
- **Smart Reflection**: The critic agent enforces professional tone, removes placeholders, and ensures technical accuracy.

---

## 🛠️ Project Structure

```text
reflection_agent/
├── telegram_bot.py  # Main Telegram Bot entry point
├── ui_app.py        # Streamlit Web Interface (UI)
├── reflection.py    # Core LangGraph workflow logic
└── README.md        # This file
```

---

## ⚙️ Configuration & Setup

### 1. Environment Variables (`.env`)
Create a `.env` file in the root directory and add your credentials:

```env
OPENAI_API_KEY=your_openai_api_key
BOT_TOKEN=your_telegram_bot_token
```

### 2. Getting a Telegram Token
1. Open Telegram and search for **@BotFather**.
2. Send the `/newbot` command and follow the instructions to name your bot.
3. Copy the **API Token** provided and paste it into your `.env` file as `BOT_TOKEN`.

---

## 📖 How to Run

### Setup Virtual Environment
```bash
source venv/bin/activate
# Install dependencies if you haven't already
pip install -r requirements.txt 
```

### Run Telegram Bot
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/reflection_agent
python reflection_agent/telegram_bot.py
```

### Run Streamlit UI
```bash
streamlit run reflection_agent/ui_app.py
```

---

## ⚠️ Troubleshooting

### Telegram Bot "Conflict" Error
If you see a `Conflict` error, another instance of the bot is likely running. Stop all instances with:
```bash
pkill -f "telegram_bot.py"
```

---
Built with 💙 using LangGraph and Streamlit.