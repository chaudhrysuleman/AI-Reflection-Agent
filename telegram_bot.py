print("SCRIPT STARTING...", flush=True)
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    CallbackQueryHandler,
    filters,
)
import os
from dotenv import load_dotenv, find_dotenv

try:
    from reflection import build_graph
    from langchain_core.messages import HumanMessage, AIMessage
except ImportError:
    # If imports fail (e.g. during testing), we use fallback placeholders
    build_graph = None
    print("Warning: reflection.py or dependencies not found. Using placeholders.")

load_dotenv(find_dotenv())
BOT_TOKEN = os.getenv("BOT_TOKEN")

user_state = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi 👋\nWhat topic should I write about for today's LinkedIn post?"
    )
    user_state[update.effective_user.id] = {"stage": "WAIT_TOPIC"}

async def handle_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    state = user_state.get(user_id)

    if not state or state["stage"] != "WAIT_TOPIC":
        return

    topic = update.message.text
    state["topic"] = topic
    state["stage"] = "WAIT_APPROVAL"

    await update.message.reply_text("🔁 Generating and refining your post using LangGraph... Please wait.")

    generated_post = await generate_linkedin_post(topic)

    state["post"] = generated_post

    keyboard = [
        [
            InlineKeyboardButton("✅ Approve", callback_data="approve"),
            InlineKeyboardButton("🔁 Regenerate", callback_data="regenerate"),
            InlineKeyboardButton("❌ Cancel", callback_data="cancel"),
        ]
    ]

    await update.message.reply_text(
        f"Here is the draft post:\n\n{generated_post}",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def handle_decision(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    state = user_state.get(user_id)

    if not state:
        return

    if query.data == "approve":
        await query.edit_message_text(f"✅ Approved. Content:\n\n{state['post']}")
        post_to_linkedin(state["post"])
        user_state.pop(user_id, None)

    elif query.data == "regenerate":
        await query.edit_message_text("🔁 Regenerating post...")
        regenerated_post = await generate_linkedin_post(state["topic"])
        state["post"] = regenerated_post

        keyboard = [
            [
                InlineKeyboardButton("✅ Approve", callback_data="approve"),
                InlineKeyboardButton("🔁 Regenerate", callback_data="regenerate"),
                InlineKeyboardButton("❌ Cancel", callback_data="cancel"),
            ]
        ]

        await context.bot.send_message(
            chat_id=user_id,
            text=f"New draft:\n\n{regenerated_post}",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif query.data == "cancel":
        await query.edit_message_text("❌ Cancelled. No post today.")
        user_state.pop(user_id, None)

# ---- GENERATION LOGIC ----
async def generate_linkedin_post(topic: str) -> str:
    # 🔗 CALL YOUR LANGGRAPH WORKFLOW HERE
    if build_graph is None:
        return f"[MOCK] Generated LinkedIn post about: {topic}"
    
    try:
        workflow = build_graph()
        inputs = HumanMessage(content=topic)

        print("--- Starting Workflow ---")
        final_post = ""
        for event in workflow.stream(inputs):
            for node_name, messages in event.items():
                print(f"\n[Node: {node_name}]")
                for msg in messages:
                    if isinstance(msg, AIMessage):
                        print(f"Agent >> {msg.content}")
                        if node_name == "generate":
                            final_post = msg.content
                    elif isinstance(msg, HumanMessage):
                        print(f"Reflection >> {msg.content}")
            print("-" * 40)

        print("\n" + "="*50)
        print("FINAL LINKEDIN POST:")
        print(f"'{final_post}'")
        print("="*50)
        return final_post
    except Exception as e:
        return f"Error during generation: {str(e)}"

def post_to_linkedin(content: str):
    # 🔗 Playwright or LinkedIn API here
    print("Posting to LinkedIn:\n", content)

def main():
    try:
        print("Starting ApplicationBuilder...", flush=True)
        app = ApplicationBuilder().token(BOT_TOKEN).build()

        print("Adding handlers...", flush=True)
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_topic))
        app.add_handler(CallbackQueryHandler(handle_decision))

        print("Telegram bot is running...", flush=True)
        app.run_polling()
    except Exception as e:
        print(f"CRITICAL ERROR IN MAIN: {e}", flush=True)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"CRITICAL ERROR AT TOP LEVEL: {e}", flush=True)
        import traceback
        traceback.print_exc()
