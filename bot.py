import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ------------------------------
# تنظیمات لاگر برای مانیتور خروجی
# ------------------------------
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ------------------------------
# تعریف دستورات پایه
# ------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام 👋 من 🚦دستیار مجازی🚦 هستم، آماده‌ام!")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("لیست دستورات من به‌زودی اضافه می‌شود...")

# ------------------------------
# تابع اصلی
# ------------------------------
def main():
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    if not TELEGRAM_BOT_TOKEN:
        logger.error("❌ TELEGRAM_BOT_TOKEN environment variable not set.")
        raise ValueError("TELEGRAM_BOT_TOKEN not found.")

    # آدرس عمومی (همان لینک Replit)
    WEBHOOK_URL = f"https://dastyarmajazibot.mhghy92.repl.co/{TELEGRAM_BOT_TOKEN}"

    # ساخت اپلیکیشن
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # افزودن هندلرها
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_cmd))

    # اجرای سرور به صورت Webhook
    logger.info("🚀 Starting bot using Webhook Mode...")
    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),  # Replit معمولاً از پورت 8000 استفاده می‌کند
        url_path=TELEGRAM_BOT_TOKEN,
        webhook_url=WEBHOOK_URL
    )

# ------------------------------
# اجرای فایل
# ------------------------------
if __name__ == "__main__":
    main()
