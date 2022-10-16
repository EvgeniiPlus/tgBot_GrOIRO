import json
import requests
from bs4 import BeautifulSoup
from config import url, headers


def parse():
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    announces = soup.find('div', class_='panel hot_announces').findAll('div', class_='item clearfix')
    return announces


def get_announcements():
    announcements = parse()

    ann_dict = {}
    for ann in announcements:
        ann_url = url + ann.find('a').get('href')
        ann_title = ann.find('a').text
        ann_id = ann_url[ann_url.find('p-') + 2: -5]
        ann_date = ann.find('div', class_ = 'date').text

        ann_dict[ann_id] = {
            'ann_title': ann_title,
            'ann_url': ann_url,
            'ann_date': ann_date
        }

        with open('ann_dict.json', 'w') as f:
            json.dump(ann_dict, f, indent=4, ensure_ascii=False)

    return ann_dict

def check_ann_update():
    with open('ann_dict.json') as f:
        ann_dict = json.load(f)

    announcements = parse()
    fresh_anns = {}
    for ann in announcements:
        ann_url = url + ann.find('a').get('href')
        ann_id = ann_url[ann_url.find('p-') + 2: -5]

        if ann_id in ann_dict:
            continue
        else:
            ann_title = ann.find('a').text
            ann_date = ann.find('div', class_='date').text

            ann_dict[ann_id] = {
                'ann_title': ann_title,
                'ann_url': ann_url,
                'ann_date': ann_date
            }
            fresh_anns[ann_id] = {
                'ann_title': ann_title,
                'ann_url': ann_url,
                'ann_date': ann_date
            }
    with open('ann_dict.json', 'w') as f:
        json.dump(ann_dict, f, indent=4, ensure_ascii=False)

    return fresh_anns

def main():
    # get_announcements()
    check_ann_update()


if __name__ == '__main__':
    main()
