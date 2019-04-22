import requests
from bs4 import BeautifulSoup as bs
import os
from datetime import date

articles_ids = []

def get_links(hub_name, path):
    check_file(path)
    links = ''
    headers = {'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
    base_url = 'https://habr.com/ru/top/page'
    i = 1
    while True:
        url = base_url + str(i)
        try:
            get_page = requests.get(url, headers=headers)
            if get_page.status_code == 200:
                links += parse_page(get_page.text.encode('utf-8'), hub_name=hub_name)
                i += 1
            else:
                break
        except Exception as e:
            print(e)
    rewrite_ids()
    return links


def parse_page(page_html, hub_name):
    article_link = ''
    bs_obj: bs = bs(page_html, 'html.parser')
    bs_articles = bs_obj.find_all('article', {'class': 'post post_preview'})
    for article in bs_articles:
        bs_hubs = article.find_all('a', {'class': 'hub-link'})
        for a in bs_hubs:
            if a.text == hub_name:
                post_link = article.find('a', {'class': 'post__title_link'})
                if post_link.get('href') not in articles_ids:
                    articles_ids.append(post_link.get('href'))
                    article_link += '{}, {}\n'.format(post_link.text, post_link.get('href'))
    return article_link


def rewrite_ids():
    file_name = get_filename()
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(';'.join(articles_ids))


def get_filename():
    date_today = date.today()
    filename = date_today.strftime('%Y%m%d') + 'ids.txt'
    return filename


def check_file(dir_name):
    global articles_ids
    file_name = get_filename()
    if os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            articles_ids = f.read().split(';')
    else:
        _delete_ids(dir_name)
        with open(file_name, 'w', encoding='utf-8') as f:
            pass

def _delete_ids(dir_name):
    for root, dirs, names in os.walk(dir_name):
        for name in names:
            if 'ids.txt' in name:
                os.remove(os.path.join(root, name))
