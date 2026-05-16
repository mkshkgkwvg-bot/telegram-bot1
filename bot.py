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

MENU_TEXT = """
🤖 بوت تحميل سريع ⚡

📥 ابعت أي رابط:
- YouTube 🎬
- Instagram 📸
- TikTok 🎵

🎬 يوتيوب:
📹 فيديو
🎧 صوت سريع
"""


# 🟢 Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(MENU_TEXT)


# 🟢 رسائل الروابط
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    try:
        # 🎬 YouTube
        if "youtube.com" in url or "youtu.be" in url:
            keyboard = [
                [
                    InlineKeyboardButton("📹 فيديو سريع", callback_data=f"video|{url}"),
                    InlineKeyboardButton("🎧 صوت سريع ⚡", callback_data=f"audio|{url}")
                ]
            ]
            await update.message.reply_text(
                "⚡ اختر نوع التحميل السريع:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            return

        # 📸 Instagram
        if "instagram.com" in url:
            await update.message.reply_text("⚡ تحميل إنستجرام...")

            ydl_opts = {
                "outtmpl": "insta.%(ext)s",
                "format": "best",
                "quiet": True,
                "no_warnings": True
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            await update.message.reply_document(open("insta.mp4", "rb"))
            os.remove("insta.mp4")
            return

        # 🎵 TikTok
        if "tiktok.com" in url:
            await update.message.reply_text("⚡ تحميل تيك توك...")

            ydl_opts = {
                "outtmpl": "tiktok.%(ext)s",
                "format": "best",
                "quiet": True
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            await update.message.reply_document(open("tiktok.mp4", "rb"))
            os.remove("tiktok.mp4")
            return

        await update.message.reply_text("❌ ابعت رابط صحيح")

    except Exception as e:
        await update.message.reply_text(f"⚠️ خطأ: {str(e)}")


# 🟢 يوتيوب (سريع جدًا)
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    action, url = query.data.split("|")

    try:
        # 📹 فيديو سريع
        if action == "video":
            await query.message.reply_text("⚡ تحميل فيديو سريع...")

            ydl_opts = {
                "outtmpl": "video.%(ext)s",
                "format": "best[ext=mp4]/best",
                "noplaylist": True,
                "quiet": True,
                "no_warnings": True,
                "concurrent_fragment_downloads": 3
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            await query.message.reply_document(open("video.mp4", "rb"))
            os.remove("video.mp4")

        # 🎧 صوت سريع جدًا
        elif action == "audio":
            await query.message.reply_text("⚡ تحميل صوت سريع...")

            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": "audio.%(ext)s",
                "noplaylist": True,
                "quiet": True,
                "no_warnings": True,
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192"
                }]
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            await query.message.reply_audio(open("audio.mp3", "rb"))
            os.remove("audio.mp3")

    except Exception as e:
        await query.message.reply_text(f"⚠️ خطأ: {str(e)}")


# 🟢 تشغيل البوت
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_handler(CallbackQueryHandler(button_handler))

print("Bot is running ⚡")
app.run_polling()
