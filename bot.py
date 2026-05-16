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
⌁︙آهلا بكَِ اغاتي في بوت الانستكرام 🤍
⌁︙يمكنك ايضاً التحميل من ( اليوتيوب ، انستكرام ، تيكتوك ، فيسبوك ، تويتر ، سناب شات ، ساوند كلاود )

⌁︙تكدر تحمل اي شي يعجبك بسهولة تامة 🔥
⌁︙لتحميل المقاطع ارسل رابط الفيديو 🎞️
⌁︙لحميل الستوريات او الهايلايت ارسل يوزر المستخدم الى البوت 👤" "" 


# 🟢 Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(MENU_TEXT)


# 🟢 الرسائل
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
            await update.message.reply_text("⏳ خد نفسك واهدى كده يابا ببعت لك الفيديو انا اهو..")

            ydl_opts = {
                "outtmpl": "insta.%(ext)s",
                "format": "best",
                "quiet": True
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            await update.message.reply_document(open("insta.mp4", "rb"))
            os.remove("insta.mp4")
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

            await update.message.reply_document(open("tiktok.mp4", "rb"))
            os.remove("tiktok.mp4")
            return

        await update.message.reply_text("❌ الرابط غلط يبني ابعت رابط صح ومتتعبناش")

    except Exception as e:
        await update.message.reply_text(f"⚠️ خطأ: {str(e)}")


# 🟢 يوتيوب (فيديو + صوت)
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    action, url = query.data.split("|")

    try:
        # 📹 فيديو
        if action == "video":
            await query.message.reply_text("⏳ اهدي شويه ببعت الفديو اهو..")

            ydl_opts = {
                "outtmpl": "video.mp4",
                "format": "best",
                "noplaylist": True
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            await query.message.reply_document(open("video.mp4", "rb"))
            os.remove("video.mp4")

        # 🎧 صوت
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

            await query.message.reply_audio(open("audio.mp3", "rb"))
            os.remove("audio.mp3")

    except Exception as e:
        await query.message.reply_text(f"⚠️ خطأ: {str(e)}")


# 🟢 تشغيل البوت
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_handler(CallbackQueryHandler(button_handler))

print("Bot is running...")
app.run_polling()
