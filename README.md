# AI Reflection Agent 🤖📝

A multi-agent LinkedIn post generator and refiner built with **LangGraph**, providing interfaces via **Telegram Bot** and **Streamlit**.

## 🚀 Features

- **Agentic Workflow**: Uses a "Generator" and a "Critique" agent loop to refine content.
- **Telegram Bot**: Generate and approve posts directly from your phone.
- **Streamlit UI**: Visual workflow progress and final post preview.
- **Strict Content Rules**: Professional, placeholder-free, and technical tone.

## 🛠️ Project Structure

```text
reflection_agent/
├── bot.py           # Legacy (deleted)
├── telegram_bot.py  # Main Telegram Bot entry point
├── ui_app.py        # Streamlit Web Interface
├── reflection.py    # Core LangGraph workflow logic
└── README.md        # This file
```

## 📖 How to Run

### Setup
Ensure you are in the project root and have your virtual environment active:
```bash
source venv/bin/activate
```

### Telegram Bot
The bot allows you to generate, refine, and approve posts via Telegram chat.
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/reflection_agent
python reflection_agent/telegram_bot.py
```

### Streamlit UI
A web-based interface for interactive post generation.
```bash
streamlit run reflection_agent/ui_app.py
```

## ⚠️ Troubleshooting

### Telegram Bot "Conflict" Error
If you see a `Conflict` error, it means another instance of the bot is already running. You can stop all instances with:
```bash
pkill -f "telegram_bot.py"
```

---
Built with 💙 using LangGraph and LangChain.