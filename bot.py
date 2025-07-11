import telebot
import os

TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID"))

bot = telebot.TeleBot(TOKEN)

appointments = []

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام! برای ثبت نوبت لطفاً پیام بده: \n\nنام + تاریخ + ساعت + خدمات")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    if message.chat.id != GROUP_ID:
        return

    text = message.text.strip()
    if text.startswith("ویرایش "):
        try:
            parts = text.split(" ", 2)
            index = int(parts[1]) - 1
            new_text = parts[2]
            appointments[index] = new_text
            bot.reply_to(message, f"✅ نوبت شماره {index+1} ویرایش شد.")
        except:
            bot.reply_to(message, "خطا در ویرایش. فرمت صحیح: ویرایش 1 متن جدید")
    elif text == "لیست نوبت‌ها":
        if not appointments:
            bot.reply_to(message, "هنوز نوبتی ثبت نشده.")
        else:
            reply = "\n".join([f"{i+1}. {a}" for i, a in enumerate(appointments)])
            bot.reply_to(message, "📅 لیست نوبت‌ها:\n" + reply)
    else:
        appointments.append(text)
        bot.reply_to(message, f"✅ نوبت ثبت شد. شماره {len(appointments)}")

bot.infinity_polling()
