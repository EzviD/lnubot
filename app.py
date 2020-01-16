import telebot as tb
from random import randint,seed
from resources.parser import get_text, news_parse, f_parse, r_parse

#CONFIG
Token = "966190262:AAEJJpUkyV_AwbKV0HSjXb4qNuYxVv937GE"
url = "https://www.lnu.edu.ua/"
seed(1)
bot = tb.TeleBot(Token)

#COMMANDS
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,'''Hi there.
It is LNU website in Telegram for your comfort.\n
Enter /help to start''')

@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id,'''/help - list of commands,
/news - last news
/about - information about university
/facult - list of faculties
/rector - the current rector''')

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
    with open("tmp/about.txt","r",encoding='utf-8') as input:
        data = input.read()
        input.close()
    message_for_user = f"{data}\n{url}"
    bot.send_message(message.chat.id, message_for_user)

@bot.message_handler(commands=['facult'])
def facult(message):
    url = "https://www.lnu.edu.ua/about/faculties/"
    result = f_parse(url)

    _id=0
    for item in result:
        message_for_user = f'''{item[f'logo{_id}']}\n
    Адреса: {item[f'text{_id}'][0]}
    Телефон: {item[f'text{_id}'][1]}
    E-mail: {item[f'text{_id}'][2]}
    Сайт: {item[f'text{_id}'][3]}'''
        bot.send_message(message.chat.id, message_for_user)
        _id+=1

@bot.message_handler(commands=['rector'])
def rector(message):
    url = "https://www.lnu.edu.ua/about/administration/rector/"
    result = r_parse(url)

    message_for_user = f'''{result[0]['name']}\n
{result[0]['phone']}
E-mail: {result[0]['email']}\n
Стратегія розвитку:
{result[0]['strat']}'''
    bot.send_message(message.chat.id, message_for_user)

#CONTENT TYPES
@bot.message_handler(content_types=['text'])
def send_img(message):
    if message.text.lower() in ['lnu','лну']:
        photo = open(f'tmp/img/lnu/{randint(1,3)}.jpg','rb')
        bot.send_photo(message.chat.id, photo)

bot.polling()
