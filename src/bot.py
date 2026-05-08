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

# ==================== SPAM COUNTER ====================
# Dictionary to store spam counts for each user
spam_counter = {}

def get_spam_count(user_id):
    """Get spam count for a user"""
    return spam_counter.get(user_id, 0)

def increment_spam_count(user_id):
    """Increment spam count and return new count"""
    spam_counter[user_id] = spam_counter.get(user_id, 0) + 1
    return spam_counter[user_id]

def reset_spam_count(user_id):
    """Reset spam count for a user"""
    spam_counter[user_id] = 0

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
        "/about - About me\n"
        "/mywarnings - Check your spam count\n\n"
        "_Spammers get KICKED after 3 warnings!_ 👢",
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
        "/about - About Boubou\n"
        "/mywarnings - Check your spam count\n\n"
        "**Rules:**\n"
        "⚠️ Warning 1: Boubou warns you\n"
        "⚠️ Warning 2: Boubou warns you again\n"
        "👢 Warning 3: Boubou KICKS you out!\n\n"
        "_Don't spam. Boubou is watching._ 👀",
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

async def mywarnings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user their current spam count"""
    user = update.effective_user
    user_id = user.id
    count = get_spam_count(user_id)
    
    if count == 0:
        await update.message.reply_text(
            f"✅ **{user.first_name}**, you have **0 spam warnings**.\n\n"
            f"Keep up the good behavior! 🎉",
            parse_mode='Markdown'
        )
    else:
        remaining = 3 - count
        if remaining < 0:
            remaining = 0
        await update.message.reply_text(
            f"⚠️ **{user.first_name}**, you have **{count}/3 spam warnings**.\n\n"
            f"**{remaining} warning(s) left before being KICKED!**\n\n"
            f"_Stop spamming or Boubou will kick you!_ 👀",
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
    # Calculate total warnings
    total_warnings = sum(spam_counter.values())
    
    await update.message.reply_text(
        f"📊 **Boubou's Stats**\n\n"
        f"**Model:**\n"
        f"• Accuracy: 96.5%\n"
        f"• Precision: 96%\n"
        f"• Recall: 74%\n\n"
        f"**Spam Tracking:**\n"
        f"• Total spam warnings: {total_warnings}\n"
        f"• Users with warnings: {len(spam_counter)}\n\n"
        f"**Top Spam Words:**\n"
        f"• free • txt • claim • stop • prize\n\n"
        f"_Boubou is protecting your group!_ 🛡️",
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
    
    user = update.effective_user
    user_id = user.id
    username = f"@{user.username}" if user.username else user.first_name
    chat_id = update.effective_chat.id
    
    # Check for spam
    pred, conf = predict_spam(text)
    
    if pred == 'spam' and conf > 0.3:
        # Increment spam counter
        spam_count = increment_spam_count(user_id)
        
        try:
            # Delete the spam message
            await update.message.delete()
            
            # Send warning based on spam count
            if spam_count == 1:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=f"⚠️ **{username}**\n\nBoubou detected spam! ({conf:.0%} confidence)\nThis is your **1st warning**.\n\n_2 more warnings and you will be kicked._ 👀",
                    parse_mode='Markdown'
                )
            elif spam_count == 2:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=f"⚠️⚠️ **{username}**\n\nBoubou detected spam AGAIN! ({conf:.0%} confidence)\nThis is your **2nd warning**.\n\n**1 more warning and you will be KICKED!** 👢",
                    parse_mode='Markdown'
                )
            elif spam_count >= 3:
                try:
                    # KICK the user (ban then unban = kick)
                    await context.bot.ban_chat_member(chat_id, user_id)
                    await context.bot.unban_chat_member(chat_id, user_id)
                    
                    # Send confirmation
                    await context.bot.send_message(
                        chat_id=chat_id,
                        text=f"👢👢👢 **{username}**\n\nYou have been **KICKED** from this group for spamming {spam_count} times!\n\n_Goodbye. Boubou does not forgive._ 👢",
                        parse_mode='Markdown'
                    )
                    
                    logger.info(f"✅ KICKED user {user_id} from chat {chat_id}")
                    reset_spam_count(user_id)
                    
                except Exception as kick_error:
                    logger.error(f"Kick failed: {kick_error}")
                    await context.bot.send_message(
                        chat_id=chat_id,
                        text=f"⚠️ **Error**\n\nI want to kick **{username}** but I'm missing permissions!\nPlease make me an admin with 'Ban Users' rights.",
                        parse_mode='Markdown'
                    )
            
            logger.info(f"Spam #{spam_count} from {user_id} ({conf:.0%})")
            
        except Exception as e:
            logger.error(f"Failed to handle spam: {e}")
    else:
        logger.info(f"Clean message from {user_id}")

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
    app.add_handler(CommandHandler("mywarnings", mywarnings_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("🤵 Boubou is online with spam counter and KICK system!")
    app.run_polling()

if __name__ == '__main__':
    main()