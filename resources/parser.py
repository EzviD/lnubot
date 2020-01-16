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
        id=0
        for item in sections:
            post = item.find('h2', {'class': 'post-title'})
            results.append({f'text{id}':post.text,
                            f'href{id}':post.find('a').get('href'),
                            f'date{id}':item.find('div',{'class':'post-date'}).text})
            id+=1
    else:
        results.append('There are no such news')

    return results
