from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import os

TOKEN = "8017914106:AAH37SYFd_hKz1BfzAct5dScXw_INGsUaL8"
CHANNEL_ID = "-1002752698442"
BOT_USERNAME = "ebblender3D_bot"  # @ belgisisiz yoziladi

# 📂 Modellar ro‘yxati
models = {
    "trophy": {
        "file": "C:\\Users\\B-SMART\\MyBot\\models\\trophy_final.zip",
        "photo": "https://i.postimg.cc/tTTtNXDr/photo-2025-08-25-19-29-07.jpg",
        "name": "🏆 Trophy Final",
        "desc": "Bu 3D trophy modeli Blender uchun tayyorlangan.",
    },
    "house": {
        "file": "C:\\Users\\B-SMART\\MyBot\\models\\Bladesong Whisper.zip",
        "photo": "https://i.postimg.cc/wjyvqn0D/Country-Garden-Farmhouse-Watercolor-Clipart-Farmhouse-clipart-Country-Bundle-PNG-House-watercol.jpg",
        "name": "🏠 Uy modeli",
        "desc": "Bu 3D uy modeli Blender uchun tayyorlangan."
        # ❌ video yo‘q, shuning uchun WATCH HERE chiqmaydi
    },
    "medieval": {
        "file": "C:\\Users\\B-SMART\\MyBot\\models\\Medieval_Armor_Jacket.zip",
        "photo": "https://i.postimg.cc/9f9Y78F7/photo-2025-08-31-14-22-27.jpg",
        "name": "🛡️ Orta asr zirh modeli",
        "desc": "Bu modelni bot orqali OBJ va FBX formatlarda yuklab olishingiz mumkin.",
        "video": "https://www.youtube.com/shorts/HYlb8EwN7-s"
    }
}

# /start buyrug‘i orqali ZIP faylni yuborish
def start_handler(update, context):
    args = context.args
    if args:
        model_id = args[0]
        if model_id in models:
            model = models[model_id]
            file_path = model["file"]

            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    context.bot.send_document(
                        chat_id=update.message.chat_id,
                        document=f,
                        caption=f"📦 Mana siz so‘ragan {model['name']}!"
                    )
            else:
                update.message.reply_text("❌ Fayl topilmadi. Iltimos, yo‘lni tekshiring.")
        else:
            update.message.reply_text("❌ Bunday model topilmadi.")
    else:
        update.message.reply_text("Salom! Model yuklab olish uchun kanal tugmasini bosing. 🚀")

# /send <model_id> orqali kanalga post joylash
def send_project(update, context):
    if not context.args:
        update.message.reply_text("❌ Model nomini kiriting! Masalan: /send trophy")
        return

    model_id = context.args[0]
    if model_id not in models:
        update.message.reply_text("❌ Bunday model topilmadi.")
        return

    model = models[model_id]

    # 🔘 Tugmalar dinamik yaratiladi
    keyboard = [[InlineKeyboardButton("📥 GET CODE", url=f"https://t.me/{BOT_USERNAME}?start={model_id}")]]
    if "video" in model:  # faqat agar video bo‘lsa
        keyboard.append([InlineKeyboardButton("▶️ WATCH HERE", url=model["video"])])

    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_photo(
        chat_id=CHANNEL_ID,
        photo=model["photo"],
        caption=f"🎉 {model['name']}\n\n{model['desc']}",
        reply_markup=reply_markup
    )

    update.message.reply_text(f"✅ {model['name']} kanalga joylandi!")

# Callback tugma (hozircha ishlatilmayapti)
def button_handler(update, context):
    query = update.callback_query
    query.answer()

# 🔄 Botni ishga tushirish
updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("send", send_project))   # /send <model_id>
dp.add_handler(CallbackQueryHandler(button_handler))
dp.add_handler(CommandHandler("start", start_handler))

updater.start_polling()
updater.idle()
