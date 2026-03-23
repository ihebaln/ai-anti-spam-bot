import os
from dotenv import load_dotenv
import telegram.ext

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

def start(update, context):
    update.message.reply_text("Boubou is alive!")

def main():
    print("Starting Boubou...")
    
    # Create updater with longer timeouts
    updater = telegram.ext.Updater(
        BOT_TOKEN,
        use_context=True,
        request_kwargs={
            'read_timeout': 60,
            'connect_timeout': 60
        }
    )
    
    dp = updater.dispatcher
    dp.add_handler(telegram.ext.CommandHandler("start", start))
    
    print("Boubou is online!")
    updater.start_polling(timeout=60)
    updater.idle()

if __name__ == '__main__':
    main()