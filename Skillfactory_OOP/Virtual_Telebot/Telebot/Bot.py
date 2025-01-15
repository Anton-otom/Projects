import telebot
from Token import TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, f"Welcome, {message.chat.username}")


#@bot.message_handler(content_types=['text'])
#def exo_bot(message):
#    bot.send_message(message.chat.id, f"Повторяю: {message.text}")


@bot.message_handler(content_types=['photo'])
def handle_photo(message: telebot.types.Message):
    bot.reply_to(message, 'Nice meme Xdd')


bot.polling(none_stop=True)
