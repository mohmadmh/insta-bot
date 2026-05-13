import os
import json
import random
import string
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

TOKEN = "1927821341:AAHh5iQT3dNw1AoI-z-HxDHcULOuLLwuUM4"
URL = f"https://api.telegram.org/bot{TOKEN}/"

def generate_username(length):
    chars = string.ascii_lowercase + string.digits + "._"
    return ''.join(random.choice(chars) for _ in range(length))

def send_message(chat_id, text, reply_markup=None):
    payload = {'chat_id': chat_id, 'text': text, 'parse_mode': 'Markdown'}
    if reply_markup:
        payload['reply_markup'] = json.dumps(reply_markup)
    requests.post(URL + "sendMessage", json=payload)

@app.route('/', defaults={'path': ''}, methods=['POST', 'GET'])
@app.route('/<path:path>', methods=['POST', 'GET'])
def main_handler(path):
    if request.method == "POST":
        data = request.get_json()
        if "message" in data:
            chat_id = data["message"]["chat"]["id"]
            text = data["message"].get("text", "")

            if text == "/start":
                markup = {
                    "inline_keyboard": [
                        [{"text": "ثلاثي 🥉", "callback_data": "3"}, {"text": "رباعي 🥈", "callback_data": "4"}],
                        [{"text": "خماسي 🥇", "callback_data": "5"}],
                        [{"text": "المطور 👨‍💻", "url": "https://t.me/H0_Om"}]
                    ]
                }
                send_message(chat_id, "👋 أهلاً بك في بوت تخمين اليوزرات!\nإختر النوع الذي تريده:", reply_markup=markup)
        
        elif "callback_query" in data:
            query = data["callback_query"]
            chat_id = query["message"]["chat"]["id"]
            length = int(query["data"])
            
            users = [generate_username(length) for _ in range(10)]
            res = f"✅ يوزرات مخمنة ({length}) حروف:\n\n" + "\n".join([f"• `@{u}`" for u in users])
            send_message(chat_id, res)
            
    return "OK", 200
