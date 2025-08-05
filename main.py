import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_NAME = os.getenv("CHANNEL_NAME", "@yourchannelname")

# Список сигналов
signals = [
    {"pair": "EUR/USD", "action": "Buy", "confidence": "85%"},
    {"pair": "GBP/JPY", "action": "Sell", "confidence": "78%"},
    {"pair": "USD/CHF", "action": "Buy", "confidence": "91%"},
]

# Кнопки валют
currency_buttons = [
    ["EUR", "USD", "GBP"],
    ["JPY", "CHF", "AUD"],
    ["CAD"]
]

def build_keyboard():
    keyboard = [
        [InlineKeyboardButton(text=f"{base}/{quote}", callback_data=f"{base}/{quote}")
         for quote in row]
        for row in currency_buttons
        for base in currency_buttons[0]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Выберите валютную пару:", reply_markup=build_keyboard())

async def signal(update: Update, context: CallbackContext):
    message = "
".join([f"{s['pair']}: {s['action']} ({s['confidence']})" for s in signals])
    await context.bot.send_message(chat_id=CHANNEL_NAME, text=f"📊 Активные сигналы:
{message}")
    await update.message.reply_text("Сигналы отправлены в канал!")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))
    app.run_polling()

if __name__ == "__main__":
    main()