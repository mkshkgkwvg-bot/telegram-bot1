import os
import yt_dlp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

MENU_TEXT = """🤖 بوت تحميل احترافي ⚡
⌁︙آهلا بك اغاتي في بوت التحميل 🤍
⌁︙يمكنك التحميل من (يوتيوب، انستكرام، تيك توك، فيسبوك، تويتر، سناب شات، ساوند كلاود)
⌁︙تكدر تحمل أي فيديو بسهولة 🔥
⌁︙لتحميل المقاطع أرسل رابط الفيديو 🎞️
⌁︙لتحميل الفيديوهات أو الصوت اختار من الأزرار 👇
"""


# 🟢 Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(MENU_TEXT)


# 🟢 Handle messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    try:
        # YouTube
        if "youtube.com" in url or "youtu.be" in url:
            keyboard = [
                [
                    InlineKeyboardButton("📹 فيديو", callback_data=f"video|{url}"),
                    InlineKeyboardButton("🎧 صوت", callback_data=f"audio|{url}")
                ]
            ]
            await update.message.reply_text(
                "🎬 اختر الطريقة:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            return

        # Instagram
        if "instagram.com" in url:
            await update.message.reply_text("⏳ جاري تحميل إنستكرام...")

            ydl_opts = {
                "outtmpl": "insta.%(ext)s",
                "format": "best",
                "quiet": True
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            file_path = "insta.mp4"
            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    await update.message.reply_document(f)
                os.remove(file_path)
            return

        # TikTok
        if "tiktok.com" in url:
            await update.message.reply_text("⏳ جاري تحميل تيك توك...")

            ydl_opts = {
                "outtmpl": "tiktok.%(ext)s",
                "format": "best",
                "quiet": True
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            file_path = "tiktok.mp4"
            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    await update.message.reply_document(f)
                os.remove(file_path)
            return

        await update.message.reply_text("❌ ابعت رابط صحيح يا نجم")

    except Exception as e:
        await update.message.reply_text(f"⚠️ خطأ: {e}")


# 🟢 Button handler (YouTube)
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    action, url = query.data.split("|")

    try:
        # 📹 Video
        if action == "video":
            await query.message.reply_text("⏳ جاري تحميل الفيديو...")

            ydl_opts = {
                "outtmpl": "video.mp4",
                "format": "best",
                "noplaylist": True
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            file_path = "video.mp4"
            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    await query.message.reply_document(f)
                os.remove(file_path)

        # 🎧 Audio
        elif action == "audio":
            await query.message.reply_text("⏳ جاري تحميل الصوت...")

            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": "audio.%(ext)s",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192"
                }]
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            file_path = "audio.mp3"
            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    await query.message.reply_audio(f)
                os.remove(file_path)

    except Exception as e:
        await query.message.reply_text(f"⚠️ خطأ: {e}")


# 🟢 Run bot
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_handler(CallbackQueryHandler(button_handler))

print("Bot is running...")
app.run_polling()
