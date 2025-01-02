import logging
import re
from telegram import Update
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackContext
import joblib
import pandas as pd
import datetime as dt

# Log sozlamalari
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Modelni yuklash
model = joblib.load('models/ddos_rf_model.pkl')

# Ustun nomlari model uchun
encoded_column_names = [
    'ip.src_192.168.1.1', 'ip.dst_192.168.1.2', 'frame.len', 'tcp.flags.push',
    'ip.flags.df', 'Packets', 'Bytes', 'Tx Packets', 'Tx Bytes', 'Rx Packets', 'Rx Bytes'
]

# Guruh xabarlarini saqlash uchun vaqt bo‘yicha tarix
message_history = []

# Start komandasi uchun funksiya
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("🤖 Bot ishga tushdi! Salom!")

# Xabarlarni qayta ishlash funksiyasi
def process_message(update: Update, context: CallbackContext) -> None:
    global message_history

    # Xabar matnini olish
    text = update.message.text
    timestamp = dt.datetime.now()

    # IP manzillarni ajratish
    ip_addresses = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', text)
    if not ip_addresses:
        return  # Agar xabarda IP manzillar bo‘lmasa, qaytib chiqamiz

    # Matndagi ma'lumotlarni modelga moslashtirish
    frame_len = len(text)  # Xabar uzunligi
    packets = len(ip_addresses)  # IP manzillar soni
    data = {
        'ip.src': ip_addresses[0],
        'ip.dst': ip_addresses[1] if len(ip_addresses) > 1 else '0.0.0.0',
        'frame.len': frame_len,
        'tcp.flags.push': 0,  # Default qiymat
        'ip.flags.df': 1,  # Default qiymat
        'Packets': packets,
        'Bytes': frame_len * packets,
        'Tx Packets': packets // 2,
        'Tx Bytes': frame_len * (packets // 2),
        'Rx Packets': packets // 2,
        'Rx Bytes': frame_len * (packets // 2)
    }

    # Ma'lumotlarni DataFrame formatiga o‘tkazish
    user_data = pd.DataFrame([data], columns=encoded_column_names)

    # Bashorat qilish
    prediction = model.predict(user_data)[0]

    # Xabarni tarixga qo'shish
    message_history.append({'timestamp': timestamp, 'text': text, 'prediction': prediction})

    # Xabarlar tarixida hujum borligini aniqlash
    ddos_count = sum(msg['prediction'] for msg in message_history if (timestamp - msg['timestamp']).seconds < 60)
    if ddos_count > 5:  # 60 soniya ichida 5 dan ortiq DDoS hujum aniqlansa
        update.message.reply_text("⚠️ Guruhda DDoS hujumi aniqlangan! Tezda chora ko'ring!")

# Botni ishga tushirish
def main():
    TOKEN = "7934959141:AAH6rqlOq_sgbtMmTA76n1ZVwCaWxRQ-lsw"

    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Start komandasi uchun handler
    dispatcher.add_handler(CommandHandler("start", start))

    # Matn xabarlarini kuzatish uchun handler
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, process_message))

    # Botni ishga tushirish
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()


# from telegram import Bot
# from telegram.ext import ApplicationBuilder, MessageHandler, filters
# from inference import predict_ddos
# from utils import load_env

# # Muhit o‘zgaruvchilarini yuklash
# load_env()
# TOKEN = os.getenv("BOT_TOKEN")

# # Xabarlarni qayta ishlash funksiyasi
# async def process_message(update, context):
#     message = update.message.text  # Guruhdagi xabar matni
#     prediction = predict_ddos(message)  # Model orqali bashorat qilish

#     # Natija asosida javob
#     if prediction == 1:  # DDoS deb baholandi
#         await update.message.reply_text("⚠️ Ogohlantirish: DDoS hujumi aniqlandi!")
#     else:
#         await update.message.reply_text("✅ Xavfsiz: Xabar normal holatda.")

# async def send_start_message(application):
#     # Bot boshlanganda "Salom" xabarini yuboradi
#     chat_id = YOUR_CHAT_ID  # Guruh yoki foydalanuvchi ID'sini kiriting
#     bot = Bot(token=TOKEN)
#     await bot.send_message(chat_id=chat_id, text="🤖 Bot ishlayapti! Salom!")

# def main():
#     # Telegram botni ishga tushirish
#     application = ApplicationBuilder().token(TOKEN).build()

#     # Xabarlarni qayta ishlovchi handler
#     application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_message))

#     # Botni ishga tushirishdan oldin xabar yuborish
#     application.run_polling()
