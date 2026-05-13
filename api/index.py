import os
import random
import string
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# إعدادات البوت
TOKEN = "1927821341:AAHh5iQT3dNw1AoI-z-HxDHcULOuLLwuUM4"
OWNER_USERNAME = "@H0_Om"

def generate_username(length):
    chars = string.ascii_lowercase + string.digits + "._"
    return ''.join(random.choice(chars) for _ in range(length))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("ثلاثي 🥉", callback_data='3'),
         InlineKeyboardButton("رباعي 🥈", callback_data='4')],
        [InlineKeyboardButton("خماسي 🥇", callback_data='5')],
        [InlineKeyboardButton("المطور 👨‍💻", url=f"https://t.me/{OWNER_USERNAME[1:]}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 أهلاً بك في بوت تخمين يوزرات انستقرام\n\nإختر نوع اليوزر:",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    length = int(query.data)
    results = [generate_username(length) for _ in range(10)]
    response_text = f"✅ تم تخمين يوزرات ({query.data}) حروف:\n\n"
    for u in results:
        response_text += f"• `@{u}`\n"
    response_text += f"\nمطور البوت: {OWNER_USERNAME}"
    keyboard = [[InlineKeyboardButton("تخمين المزيد 🔄", callback_data=str(length))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=response_text, parse_mode='Markdown', reply_markup=reply_markup)

# بناء التطبيق
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

# هذه هي الدالة المقصودة (المسؤولة عن الربط مع Vercel)
async def handler(request):
    if request.method == "POST":
        try:
            await app.initialize()
            # استلام البيانات من تليجرام عبر Vercel
            body = await request.json()
            update = Update.de_json(body, app.bot)
            await app.process_update(update)
        except Exception as e:
            print(f"Error: {e}")
    return {"statusCode": 200, "body": "OK"}
