import requests
from bs4 import BeautifulSoup

def get_text(url):
    r = requests.get(url)
    text=r.text
    return text

#PARSER FOR NEWS
def news_parse(url):
    results = []
    text = get_text(url)
    soup = BeautifulSoup(text,features="lxml")

    sections = soup.find_all('section',{'class':['post with-image clearfix','post no-image clearfix']})
    if sections:
        _id=0
        for item in sections:
            post = item.find('h2', {'class': 'post-title'})
            results.append({f'text{_id}':post.text,
                            f'href{_id}':post.find('a').get('href'),
                            f'date{_id}':item.find('div',{'class':'post-date'}).text})
            _id+=1
    else:
        results.append('There are no such news')

    return results

#PARSER FOR FACULTIES
def f_parse(url):
    results = []
    text = get_text(url)
    soup = BeautifulSoup(text,features="lxml")

    sections = soup.find_all('li',{'class':'clearfix'})
    if sections:
        _id=0
        for item in sections:
            post = item.find('div',{'class':'details'}).find_all('p')
            results.append({f'logo{_id}':item.find('h2', {'class':'title'}).text,
                            f'text{_id}':[x.find('span',{'class':'value'}).text for x in post]})
            _id+=1
    else:
        results.append('There are no such faculties')

    return results

#RECTOR PARSER
def r_parse(url):
    results = []
    text = get_text(url)
    soup = BeautifulSoup(text,features="lxml")

    section = soup.find('div',{'class':'vc_row wpb_row vc_row-fluid'})
    results.append({'name':soup.find('h2',{'class':'name'}).find('strong').text,
                    'phone':soup.find('p',{'class':'phone'}).text,
                    'email':soup.find('p',{'class':'email'}).find('a').text,
                    'strat':section.find_all('a',{'rel':'noopener noreferrer'})[1].get('href')})

    return results

#CONTACTS PARSER
def c_parse(url):
    results = []
    text = get_text(url)
    soup = BeautifulSoup(text,features="lxml")

    paragraph = soup.find_all('p')
    headers = soup.find_all('h3')
    for item in paragraph:
        results.append({'text p':item.text})

    for item in headers:
        if item.find('a'):
            a = item.find('a')
            results.append({'text h3':a.text,
                            'hrefs':a.get('href')})
        else:
            results.append({'text h3':item.text,
                            'hrefs': None})

    return results

#STAFF PARSER
def s_parse(url):
    results = []
    text = get_text(url)
    soup = BeautifulSoup(text,features="lxml")

    section = soup.find('article',{'class':'content staff'})
    names = section.find_all('td',{'class':'name'})
    for item in names:
        a = item.find('a')
        results.append({'name':a.text.lower().split()[0:2],
                        'href':a.get('href')})

    return results
