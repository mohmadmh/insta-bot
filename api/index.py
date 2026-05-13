import os
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "1927821341:AAHh5iQT3dNw1AoI-z-HxDHcULOuLLwuUM4"

# بناء التطبيق بدون تشغيل مستمر (لأنه يعمل كـ Function)
app = Application.builder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ أهلاً محمد! البوت اشتغل أخيراً.")

app.add_handler(CommandHandler("start", start))

# الدالة التي تناديها Vercel
async def handler(request):
    if request.method == "POST":
        try:
            await app.initialize()
            # التأكد من استلام البيانات كنص ثم تحويلها لـ JSON
            body = await request.text()
            data = json.loads(body)
            update = Update.de_json(data, app.bot)
            await app.process_update(update)
        except Exception as e:
            print(f"Error: {e}")
    
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"status": "ok"})
    }
