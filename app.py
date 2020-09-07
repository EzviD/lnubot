import telebot as tb
from random import randint,seed
from resources.parser import get_text, news_parse, f_parse, r_parse, c_parse, s_parse

#CONFIG
Token = "*"
url = "https://www.lnu.edu.ua/"
seed(1)
bot = tb.TeleBot(Token)

#COMMANDS
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,'''Hi there.
It is LNU Bot in Telegram for your comfort.\n
Enter /help to start''')

@bot.message_handler(commands=['help'])
def start_message(message):
    with open('tmp/commands.txt','r',encoding='utf-8') as output:
        message_for_user = output.read()
        output.close()
    bot.send_message(message.chat.id,message_for_user)

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
    with open("tmp/about.txt","r",encoding='utf-8') as output:
        data = output.read()
        output.close()
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

@bot.message_handler(commands=['contacts'])
def contact(message):
    url = "https://www.lnu.edu.ua/contacts/"
    result = c_parse(url)

    message_for_user = f'''{result[7]['text h3']}:\n{result[0]['text p']}\n
{result[8]['text h3']}:\n{result[1]['text p']}\n
{result[10]['text h3']}:\n{result[2]['text p']}
Email: {result[3]['text p']}\n
{result[10]['hrefs']}\n
{result[12]['text h3']}:\n{result[4]['text p']}
{result[12]['hrefs']}\n
{result[14]['text h3']}:\n{result[5]['text p']}
{result[14]['hrefs']}\n
{result[16]['text h3']}:
{result[16]['hrefs']}\n
{result[17]['text h3']}:
{result[17]['hrefs']}\n
Author: @ezvidu4'''
    bot.send_message(message.chat.id,message_for_user)


#CONTENT TYPES
@bot.message_handler(content_types=['text'])
def send_msg(message):
    if message.text.lower() in ['lnu','лну']:
        photo = open(f'tmp/img/lnu/{randint(1,3)}.jpg','rb')
        bot.send_photo(message.chat.id, photo)
    elif len(message.text.split()) >= 3:
        info = message.text.lower().split() #info - [faculty, surname, name]
        faculty = ' '.join(info[:-2])
        info.append(faculty) #info - [FALSE, surname, name, faculty]
        with open('tmp/staff.txt','r',encoding='utf-8') as output:
            _str = output.read()
            output.close()
        dict = eval(_str)
        try:
            url = dict[info[-1]]
            result = s_parse(url)
            flag = False
            for item in result:
                if item['name']==info[-3:-1]:
                    bot.send_message(message.chat.id, item['href'])
                    flag = True
            if flag:
                    flag = False
            else:
                bot.send_message(message.chat.id, 'Wrong input information')
        except KeyError:
            bot.send_message(message.chat.id, 'Wrong input information.')

if __name__ == '__main__':
    bot.polling()
