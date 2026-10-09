"""
Local runner for Telegram Bot.
Supports:
1. Polling mode (default): Test locally without ngrok or webhooks!
   Usage: python bot.py
2. Webhook / Server mode: Run the local Flask server.
   Usage: python bot.py --server
"""

import sys
import os
import time
import requests
from api.index import app, process_telegram_update, BOT_TOKEN, TELEGRAM_API_BASE

def run_polling():
    if not BOT_TOKEN:
        print("[ERROR] TELEGRAM_BOT_TOKEN is not set.")
        print("Please set the environment variable:")
        print("  Windows: $env:TELEGRAM_BOT_TOKEN=\"your_bot_token\"")
        print("  Linux/Mac: export TELEGRAM_BOT_TOKEN=\"your_bot_token\"")
        sys.exit(1)

    print("Checking bot identity...")
    try:
        me = requests.get(f"{TELEGRAM_API_BASE}/getMe", timeout=10).json()
        if not me.get("ok"):
            print(f"[ERROR] Invalid bot token: {me}")
            sys.exit(1)
        bot_user = me["result"]["username"]
        print(f"Bot connected: @{bot_user}")
    except Exception as e:
        print(f"[ERROR] Could not connect to Telegram: {e}")
        sys.exit(1)

    # Delete webhook so polling works without conflict
    print("Deleting any existing webhook to enable polling...")
    requests.get(f"{TELEGRAM_API_BASE}/deleteWebhook", timeout=10)

    print("\nStarting bot polling... Press Ctrl+C to stop.")
    offset = None

    while True:
        try:
            params = {"timeout": 30}
            if offset is not None:
                params["offset"] = offset

            resp = requests.get(
                f"{TELEGRAM_API_BASE}/getUpdates",
                params=params,
                timeout=35
            )

            if resp.status_code == 200:
                data = resp.json()
                if data.get("ok"):
                    for update in data.get("result", []):
                        offset = update["update_id"] + 1
                        print(f"Received update #{update['update_id']}")
                        process_telegram_update(update)
            time.sleep(0.5)
        except KeyboardInterrupt:
            print("\nBot polling stopped.")
            break
        except Exception as err:
            print(f"[WARNING] Polling error: {err}")
            time.sleep(3)


def run_server():
    port = int(os.environ.get("PORT", 8443))
    print(f"Starting local Flask server on http://localhost:{port}...")
    app.run(host="0.0.0.0", port=port, debug=True)


if __name__ == "__main__":
    if "--server" in sys.argv:
        run_server()
    else:
        run_polling()