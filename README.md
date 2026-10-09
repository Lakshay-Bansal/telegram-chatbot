# 🤖 Telegram News & Assistant Bot (Vercel Serverless)

A modern, production-ready Telegram Bot built with Python and Flask, engineered specifically for **100% free serverless deployment on [Vercel](https://vercel.com)**.

Includes built-in interactive keyboards, real-time Google News RSS parsing across 9 categories, sticker/message echoing, a 1-click webhook registration endpoint, and complete tracking of developmental milestones.

---

## 🌟 Key Features

- ⚡ **Vercel Serverless**: Runs completely on serverless functions with zero idle cost and ultra-fast cold starts.
- 📰 **Live Real-Time News**: Instant news fetching across 9 categories (*Top Stories, World, Nation, Business, Technology, Entertainment, Sports, Science, Health*) via Google News RSS without third-party API keys.
- ⌨️ **Interactive Telegram Keyboards**: Custom reply keyboards for smooth category navigation.
- 🔄 **Sticker & Text Echoing**: Mirrors stickers and fallback text seamlessly.
- 🛠️ **1-Click Webhook Setup**: Navigate to `https://<your-domain>.vercel.app/set_webhook` in any browser to automatically link Telegram to your Vercel deployment.
- 💻 **Dual Mode (Local & Cloud)**:
  - **Local Development**: Run `python bot.py` to test with long-polling (no ngrok or public URL required!).
  - **Cloud Production**: Deploys to Vercel via stateless webhooks.
- 📜 **Complete Version History**: Includes and documents all developmental milestones in [`versions/`](versions/) from the initial prototype to Dialogflow NLP, keyboards, and serverless production.

---

## 📁 Project Structure

```text
chat_bot/
├── api/
│   └── index.py                        # Main serverless entry point (Flask app & webhook handler)
├── bot.py                              # Local runner (polling mode & local server)
├── vercel.json                         # Vercel routing and rewrite configuration
├── requirements.txt                    # Lean production dependencies (Flask & requests)
├── .env.example                        # Environment variables template
├── .gitignore                          # Configured for Python & Vercel builds
├── Procfile                            # (Optional) For deployment on Render/Railway
├── README.md                           # Documentation, setup guide & version history
└── versions/                           # Developmental milestones & reference scripts
    ├── telegram_bot.py                 # Core telegram bot script (tracked across git commits)
    ├── dialogflow.py                   # Google Dialogflow NLP session & intent detection logic
    └── fetch_news.py                   # Standalone news retrieval script using gnewsclient
```

---

## 📜 Project Evolution & Version History

This repository tracks the complete journey of the bot across incremental commits and architectural improvements:

| Step / Commit | Milestone | Description |
| :--- | :--- | :--- |
| **v1.0** (`c83af25`) | Initial Echo Bot | First working prototype using classic `(bot, update)` handlers with `/start`, `/help`, `echo_text`, and `echo_sticker`. |
| **v2.0** (`03e8c90`) | Modern Handler Architecture | Refactored callback signatures to `(update: Update, context: CallbackContext)` and switched to `update.message.reply_text`. |
| **v3.0** (`6d914e4`) | Webhook & Public Server | Migrated from client-side polling to event-driven webhooks using Flask and `ngrok` on port 8443. |
| **v4.0** (`751a5f0`) | Google Dialogflow Connection | Added [`dialogflow.py`](versions/dialogflow.py) to connect to Google Cloud Dialogflow (`newsextractor-tjiy`) for NLP intent detection (`get_news` vs `small_talk`). |
| **v4.1** (`0ddbc1b`) | Dialogflow Bot Integration | Integrated `dialogflow.py` with `telegram_bot.py` to parse user queries, extract news topics, and return article links. |
| **v4.2** (`a8d0465`) | Standalone News Retrieval | Added [`fetch_news.py`](versions/fetch_news.py) using `gnewsclient` to test fetching news by topic, language, and country. |
| **v5.0** (`76979b4`) | Interactive Category Keyboards | Added `topics_keyboard` and `/news_topics` command returning a 3x3 `ReplyKeyboardMarkup` for intuitive user navigation. |
| **v6.0** (`dc79a71`) | Vercel Serverless Production | Converted bot to production serverless architecture with `api/index.py`, 1-click `/set_webhook`, RSS feeds, and local runner `bot.py`. |

---

## 🚀 Quick Start: Deploy to Vercel (Step-by-Step)

### Step 1: Create Your Bot on Telegram
1. Open Telegram and search for [@BotFather](https://t.me/BotFather).
2. Send `/newbot` and follow the prompts to choose a name and username.
3. BotFather will provide an API token that looks like:
   ```text
   1234567890:ABCdefGhIJKlmNoPQRsTUVwxyZ
   ```
4. Copy this token safely.

---

### Step 2: Push This Repository to GitHub
```bash
git add .
git commit -m "Update documentation and version history"
git push origin main
```

---

### Step 3: Deploy on Vercel
1. Go to [Vercel](https://vercel.com) and log in with your GitHub account.
2. Click **"Add New..."** → **"Project"**.
3. Import your `chat_bot` (or `telegram-chatbot`) repository.
4. In the **Environment Variables** section, add:
   - **Key**: `TELEGRAM_BOT_TOKEN`
   - **Value**: `Your Telegram Bot Token from Step 1`
5. Click **Deploy**. Vercel will build and deploy your project in under a minute!

---

### Step 4: Register the Webhook (1-Click)
Once deployed, Vercel assigns you a URL (e.g. `https://my-telegram-bot.vercel.app`).

1. Open your browser and visit:
   ```text
   https://<your-vercel-domain>.vercel.app/set_webhook
   ```
2. You will receive a JSON response from Telegram confirming registration:
   ```json
   {
     "target_webhook_url": "https://my-telegram-bot.vercel.app/api/webhook",
     "telegram_response": {
       "ok": true,
       "result": true,
       "description": "Webhook was set"
     }
   }
   ```
3. Open your bot on Telegram, send `/start`, and enjoy! 🎉

---

## 💻 Local Development

You can test and run the bot on your computer without deploying or using webhooks.

### 1. Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# On macOS / Linux:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set the Environment Variable
- **Windows (PowerShell)**:
  ```powershell
  $env:TELEGRAM_BOT_TOKEN="your_bot_token_here"
  ```
- **macOS / Linux**:
  ```bash
  export TELEGRAM_BOT_TOKEN="your_bot_token_here"
  ```

### 4. Run Locally (Polling Mode)
```bash
python bot.py
```
> **Note**: Polling mode connects directly to Telegram and fetches updates in real-time. No ngrok, port-forwarding, or public IP needed!

### 5. Run Local Webhook Server (Optional)
If you want to run the Flask server locally on `http://localhost:8443`:
```bash
python bot.py --server
```

---

## 🌐 Webhook & Server Endpoints

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/` | `GET` | Health check dashboard showing bot status & links |
| `/api/webhook` | `POST` | Telegram webhook receiver (invoked by Telegram servers) |
| `/set_webhook` | `GET` | Automatically registers the active Vercel domain with Telegram |
| `/webhook_info` | `GET` | Queries Telegram's `getWebhookInfo` to inspect webhook health |

---

## 🤖 Available Bot Commands

| Command / Input | Action |
| :--- | :--- |
| `/start` | Welcomes the user with their name and shows available features |
| `/news_topics` | Displays interactive buttons for news categories |
| Click category | Returns the latest 5 news headlines with clickable links |
| `/help` | Displays help message and instructions |
| *Any text* | Echoes the text back |
| *Sticker* | Echoes the sticker back |

---

## 🛠️ Troubleshooting

### 1. Bot doesn't reply on Vercel
- **Check environment variable**: In the Vercel dashboard, verify that `TELEGRAM_BOT_TOKEN` is set and saved under **Settings** → **Environment Variables**, then trigger a redeploy.
- **Check webhook registration**: Visit `https://<your-vercel-domain>.vercel.app/webhook_info` to ensure `url` points to `https://<your-vercel-domain>.vercel.app/api/webhook` and `pending_update_count` is 0.
- **Check Vercel Runtime Logs**: In Vercel, open your project → **Logs** to view live function logs.

### 2. "Webhook is already set" or conflicts during local testing
- When you run `python bot.py`, it automatically clears any existing webhook so polling works immediately.
- When you are ready to switch back to Vercel, simply visit `https://<your-vercel-domain>.vercel.app/set_webhook` again.

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).
