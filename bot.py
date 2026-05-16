import os

import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler
MENU_TEXT = """
🤖 Bot Menu:

📥 ابعت أي رابط وسيتم تحميله تلقائيًا:
- Instagram
- YouTube

/start لبدء البوت
"""
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(MENU_TEXT)
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    print("BOT_TOKEN is missing!")
    exit()




# 🟢 رسالة ترحيب
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 أهلاً بيك في بوت التحميل\n\n"
        "📌 ابعت أي لينك:\n"
        "- إنستجرام\n"
        "- يوتيوب\n\n"
        "وهحمّلهولك فوراً 🔥"
    )


# 🟢 معالجة الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    try:
        # 📌 يوتيوب
        from telegram import InlineKeyboardButton, InlineKeyboardMarkup

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    if "youtube.com" in url or "youtu.be" in url:
        keyboard = [
            [
                InlineKeyboardButton("📹 فيديو", callback_data=f"video|{url}"),
                InlineKeyboardButton("🎧 صوت", callback_data=f"audio|{url}")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "🎬 اختار طريقة التحميل:",
            reply_markup=reply_markup
        )
        return

        async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    action, url = data.split("|")

    if action == "video":
        await query.message.reply_text("⏳ جاري تحميل الفيديو...")
        

       # 📌 Instagram
        if "instagram.com" in url:
            await update.message.reply_text("⏳ جاري تحميل الفيديو من إنستجرام...")

            ydl_opts = {
                'outtmpl': 'instagram.mp4',
                'format': 'best'
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            await update.message.reply_document(document=open("instagram.mp4", "rb"))

            os.remove("instagram.mp4")
            return     
    
        



        await update.message.reply_text("❌ ابعت لينك إنستجرام أو يوتيوب صحيح")

    except Exception as e:
        await update.message.reply_text(f"⚠️ حصل خطأ: {str(e)}")


# 🟢 تشغيل البوت
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot is running...")
app.run_polling()
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    action, url = data.split("|")

    if action == "video":
        await query.message.reply_text("⏳ جاري تحميل الفيديو...")

        ydl_opts = {
            'outtmpl': 'video.mp4',
            'format': 'best'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        await query.message.reply_document(document=open("video.mp4", "rb"))
        os.remove("video.mp4")

    elif action == "audio":
        await query.message.reply_text("⏳ جاري تحميل الصوت...")

        ydl_opts = {
            'outtmpl': 'audio.mp3',
            'format': 'bestaudio'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        await query.message.reply_audio(audio=open("audio.mp3", "rb"))
        os.remove("audio.mp3")
