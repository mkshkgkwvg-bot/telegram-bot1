import os
import instaloader
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    print("BOT_TOKEN is missing!")
    exit()

loader = instaloader.Instaloader()


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
        if "youtube.com" in url or "youtu.be" in url:
            await update.message.reply_text("⏳ جاري تحميل الفيديو من يوتيوب...")

            ydl_opts = {
                'outtmpl': 'video.mp4',
                'format': 'best'
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            await update.message.reply_document(document=open("video.mp4", "rb"))

            os.remove("video.mp4")
            return

        # 📌 إنستجرام
        if "instagram.com" in url:
            await update.message.reply_text("⏳ جاري تحميل من إنستجرام...")

            shortcode = url.split("/")[-2]
            post = instaloader.Post.from_shortcode(loader.context, shortcode)

            loader.download_post(post, target="downloads")

            files = os.listdir("downloads")
            file_path = os.path.join("downloads", files[0])

            await update.message.reply_document(document=open(file_path, "rb"))

            # تنظيف
            for f in files:
                os.remove(os.path.join("downloads", f))

            return

        await update.message.reply_text("❌ ابعت لينك إنستجرام أو يوتيوب صحيح")

    except Exception as e:
        await update.message.reply_text(f"⚠️ حصل خطأ: {str(e)}")


# 🟢 تشغيل البوت
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot is running...")
app.run_polling()
