#!/bin/bash

echo "================================================"
echo "  AI Anti-Spam Bot - Deployment Preparation"
echo "================================================"
echo ""

# Check we're in the right folder
if [ ! -f "requirements.txt" ]; then
    echo "❌ ERROR: Please run this script from inside your ai-anti-spam-bot folder!"
    echo "   cd into the folder first, then run: bash deploy-prep.sh"
    exit 1
fi

echo "[1/5] Removing venv from Git tracking..."
git rm -r --cached venv/ 2>/dev/null && echo "✅ venv removed from Git" || echo "⚠️  venv wasn't tracked — OK, continuing..."

echo ""
echo "[2/5] Removing output.txt from Git tracking..."
git rm --cached output.txt 2>/dev/null || true

echo ""
echo "[3/5] Staging all deployment files..."
git add .gitignore
git add railway.toml
git add Procfile
git add .env.example
git add README.md
git add requirements.txt
git add src/
git add models/
git add data/
echo "✅ Files staged"

echo ""
echo "[4/5] Committing..."
git commit -m "Add deployment config — ready for Railway"
echo "✅ Committed"

echo ""
echo "[5/5] Pushing to GitHub..."
git push
echo "✅ Pushed!"

echo ""
echo "================================================"
echo "  ✅ DONE! Your repo is ready to deploy."
echo ""
echo "  Next steps:"
echo "  1. Go to https://railway.app"
echo "  2. Sign up with GitHub"
echo "  3. New Project → Deploy from GitHub repo"
echo "  4. Select ai-anti-spam-bot"
echo "  5. Add variable: TELEGRAM_BOT_TOKEN = your_token"
echo "================================================"
