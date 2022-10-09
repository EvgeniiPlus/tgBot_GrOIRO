import json
import requests
from bs4 import BeautifulSoup
from config import url, headers


def parse():
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    news = soup.find('div', id='tab1').findAll('div', class_='item clearfix')
    return news


def get_news():
    news = parse()

    news_dict = {}
    for article in news:
        article_url = url + article.find('a', class_='preview').get('href')
        img_news = article.find('a', class_='preview').get('style')
        article_img = url + img_news[img_news.find("/"):-3]
        article_title = article.find('h3').find('a').text
        article_id = article_url[article_url.find('p-') + 2:-5]
        # print(f'{article_id}\n'
        #       f'{article_title}\n'
        #       f'{article_img}\n'
        #       f'{article_url}\n')

        news_dict[article_id] = {
            "article_title": article_title,
            "article_url": article_url,
            "article_img": article_img
        }

        with open('news_dict.json', 'w') as f:
            json.dump(news_dict, f, indent=4, ensure_ascii=False)


def check_news_update():
    with open('news_dict.json') as f:
        news_dict = json.load(f)
    news = parse()

    fresh_news = {}
    for article in news:
        article_url = url + article.find('a', class_='preview').get('href')
        article_id = article_url[article_url.find('p-') + 2:-5]

        if article_id in news_dict:
            continue
        else:
            article_url = url + article.find('a', class_='preview').get('href')
            img_news = article.find('a', class_='preview').get('style')
            article_img = url + img_news[img_news.find("/"):-3]
            article_title = article.find('h3').find('a').text

            news_dict[article_id] = {
                "article_title": article_title,
                "article_url": article_url,
                "article_img": article_img
            }

            fresh_news[article_id] = {
                "article_title": article_title,
                "article_url": article_url,
                "article_img": article_img
            }
    with open('news_dict.json', 'w') as f:
        json.dump(news_dict, f, indent=4, ensure_ascii=False)

    return fresh_news


def main():
    # get_news()
    print(check_news_update())


if __name__ == '__main__':
    main()
