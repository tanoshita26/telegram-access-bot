import os
from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = "YOUR_NEW_BOT_TOKEN"
CHAT_ID = "7539943162"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=data)

@app.route("/", defaults={'path': ''})
@app.route("/<path:path>")
def catch_all(path):
    full_url = request.url
    send_telegram_message(f"🌐 Someone accessed: {full_url}")
    return f"✅ Access logged and reported to Telegram.\n\n{full_url}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Get the port from environment
    app.run(host="0.0.0.0", port=port)  