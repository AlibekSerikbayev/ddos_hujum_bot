import os
from telegram.ext import Updater, MessageHandler, Filters
from inference import predict_ddos
from utils import load_env

# Muhit o‘zgaruvchilarini yuklash
load_env()
TOKEN = os.getenv("BOT_TOKEN")

# Xabarlarni qayta ishlash funksiyasi
def process_message(update, context):
    message = update.message.text  # Guruhdagi xabar matni
    prediction = predict_ddos(message)  # Model orqali bashorat qilish

    # Natija asosida javob
    if prediction == 1:  # DDoS deb baholandi
        update.message.reply_text("⚠️ Ogohlantirish: DDoS hujumi aniqlandi!")
    else:
        update.message.reply_text("✅ Xavfsiz: Xabar normal holatda.")

def main():
    # Telegram botni ishga tushirish
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Xabarlarni qayta ishlovchi handler
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, process_message))

    # Botni ishga tushirish
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
