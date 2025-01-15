import telebot
from config import TOKEN

bot = telebot.Telebot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, f"Welcome, {message.chat.username}")


@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
    pass
