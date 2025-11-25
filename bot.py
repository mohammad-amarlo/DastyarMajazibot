    import logging
    import os
    from telegram import Update
    from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
    from fastapi import FastAPI
    import uvicorn
    import asyncio
    import nest_asyncio

    nest_asyncio.apply()

    # توکن ربات شما
    # برای امنیت، این توکن را از "Secrets" (متغیرهای محیطی) Replit دریافت می‌کنیم.
    # اگر در Secrets تنظیم نشده بود، از توکن پیش‌فرض شما استفاده می‌شود.
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8447298172:AAGIPXwUuC1FdJ7-nwuCrs8njTMSH5ee_I4")

    # پورتی که وب‌سرور ربات شما روی آن گوش می‌کند.
    # Replit خودش یک پورت را اختصاص می‌دهد که از طریق متغیر محیطی PORT در دسترس است.
    PORT = int(os.environ.get("PORT", "8000"))

    # تنظیمات لاگ‌گیری برای نمایش اطلاعات در کنسول Replit
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )
    logger = logging.getLogger(__name__)

    # تابع هندلر برای دستور /start
    async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """پیام خوشامدگویی هنگام اجرای دستور /start."""
        user = update.effective_user
        await update.message.reply_html(
            rf"سلام خالق من {user.mention_html()}! من دستیار مجازی تو هستم و آماده خدمت.",
        )

    # تابع هندلر برای پاسخ به پیام‌های متنی (مثلاً echo)
    async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """پیام کاربر را تکرار می‌کند."""
        await update.message.reply_text(update.message.text)

    def main() -> None:
        """شروع به کار ربات."""
        application = Application.builder().token(TOKEN).build()
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

        # اجرای ربات در حالت Webhook
        # Replit این وب‌سرور را میزبانی می‌کند و یک آدرس عمومی به آن می‌دهد.
        application.run_webhook(
            listen="0.0.0.0", # گوش دادن روی همه رابط‌های شبکه داخلی Replit
            port=PORT,
            url_path=TOKEN # مسیری که تلگرام درخواست‌ها را به آن می‌فرستد (برای امنیت بیشتر)
        )

        logger.info(f"ربات بر روی پورت {PORT} در حالت Webhook شروع به کار کرد.")
        logger.info("پس از شروع به کار Replit، باید Webhook URL نهایی را به تلگرام معرفی کنید.")


    if __name__ == "__main__":
        main()
