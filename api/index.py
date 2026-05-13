import json
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "1927821341:AAHh5iQT3dNw1AoI-z-HxDHcULOuLLwuUM4"

# إعداد التطبيق
app = Application.builder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ تم الاتصال بنجاح! البوت الآن جاهز للعمل.")

app.add_handler(CommandHandler("start", start))

async def handler(request):
    if request.method == "POST":
        try:
            await app.initialize()
            data = await request.json()
            update = Update.de_json(data, app.bot)
            await app.process_update(update)
        except Exception as e:
            print(f"Error: {e}")
    return {"statusCode": 200, "body": "OK"}
