import os
import logging
import joblib
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ==================== CONFIGURATION ====================
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

# ==================== LOGGING ====================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ==================== LOAD MODEL ====================
try:
    model = joblib.load('models/model.pkl')
    vectorizer = joblib.load('models/vectorizer.pkl')
    logger.info("✅ Boubou's brain loaded!")
except Exception as e:
    logger.error(f"❌ Failed to load model: {e}")
    model = vectorizer = None

# ==================== HELPERS ====================
def predict_spam(text):
    """Return (prediction, confidence) for a given text"""
    if not model or not vectorizer:
        return None, 0
    vec = vectorizer.transform([text.lower()])
    pred = model.predict(vec)[0]
    prob = model.predict_proba(vec)[0]
    spam_idx = list(model.classes_).index('spam')
    return pred, prob[spam_idx]

# ==================== COMMANDS ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"👋 **Welcome {user.first_name}!**\n\n"
        "🕴️ **I'm Boubou.** I protect groups from spam!\n\n"
        "**Commands:**\n"
        "/start - Meet Boubou\n"
        "/help - Show help\n"
        "/check [msg] - Test if message is spam\n"
        "/stats - Statistics\n"
        "/about - About me\n\n"
        "_Add me to a group and make me admin!_ 🛡️",
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "**🆘 Help**\n\n"
        "**Commands:**\n"
        "/start - Meet Boubou\n"
        "/help - This message\n"
        "/check [msg] - Test a message\n"
        "/stats - View statistics\n"
        "/about - About Boubou\n\n"
        "**Group Setup:**\n"
        "1. Add me to group\n"
        "2. Make me admin\n"
        "3. I auto-delete spam!\n\n"
        "_Boubou is always watching._ 👀",
        parse_mode='Markdown'
    )

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🕴️ **About Boubou**\n\n"
        "**Name:** Boubou\n"
        "**Age:** 57\n"
        "**Job:** Anti-spam agent\n"
        "**Accuracy:** 96.5%\n\n"
        "_Boubou keeps your groups clean!_ 🛡️",
        parse_mode='Markdown'
    )

async def check_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = ' '.join(context.args) if context.args else ""
    if not text:
        await update.message.reply_text("❌ Usage: /check [message]\n\nExample: /check Win an iPhone!")
        return
    
    pred, conf = predict_spam(text)
    if pred is None:
        await update.message.reply_text("❌ Model not ready!")
        return
    
    if pred == 'spam':
        await update.message.reply_text(f"🚨 **SPAM!** ({conf:.0%} confidence)")
    else:
        await update.message.reply_text(f"✅ **CLEAN!** ({conf:.0%} confidence)")

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📊 **Boubou's Stats**\n\n"
        "**Model:**\n"
        "• Accuracy: 96.5%\n"
        "• Precision: 96%\n"
        "• Recall: 74%\n\n"
        "**Top Spam Words:**\n"
        "• free • txt • claim • stop • prize\n\n"
        "_Protecting your group!_ 🛡️",
        parse_mode='Markdown'
    )

# ==================== GROUP HANDLER ====================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Skip bots and non-group messages
    if update.effective_user.is_bot:
        return
    if update.effective_chat.type not in ['group', 'supergroup']:
        return
    
    text = update.message.text or ""
    if not text or not model:
        return
    
    # Check for spam
    pred, conf = predict_spam(text)
    
    if pred == 'spam' and conf > 0.3:
        try:
            user = update.effective_user
            name = f"@{user.username}" if user.username else user.first_name
            
            await update.message.delete()
            await update.message.reply_text(
                f"🚫 **{name}**\n\n"
                f"Spam detected! ({conf:.0%} confidence)\n"
                f"Message deleted.\n\n"
                f"_Don't spam. Boubou is watching._ 👀",
                parse_mode='Markdown'
            )
            logger.info(f"Deleted spam from {user.id} ({conf:.0%})")
        except Exception as e:
            logger.error(f"Delete failed: {e}")

# ==================== MAIN ====================
def main():
    if not BOT_TOKEN:
        logger.error("No BOT_TOKEN found!")
        return
    
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(CommandHandler("check", check_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("🤵 Boubou is online!")
    app.run_polling()

if __name__ == '__main__':
    main()