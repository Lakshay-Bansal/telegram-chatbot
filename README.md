# 🤖 Telegram News & Assistant Bot (Vercel Serverless)

A modern, production-ready Telegram Bot built with Python and Flask, engineered specifically for **100% free serverless deployment on [Vercel](https://vercel.com)**.

Includes built-in interactive keyboards, real-time Google News RSS parsing across 9 categories, sticker/message echoing, and a 1-click webhook registration endpoint.

---

## 🌟 Key Features

- ⚡ **Vercel Serverless**: Runs completely on serverless functions with zero idle cost and ultra-fast cold starts.
- 📰 **Live Real-Time News**: Instant news fetching across 9 categories (*Top Stories, World, Nation, Business, Technology, Entertainment, Sports, Science, Health*) via Google News RSS without needing third-party API keys.
- ⌨️ **Interactive Telegram Keyboards**: Custom reply keyboards for smooth category navigation.
- 🔄 **Sticker & Text Echoing**: Mirrors stickers and fallback text seamlessly.
- 🛠️ **1-Click Webhook Setup**: Navigate to `https://<your-domain>.vercel.app/set_webhook` in any browser to automatically link Telegram to your Vercel deployment.
- 💻 **Dual Mode (Local & Cloud)**:
  - **Local Development**: Run `python bot.py` to test with long-polling (no ngrok or public URL required!).
  - **Cloud Production**: Deploys to Vercel via stateless webhooks.

---

## 📁 Project Structure

```text
├── api/
│   └── index.py            # Main serverless entrypoint (Flask app & webhook handler)
├── bot.py                  # Local runner (polling mode & local server)
├── vercel.json             # Vercel routing and rewrite configuration
├── requirements.txt        # Minimal, lean production dependencies (Flask & requests)
├── .env.example            # Environment variables template
├── .gitignore              # Configured for Python & Vercel builds
├── Procfile                # (Optional) For alternative deployment on Render/Railway
└── README.md               # Documentation & setup guide
```

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
If you haven't pushed your code to GitHub yet:
```bash
git add .
git commit -m "Configure Vercel serverless Telegram bot"
git branch -M main
git push -u origin main
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

### 1. Clone & Set Up Virtual Environment
```bash
git clone https://github.com/Lakshay-Bansal/telegram-chatbot.git
cd telegram-chatbot

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
