import telebot
from config import keys, TOKEN
from extensions import Converter, APIException


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    username = f'{message.from_user.first_name} {message.from_user.last_name}'
    bot.send_message(message.chat.id, f'<b>Hello</b>, <i>{username}</i>!\n<b>Commands:\
    </b>\n<i>/start\n/help\n/values</i>', parse_mode='html')


@bot.message_handler(commands=['help'])
def get_help(message: telebot.types.Message):
    bot.send_message(message.chat.id, f'<b>To get started, enter your request with the following format:</b>\n<i>\
1) currency name\n2) what currency to convert\n3) the amount of the converted currency</i>\n<b>\
For example:</b>\n<i>usd rub 100</i>', parse_mode='html')


@bot.message_handler(commands=['values'])
def get_values(message: telebot.types.Message):
    text_values = 'List of available currencies:'
    text_keys = ''
    for key in keys.keys():
        text_keys = '\n'.join((text_keys, key))
    bot.send_message(message.chat.id, f'<b>{text_values}</b><i>{text_keys}</i>', parse_mode='html')


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        quote, base, amount = message.text.lower().split(' ')
    except ValueError as e:
        bot.reply_to(message, f'<b>3 parameters required</b>', parse_mode='html')

    try:
        final = Converter.get_price(quote, base, amount)
        bot.send_message(message.chat.id, f'<b>{amount} {quote.upper()}</b> in <b>{base.upper()}</b>\
= <i>{final}</i>', parse_mode='html')
    except APIException as e:
        bot.reply_to(message, f'<b>User error:</b>\n<i>{e}</i>', parse_mode='html')


bot.polling(none_stop=True)
