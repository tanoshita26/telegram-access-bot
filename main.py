from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = "7395726596:AAFjoArLIaBDYw8SodM9QGT_Prv1rO8rGoE"
CHAT_ID = "7539943162"

# ✅ Send message via Telegram
def send_telegram_message(chat_id, message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    requests.post(url, data=data)

# ✅ Call Hugging Face GPT-2 model for a response
def generate_gpt_response(prompt):
    try:
        url = "https://api-inference.huggingface.co/models/gpt2"
        headers = {"Accept": "application/json"}
        payload = {"inputs": prompt}
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        data = response.json()
        return data[0]["generated_text"]
    except Exception as e:
        return f"⚠️ GPT Error: {str(e)}"

# ✅ When URL is accessed
@app.route("/", defaults={'path': ''})
@app.route("/<path:path>")
def catch_all(path):
    full_url = request.url
    send_telegram_message(CHAT_ID, f"🌐 Someone accessed: {full_url}")
    return f"✅ Access logged and reported to Telegram.\n\n{full_url}"

# ✅ Telegram webhook for replies
@app.route("/webhook", methods=["POST"])
def telegram_webhook():
    data = request.get_json()

    if "message" in data and "text" in data["message"]:
        user_message = data["message"]["text"]
        chat_id = data["message"]["chat"]["id"]

        reply = generate_gpt_response(user_message)
        send_telegram_message(chat_id, reply)

    return {"ok": True}

if __name__ == "__main__":
    # Render sets PORT environment variable automatically — Flask uses port 5000 by default
    from sys import argv
    port = 5000
    if len(argv) > 1:
        try:
            port = int(argv[1])
        except:
            pass
    app.run(host="0.0.0.0", port=port)
