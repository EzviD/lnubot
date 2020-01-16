import telebot as tb
from resources.parser import get_text, news_parse

Token = "966190262:AAEJJpUkyV_AwbKV0HSjXb4qNuYxVv937GE"
url = "https://www.lnu.edu.ua/"
bot = tb.TeleBot(Token)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,'''Hi there.
It is LNU website in Telegram for your comfort.\n
Type /help to start''')

@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id,'''/help - list of commands,
/news - last news
/about - information about university''')

@bot.message_handler(commands=['news'])
def news(message):
    url='https://www.lnu.edu.ua/news/all/'
    result = news_parse(url)
    if result is not None:
        _id=0
        for item in result:
            message_for_user = f'''{item[f'text{_id}']}\n\n{item[f'href{_id}']}\n{item[f'date{_id}']}'''
            bot.send_message(message.chat.id, message_for_user)
            _id+=1
    else:
        bot.send_message(message.chat.id, 'Sorry,but there are no such results.')

@bot.message_handler(commands=['about'])
def about(message):
    with open("tmp/about.txt","r") as input:
        data = input.read()
        input.close()
    message_for_user = f"{data}\n{url}"
    bot.send_message(message.chat.id, message_for_user)

bot.polling()
