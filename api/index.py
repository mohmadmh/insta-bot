import random
import string
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "1927821341:AAHh5iQT3dNw1AoI-z-HxDHcULOuLLwuUM4"

app = Application.builder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ البوت يعمل بنجاح! أرسل يوزر لتجربة التخمين.")

app.add_handler(CommandHandler("start", start))

async def handler(request):
    if request.method == "POST":
        try:
            await app.initialize()
            import json
            data = await request.json()
            await app.process_update(Update.de_json(data, app.bot))
        except Exception as e:
            print(f"Error: {e}")
    return {"statusCode": 200, "body": "OK"}
