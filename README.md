# 🤖 AI Anti-Spam Bot

A Telegram bot that automatically detects and removes spam messages using machine learning.

## How It Works

1. A pre-trained ML model (scikit-learn) lives in the `models/` folder
2. The bot connects to Telegram using your bot token
3. Every message in your group is checked by the model
4. Spam messages are automatically deleted

---

## 🚀 Deploy to Railway (24/7 Hosting)

### Step 1 — Push this repo to GitHub (if not done)
```bash
git add .
git commit -m "Ready for deployment"
git push
```

### Step 2 — Create Railway account
Go to https://railway.app → Sign up with GitHub

### Step 3 — Create new project
- Click **New Project** → **Deploy from GitHub repo**
- Select this repo

### Step 4 — Add environment variable
In Railway dashboard → your service → **Variables** tab:
```
TELEGRAM_BOT_TOKEN = paste_your_token_here
```

### Step 5 — Deploy
Railway auto-deploys. Watch the **Logs** tab to confirm it's running.

---

## 🛠 Local Development

### 1. Clone and set up
```bash
git clone https://github.com/ihebaln/ai-anti-spam-bot.git
cd ai-anti-spam-bot
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
```

### 2. Create your .env file
```bash
cp .env.example .env
# Then open .env and paste your real bot token
```

### 3. Run locally
```bash
python src/bot.py
```

---

## 📁 Project Structure

```
ai-anti-spam-bot/
├── src/           # Bot source code
├── models/        # Trained ML spam detection model (.pkl)
├── data/          # Training data
├── requirements.txt
├── railway.toml   # Railway deployment config
├── Procfile       # Process definition
├── .env.example   # Environment variable template
└── .gitignore
```

---

## ⚙️ Environment Variables

| Variable | Description |
|---|---|
| `TELEGRAM_BOT_TOKEN` | Your bot token from @BotFather on Telegram |

---

## 📦 Dependencies

- `python-telegram-bot==20.7` — Telegram API
- `scikit-learn==1.3.0` — Spam detection ML
- `pandas==2.0.3` — Data handling
- `numpy==1.24.3` — Numerical operations
- `joblib==1.3.2` — Load trained model
- `python-dotenv==1.0.0` — Read .env file
