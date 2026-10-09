import os
import logging
import requests
import xml.etree.ElementTree as ET
from urllib.parse import quote
from flask import Flask, request, jsonify, render_template_string

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Configuration
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN") or os.environ.get("BOT_TOKEN") or ""
TELEGRAM_API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"

# Keyboard categories
TOPICS_KEYBOARD = [
    ["Top Stories", "World", "Nation"],
    ["Business", "Technology", "Entertainment"],
    ["Sports", "Science", "Health"]
]

TOPIC_FEED_URLS = {
    "top stories": "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en",
    "world": "https://news.google.com/rss/headlines/section/topic/WORLD?hl=en-US&gl=US&ceid=US:en",
    "nation": "https://news.google.com/rss/headlines/section/topic/NATION?hl=en-US&gl=US&ceid=US:en",
    "business": "https://news.google.com/rss/headlines/section/topic/BUSINESS?hl=en-US&gl=US&ceid=US:en",
    "technology": "https://news.google.com/rss/headlines/section/topic/TECHNOLOGY?hl=en-US&gl=US&ceid=US:en",
    "entertainment": "https://news.google.com/rss/headlines/section/topic/ENTERTAINMENT?hl=en-US&gl=US&ceid=US:en",
    "sports": "https://news.google.com/rss/headlines/section/topic/SPORTS?hl=en-US&gl=US&ceid=US:en",
    "science": "https://news.google.com/rss/headlines/section/topic/SCIENCE?hl=en-US&gl=US&ceid=US:en",
    "health": "https://news.google.com/rss/headlines/section/topic/HEALTH?hl=en-US&gl=US&ceid=US:en"
}


def send_message(chat_id, text, reply_markup=None, parse_mode="HTML"):
    """Send a text message via Telegram Bot API."""
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN is not configured.")
        return False
    
    url = f"{TELEGRAM_API_BASE}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode,
        "disable_web_page_preview": False
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup

    try:
        res = requests.post(url, json=payload, timeout=5)
        return res.ok
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        return False


def send_sticker(chat_id, sticker_file_id):
    """Echo a sticker back to the user."""
    if not BOT_TOKEN:
        return False
    
    url = f"{TELEGRAM_API_BASE}/sendSticker"
    payload = {
        "chat_id": chat_id,
        "sticker": sticker_file_id
    }
    try:
        res = requests.post(url, json=payload, timeout=5)
        return res.ok
    except Exception as e:
        logger.error(f"Error sending sticker: {e}")
        return False


def fetch_news(topic_name, max_items=5):
    """Fetch top news articles for a specific topic using Google News RSS."""
    key = topic_name.strip().lower()
    feed_url = TOPIC_FEED_URLS.get(key)
    
    if not feed_url:
        feed_url = f"https://news.google.com/rss/search?q={quote(topic_name)}&hl=en-US&gl=US&ceid=US:en"

    try:
        resp = requests.get(
            feed_url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; TelegramBot/1.0)"},
            timeout=5
        )
        if not resp.ok:
            return "Unable to fetch news at the moment. Please try again later."
        
        root = ET.fromstring(resp.content)
        items = root.findall("./channel/item")[:max_items]
        
        if not items:
            return f"No news found for <b>{topic_name}</b>."

        msg_lines = [f"<b>Top News: {topic_name.title()}</b>\n"]
        for idx, item in enumerate(items, 1):
            title = item.find("title").text if item.find("title") is not None else "News Headline"
            link = item.find("link").text if item.find("link") is not None else "#"
            # Clean title
            title = title.replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp;")
            msg_lines.append(f"{idx}. <a href=\"{link}\">{title}</a>\n")

        return "\n".join(msg_lines)
    except Exception as e:
        logger.error(f"Failed to fetch news: {e}")
        return "Could not retrieve news at this moment. Please try again later."


def process_telegram_update(update_data):
    """Process incoming Telegram update."""
    message = update_data.get("message")
    if not message:
        return

    chat_id = message.get("chat", {}).get("id")
    first_name = message.get("chat", {}).get("first_name", "there")
    text = message.get("text", "")
    sticker = message.get("sticker")

    if not chat_id:
        return

    # Handle stickers
    if sticker:
        send_sticker(chat_id, sticker.get("file_id"))
        return

    # Handle text commands & messages
    if text:
        text_clean = text.strip()

        if text_clean.startswith("/start"):
            welcome_msg = (
                f"Hi <b>{first_name}</b>! Welcome to the News & Assistant Bot.\n\n"
                f"Available commands:\n"
                f"• /news_topics - Choose and read top news categories\n"
                f"• /help - Get assistance\n\n"
                f"Or send any message to have it echoed back!"
            )
            send_message(chat_id, welcome_msg)
            return

        if text_clean.startswith("/help"):
            help_msg = (
                "<b>Bot Help & Guide</b>\n\n"
                "• <b>/news_topics</b>: Browse news by category (Business, Tech, Sports, etc.)\n"
                "• Send any text: The bot will echo it back to you.\n"
                "• Send a sticker: The bot will echo the sticker back."
            )
            send_message(chat_id, help_msg)
            return

        if text_clean.startswith("/news_topics"):
            markup = {
                "keyboard": TOPICS_KEYBOARD,
                "one_time_keyboard": True,
                "resize_keyboard": True
            }
            send_message(chat_id, "Choose a news category:", reply_markup=markup)
            return

        # Check if the user selected one of the news categories
        if text_clean.lower() in TOPIC_FEED_URLS:
            send_message(chat_id, f"Fetching the latest <b>{text_clean}</b> news for you...")
            news_content = fetch_news(text_clean)
            send_message(chat_id, news_content)
            return

        # Default echo text
        send_message(chat_id, f"Echo: {text_clean}")


# ================== Routes ==================

@app.route("/", methods=["GET"])
def home():
    """Health check / landing page."""
    bot_configured = bool(BOT_TOKEN)
    token_preview = f"...{BOT_TOKEN[-6:]}" if len(BOT_TOKEN) > 6 else "Not Configured"
    host_url = request.host_url.rstrip("/")
    
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Telegram Bot Server</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
                color: #f8fafc;
                min-height: 100vh;
                margin: 0;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }}
            .card {{
                background: rgba(30, 41, 59, 0.85);
                backdrop-filter: blur(12px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 16px;
                padding: 36px;
                max-width: 540px;
                width: 100%;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
            }}
            h1 {{
                font-size: 1.75rem;
                margin-top: 0;
                color: #38bdf8;
                display: flex;
                align-items: center;
                gap: 10px;
            }}
            .badge {{
                display: inline-block;
                padding: 4px 12px;
                border-radius: 9999px;
                font-size: 0.85rem;
                font-weight: 600;
                margin-bottom: 20px;
            }}
            .badge-success {{ background: #065f46; color: #34d399; }}
            .badge-warn {{ background: #78350f; color: #fbbf24; }}
            .info-row {{
                margin: 12px 0;
                font-size: 0.95rem;
                color: #cbd5e1;
            }}
            .info-row code {{
                background: #0f172a;
                padding: 3px 6px;
                border-radius: 4px;
                color: #38bdf8;
            }}
            .btn-group {{
                margin-top: 24px;
                display: flex;
                gap: 12px;
                flex-wrap: wrap;
            }}
            .btn {{
                background: #2563eb;
                color: white;
                text-decoration: none;
                padding: 10px 18px;
                border-radius: 8px;
                font-weight: 500;
                font-size: 0.9rem;
                transition: background 0.2s;
                display: inline-block;
            }}
            .btn:hover {{ background: #1d4ed8; }}
            .btn-outline {{
                background: transparent;
                border: 1px solid #475569;
                color: #cbd5e1;
            }}
            .btn-outline:hover {{ background: #334155; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Telegram Bot Server</h1>
            <div>
                {"<span class='badge badge-success'>Bot Token Loaded (" + token_preview + ")</span>" if bot_configured else "<span class='badge badge-warn'>Warning: TELEGRAM_BOT_TOKEN Not Set</span>"}
            </div>
            <div class="info-row">Platform: <code>Vercel Serverless</code></div>
            <div class="info-row">Webhook Endpoint: <code>{host_url}/api/webhook</code></div>
            
            <div class="btn-group">
                <a href="/set_webhook" class="btn">Auto-Set Webhook</a>
                <a href="/webhook_info" class="btn btn-outline">Check Webhook Info</a>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)


@app.route("/api/webhook", methods=["POST"])
@app.route("/webhook", methods=["POST"])
def webhook():
    """Receives webhook updates from Telegram."""
    if not request.is_json:
        return jsonify({"status": "invalid request, expected JSON"}), 400

    update = request.get_json()
    try:
        process_telegram_update(update)
    except Exception as e:
        logger.error(f"Error processing update: {e}")
    return jsonify({"status": "ok"})


@app.route("/set_webhook", methods=["GET"])
@app.route("/api/set_webhook", methods=["GET"])
def setup_webhook():
    """One-click browser endpoint to register the Vercel webhook with Telegram."""
    if not BOT_TOKEN:
        return jsonify({"error": "TELEGRAM_BOT_TOKEN environment variable is not configured."}), 500

    host_url = request.host_url.rstrip("/")
    # Force HTTPS for Telegram webhooks
    if host_url.startswith("http://") and "localhost" not in host_url and "127.0.0.1" not in host_url:
        host_url = "https://" + host_url[7:]

    webhook_url = f"{host_url}/api/webhook"
    url = f"{TELEGRAM_API_BASE}/setWebhook?url={webhook_url}"
    
    try:
        res = requests.get(url, timeout=10)
        return jsonify({
            "target_webhook_url": webhook_url,
            "telegram_response": res.json()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/webhook_info", methods=["GET"])
@app.route("/api/webhook_info", methods=["GET"])
def webhook_info():
    """Inspect the current Telegram webhook status."""
    if not BOT_TOKEN:
        return jsonify({"error": "TELEGRAM_BOT_TOKEN environment variable is not configured."}), 500

    url = f"{TELEGRAM_API_BASE}/getWebhookInfo"
    try:
        res = requests.get(url, timeout=10)
        return jsonify(res.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# For local testing
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8443))
    print(f"Starting server on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=True)
