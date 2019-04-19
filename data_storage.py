# @Time    : 2019/4/19 17:39
# @Author  : Noah
# @File    : data_storage.py
# @Software: PyCharm
# @description: (1) TXT、JSON、CSV (2) MySQL、MongoDB、Redis
import requests
from pyquery import PyQuery as pq

URL = 'https://www.zhihu.com/explore'

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}


def get_one_page():
    try:
        html = requests.get(url=URL, headers=HEADERS)
        if html.status_code == 200:
            return html.text
    except ConnectionError:
        print("Connection Failed")


html = get_one_page()

doc = pq(html)

items = doc('.explore-tab .feed-item').items()

for item in items:
    question = item.find('h2').text()
    author = item.find('.author-link-line').text()
    answer = pq(item.find('.content').html()).text()

    # Stored as text
    # with open('explore.txt', 'a', encoding='utf-8') as file:
    #     file.write('\n'.join([question, author, answer]))
    #     file.write('\n' + '=' * 50 + '\n')

    with open('explore.json', 'a', encoding='utf-8') as file:
        file.write('\n'.join([question, author, answer]))
        file.write('\n' + '=' * 50 + '\n')
