from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from huggingface_hub import hf_hub_download
import os

# 🔑 Tokenlar
TOKEN = "8017914106:AAH37SYFd_hKz1BfzAct5dScXw_INGsUaL8"
HF_TOKEN = "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"

CHANNEL_ID = "-1002752698442"
BOT_USERNAME = "ebblender3D_bot"

# 📂 Modellar (hozircha faqat bitta)
models = {
    "villager": {
        "file": "Villager_Adventurer.zip",  # Hugging Face’dagi fayl nomi
        "photo": "https://i.postimg.cc/3rVzv27N/villager.jpg",  # test uchun rasm qo‘ydim
        "name": "🧑‍🌾 Villager Adventurer",
        "desc": "Blender uchun tayyorlangan Adventurer model.",
        "video": "https://www.youtube.com/shorts/HYlb8EwN7-s"
    }
}

# 📥 Hugging Face’dan modelni yuklab olish
def download_model(file_name):
    return hf_hub_download(
        repo_id="malikabegimqulova/ebblender-models",  # sizning repoingiz
        filename=file_name,
        token=HF_TOKEN
    )

# /start
def start_handler(update, context):
    args = context.args
    if args:
        model_id = args[0]
        if model_id in models:
            model = models[model_id]
            try:
                file_path = download_model(model["file"])
                with open(file_path, "rb") as f:
                    context.bot.send_document(
                        chat_id=update.message.chat_id,
                        document=f,
                        caption=f"📦 Mana siz so‘ragan {model['name']}!"
                    )
            except Exception as e:
                update.message.reply_text(f"❌ Yuklashda xatolik: {e}")
        else:
            update.message.reply_text("❌ Model topilmadi.")
    else:
        update.message.reply_text("Salom! Hozircha faqat `Villager Adventurer` modeli mavjud 🚀")

# /send
def send_project(update, context):
    if not context.args:
        update.message.reply_text("❌ Model nomini kiriting! Masalan: /send villager")
        return

    model_id = context.args[0]
    if model_id not in models:
        update.message.reply_text("❌ Bunday model topilmadi.")
        return

    model = models[model_id]

    keyboard = [[InlineKeyboardButton("📥 GET CODE", url=f"https://t.me/{BOT_USERNAME}?start={model_id}")]]
    if "video" in model:
        keyboard.append([InlineKeyboardButton("▶️ WATCH HERE", url=model["video"])])

    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_photo(
        chat_id=CHANNEL_ID,
        photo=model["photo"],
        caption=f"🎉 {model['name']}\n\n{model['desc']}",
        reply_markup=reply_markup
    )

    update.message.reply_text(f"✅ {model['name']} kanalga joylandi!")

def button_handler(update, context):
    query = update.callback_query
    query.answer()

# 🔄 Bot
updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("send", send_project))
dp.add_handler(CallbackQueryHandler(button_handler))
dp.add_handler(CommandHandler("start", start_handler))

updater.bot.delete_webhook(drop_pending_updates=True)
updater.idle()

