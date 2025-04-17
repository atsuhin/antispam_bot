from aiogram import dispatcher, types, Bot
import config as conf
import telebot

bot = telebot.TeleBot('7893229260:AAG34zlGRxu7x9DgSA91zXD7WGL8Y3KdCbo')
dp = dispatcher(bot)

@dp.message_handler()
async def mess_handler(message: types.Message):
    text = message.text.lower()
    for word in conf.WORDS:
        if word in text:
            await message.delete()

@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, 'Hello')

bot.infinity_polling()