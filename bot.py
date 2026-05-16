import os
import json
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

INSTAGRAM_URL = "https://www.instagram.com/10_e11?igsh=MTU1djJyYmZlajZuag=="

DATA_FILE = "users.json"
BLOCK_FILE = "blocked.json"


# ---------- ملفات ----------
def load_json(file, default):
    if not os.path.exists(file):
        return default
    with open(file, "r") as f:
        return json.load(f)

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f)


users = load_json(DATA_FILE, {})
blocked = load_json(BLOCK_FILE, {})


MENU_TEXT = """🤖 بوت التحميل ⚡
⌁︙تم التحقق بنجاح يا نجم 🔥
⌁︙ابعت أي رابط وأنا أحملهولك 💪"""


# ---------- Start ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    if blocked.get(user_id):
        await update.message.reply_text("🚫 إنت محظور")
        return

    if users.get(user_id):
        await update.message.reply_text(MENU_TEXT)
        return

    keyboard = [
        [InlineKeyboardButton("📲 تابعني على إنستجرام", url=INSTAGRAM_URL)],
        [InlineKeyboardButton("🔥 عملت متابعة", callback_data="verify")]
    ]

    await update.message.reply_text(
        "😏 تابع الإنستا الأول عشان تستخدم البوت",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ---------- Messages ----------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    if blocked.get(user_id):
        return

    if not users.get(user_id):
        await update.message.reply_text("😏 لازم تتابع الإنستا الأول وبعدين /start")
        return

    url = update.message.text

    try:
        # 🚫 BLOCK YOUTUBE
        if "youtube.com" in url or "youtu.be" in url:
            await update.message.reply_text("😅 يا صديقي مش بيدعم تحميل روابط يوتيوب دلوقتي")
            return

        # 📸 Instagram
        if "instagram.com" in url:
            await update.message.reply_text("😎 جاري تحميل إنستا...")

            ydl_opts = {"outtmpl": "insta.%(ext)s", "format": "best", "quiet": True}

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            if os.path.exists("insta.mp4"):
                with open("insta.mp4", "rb") as f:
                    await update.message.reply_document(f)
                os.remove("insta.mp4")
            return

        # 🎵 TikTok
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

        await update.message.reply_text("❌ ابعت رابط صحيح")

    except Exception as e:
        await update.message.reply_text(f"⚠️ خطأ: {e}")


# ---------- Buttons ----------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    user_id = str(update.effective_user.id)

    if blocked.get(user_id):
        return

    try:
        # ✅ Verify
        if data == "verify":
            users[user_id] = True
            save_json(DATA_FILE, users)

            await query.message.reply_text("🔥 تم التحقق يا نجم.. اكتب /start")
            return

        # 🎬 video/audio
        action, url = data.split("|")

        if action == "video":
            await query.message.reply_text("🔥 جاري التحميل...")

            ydl_opts = {"outtmpl": "video.mp4", "format": "best", "noplaylist": True}

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            if os.path.exists("video.mp4"):
                with open("video.mp4", "rb") as f:
                    await query.message.reply_document(f)
                os.remove("video.mp4")

        elif action == "audio":
            await query.message.reply_text("🔥 جاري الصوت...")

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

    except Exception as e:
        await query.message.reply_text(f"⚠️ خطأ: {e}")


# ---------- Admin ----------
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total = len(users)

    keyboard = [
        [InlineKeyboardButton("📊 عدد المستخدمين", callback_data="stats")]
    ]

    await update.message.reply_text(
        f"👑 الأدمن\n👥 المستخدمين: {total}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.message.reply_text(f"👥 عدد المستخدمين: {len(users)}")


# ---------- Run ----------
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("admin", admin))

app.add_handler(CallbackQueryHandler(stats, pattern="stats"))
app.add_handler(CallbackQueryHandler(button_handler))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot is running...")
app.run_polling()
