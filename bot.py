from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.request import HTTPXRequest
from huggingface_hub import hf_hub_download
import os

# 🔑 Tokenlar
TOKEN = "8017914106:AAH37SYFd_hKz1BfzAct5dScXw_INGsUaL8"
HF_TOKEN = "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"
CHANNEL_ID = "-1002752698442"
BOT_USERNAME = "ebblender3D_bot"

# 📦 Mavjud modellarning ro‘yxati
models = {
    "blaster": {
        "file": "Blaster_Tri_Rocket_fbx.zip",
        "photo": "https://i.postimg.cc/c4KWCkLj/photo-2025-09-06-15-18-57.jpg",
        "name": "🚀 Blaster Tri Rocket",
        "desc": "Blender uchun Blaster Tri Rocket 3D modeli."
    },
    "bovine": {
        "file": "Robotic_Bovine_fbx.zip",  # 👈 agar .zip bo‘lsa shu nom
        "photo": "https://i.postimg.cc/KvHKmDTv/7a77126984340997c7baa3ab8f4a336e826ed4ae.jpg",
        "name": "🐄 Robotic Bovine",
        "desc": "Siz uchun Robotic Bovine 3D modeli tayyor!"
    }
}

# 📥 HuggingFace'dan model yuklash
def download_model(file_name):
    try:
        file_path = hf_hub_download(
            repo_id="malikabegimqulova/ebblender-models",  # 🔥 TO‘G‘RI REPO NOMI
            filename=file_name,
            token=HF_TOKEN
        )
        return file_path
    except Exception as e:
        print(f"❌ Yuklashda xatolik: {e}")
        return None

# 🚀 /start komandasi
async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if args:
        model_id = args[0]
        if model_id in models:
            model = models[model_id]
            file_path = download_model(model["file"])
            if file_path:
                try:
                    await update.message.reply_document(
                        open(file_path, "rb"),
                        caption=f"📦 Mana siz so‘ragan {model['name']}!"
                    )
                except Exception as e:
                    await update.message.reply_text(f"❌ Faylni yuborishda xatolik: {e}")
            else:
                await update.message.reply_text("❌ Modelni yuklab bo‘lmadi.")
        else:
            await update.message.reply_text("❌ Model topilmadi.")
    else:
        await update.message.reply_text("Salom! Hozircha faqat `safetensors` modeli mavjud 🚀")

# 📤 /send komandasi
async def send_project(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Model nomini kiriting! Masalan: /send safetensors")
        return

    model_id = context.args[0]
    if model_id not in models:
        await update.message.reply_text("❌ Bunday model topilmadi.")
        return

    model = models[model_id]
    keyboard = [[InlineKeyboardButton("📥 GET CODE", url=f"https://t.me/{BOT_USERNAME}?start={model_id}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_photo(
        chat_id=CHANNEL_ID,
        photo=model["photo"],
        caption=f"🎉 {model['name']}\n\n{model['desc']}",
        reply_markup=reply_markup
    )

    await update.message.reply_text(f"✅ {model['name']} kanalga joylandi!")

# 📌 Inline tugmalarni ishlovchi
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

# 🔧 Botni ishga tushirish
def main():
    # Timeout qo‘shildi (5 daqiqa kutadi)
    request = HTTPXRequest(connect_timeout=30.0, read_timeout=300.0)

    app = Application.builder().token(TOKEN).request(request).build()
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("send", send_project))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()

