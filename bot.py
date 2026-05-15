import os
import yt_dlp

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# =========================
# TOKEN
# =========================
BOT_TOKEN=os.getenv("8667471311:AAFOvcf7jkhfvEjAMYfG_ks9bnaeGYkq8o0")

# =========================
# DOWNLOAD FOLDER
# =========================
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# =========================
# WELCOME MESSAGE
# =========================
WELCOME_MESSAGE = """
🔥 أهلاً بك في بوت التحميل الاحترافي 🔥

📥 أرسل أي رابط فيديو وسيتم التحميل فورًا.

✅ يدعم:
• YouTube
• Instagram
• TikTok
• Facebook
• Twitter / X
• ومواقع كثيرة أخرى

⚡ سريع • احترافي • يعمل 24/7
"""

# =========================
# /start
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_MESSAGE)

# =========================
# DOWNLOAD FUNCTION
# =========================
async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):

    url = update.message.text

    loading = await update.message.reply_text(
        "⏳ جاري التحميل..."
    )

    try:

        ydl_opts = {
            "format": "best",
            "outtmpl": f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s",
            "quiet": True,
            "noplaylist": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(url, download=True)

            file_path = ydl.prepare_filename(info)

        title = info.get("title", "video")

        await loading.edit_text(
            f"✅ تم التحميل:\n\n🎬 {title}"
        )

        # لو الملف أقل من 49MB يرسله فيديو
        if os.path.getsize(file_path) <= 49 * 1024 * 1024:

            await update.message.reply_video(
                video=open(file_path, "rb")
            )

        else:

            await update.message.reply_document(
                document=open(file_path, "rb")
            )

        # حذف الملف بعد الإرسال
        os.remove(file_path)

    except Exception as e:

        await loading.edit_text(
            f"❌ حدث خطأ:\n\n{str(e)}"
        )

# =========================
# MAIN
# =========================
def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            download_video
        )
    )

    print("✅ Bot Running...")

    app.run_polling(
        poll_interval=3,
        timeout=30,
        bootstrap_retries=5
    )

# =========================
# START BOT
# =========================
if __name__ == "__main__":
    main()
