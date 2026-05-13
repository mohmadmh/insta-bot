import os
import json
import random
import string
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = "1927821341:AAHh5iQT3dNw1AoI-z-HxDHcULOuLLwuUM4"
URL = f"https://api.telegram.org/bot{TOKEN}/"

def check_instagram_user(username):
    """فحص إذا كان اليوزر متاحاً أم لا"""
    try:
        # فحص اليوزر عبر رابط انستقرام المباشر
        response = requests.get(f"https://www.instagram.com/{username}/", timeout=5)
        if response.status_code == 404:
            return True  # اليوزر غير موجود فهو متاح
        return False     # اليوزر موجود (غير متاح)
    except:
        return False

def generate_available_user(length):
    """توليد يوزر متاح بعد الفحص"""
    for _ in range(20):  # محاولة فحص 20 يوزر في كل طلب
        user = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))
        if check_instagram_user(user):
            return user
    return None

def send_message(chat_id, text):
    requests.post(URL + "sendMessage", json={'chat_id': chat_id, 'text': text, 'parse_mode': 'Markdown'})

@app.route('/', defaults={'path': ''}, methods=['POST', 'GET'])
@app.route('/<path:path>', methods=['POST', 'GET'])
def main_handler(path):
    if request.method == "POST":
        data = request.get_json()
        if "message" in data:
            chat_id = data["message"]["chat"]["id"]
            text = data["message"].get("text", "")

            if text == "/start":
                send_message(chat_id, "🔍 أرسل طول اليوزر الذي تريد صيده (مثلاً 4 أو 5):")
            
            elif text.isdigit():
                length = int(text)
                send_message(chat_id, f"⏳ جاري فحص يوزرات من {length} حروف... انتظر قليلاً.")
                
                available_user = generate_available_user(length)
                if available_user:
                    send_message(chat_id, f"✅ تم صيد يوزر متاح!\n\n`@{available_user}`\n\nيمكنك استخدامه الآن.")
                else:
                    send_message(chat_id, "❌ لم يتم العثور على يوزر متاح في هذه المحاولة، جرب مرة أخرى.")
                    
    return "OK", 200
