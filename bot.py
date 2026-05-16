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

# ✅ إنستجرامك
INSTAGRAM_URL = "https://www.instagram.com/10_e11?igsh=MTU1djJyYmZlajZuag=="

MENU_TEXT = """🤖 بوت التحميل ⚡
⌁︙تم التحقق بنجاح يا نجم 🔥
⌁︙ابعت أي رابط وأنا أحملهولك 💪
⌁︙يوتيوب / إنستا / تيك توك / فيسبوك / تويتر"""

verified_users = set()


# 🟢 Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id in verified_users:
        await update.message.reply_text(MENU_TEXT)
        return

    keyboard = [
        [InlineKeyboardButton("📲 تابعني على إنستجرام يا نجم", url=INSTAGRAM_URL)],
        [InlineKeyboardButton("🔥 عملت متابعة - تحقق", callback_data="verify")]
    ]

    await update.message.reply_text(
        "😏 لازم تتابع الإنستا الأول عشان تستخدم البوت",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# 🟢 Messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in verified_users:
        await update.message.reply_text("😏 تابع الإنستا الأول وبعدين ارجع /start")
        return

    url = update.message.text

    try:
        if "youtube.com" in url or "youtu.be" in url:
            keyboard = [[
                InlineKeyboardButton("📹 فيديو", callback_data=f"video|{url}"),
                InlineKeyboardButton("🎧 صوت", callback_data=f"audio|{url}")
            ]]

            await update.message.reply_text(
                "🔥 اختار يا نجم:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            return

        if "instagram.com" in url:
            await update.message.reply_text("😎 بحمّل من إنستا يا برو...")

            ydl_opts = {"outtmpl": "insta.%(ext)s", "format": "best", "quiet": True}

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            if os.path.exists("insta.mp4"):
                with open("insta.mp4", "rb") as f:
                    await update.message.reply_document(f)
                os.remove("insta.mp4")
            return

        if "tiktok.com" in url:
            await update.message.reply_text("🔥 جاري تحميل تيك توك...")

            ydl_opts = {"outtmpl": "tiktok.%(ext)s", "format": "best", "quiet": True}

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            if os.path.exists("tiktok.mp4"):
                with open("tiktok.mp4", "rb") as f:
                    await update.message.reply_document(f)
                os.remove("tiktok.mp4")
            return

        await update.message.reply_text("❌ ابعت رابط صحيح يا نجم")

    except Exception as e:
        await update.message.reply_text(f"⚠️ خطأ: {e}")


# 🟢 Buttons
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    action, url = query.data.split("|")

    try:
        if action == "video":
            await query.message.reply_text("🔥 جاري تحميل الفيديو...")

            ydl_opts = {"outtmpl": "video.mp4", "format": "best", "noplaylist": True}

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            if os.path.exists("video.mp4"):
                with open("video.mp4", "rb") as f:
                    await query.message.reply_document(f)
                os.remove("video.mp4")

        elif action == "audio":
            await query.message.reply_text("🔥 جاري تحميل الصوت...")

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

            if os.path.exists("audio.mp3"):
                with open("audio.mp3", "rb") as f:
                    await query.message.reply_audio(f)
                os.remove("audio.mp3")

        elif action == "verify":
            user_id = update.effective_user.id
            verified_users.add(user_id)
            await query.message.reply_text("🔥 تم التحقق يا نجم.. اكتب /start")

    except Exception as e:
        await query.message.reply_text(f"⚠️ خطأ: {e}")


# 🟢 Run
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_handler(CallbackQueryHandler(button_handler))

print("Bot is running...")
app.run_polling()
