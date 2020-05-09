import telebot
import random
import config

from telebot import types
bot = telebot.TeleBot('токен')

@bot.message_handler(content_types=['text'])

def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, сейчас мы проведём викторину.")
        
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('')
    item2 = types.KeyboardButton('')
    
    markup.add(item1, item2)
    
    bot.send_message(message.chat.id, 'лфлфлф', {0.first_name}!/
        parse_mode = 'html', reply_markup)
        
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "":
        bot.send_message(message.from_user.id, '')