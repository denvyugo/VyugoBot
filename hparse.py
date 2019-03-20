import requests
from bs4 import BeautifulSoup as bs


def get_links(hub_name):
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
            break
    return links


def parse_page(page_html, hub_name):
    #page_html = open_page()
    article_link = ''
    bs_obj: bs = bs(page_html, 'html.parser')
    bs_articles = bs_obj.find_all('article', {'class': 'post post_preview'})
    i = 0
    for article in bs_articles:
        bs_hubs = article.find_all('a', {'class': 'hub-link'})
        for a in bs_hubs:
            if a.text == hub_name:
                post_link = article.find('a', {'class': 'post__title_link'})
                article_link += '{}, {}\n'.format(post_link.text, post_link.get('href'))
    return article_link
