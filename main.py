import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Load environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# Define the tone/personality of Tanjiro
def format_prompt(message: str) -> str:
    return (
        "You are Tanjiro Kamado from Demon Slayer. Respond kindly, gently, and humbly. "
        "Give thoughtful and motivational replies, with occasional subtle Demon Slayer references. "
        "Never be rude or arrogant.\n\n"
        f"User: {message}\nTanjiro:"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    prompt = format_prompt(user_message)
    
    try:
        response = model.generate_content(prompt)
        reply_text = response.text.strip()
    except Exception as e:
        reply_text = "I'm sorry, but I wasn't able to think of a response right now. Please try again."

    await update.message.reply_text(reply_text)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
