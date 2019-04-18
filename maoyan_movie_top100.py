# @Time    : 2019/4/18 18:03
# @Author  : Noah
# @File    : maoyan_movie_top100.py
# @Software: PyCharm
# @description: top100 movie spider
import time

import requests
from requests.exceptions import RequestException
import re
from pprint import pprint
import json
from multiprocessing import Pool


def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    pattern = re.compile(
        '<dd>.*?board-index.*?>(.*?)</i>'
        '.*?data-src="(.*?)"'
        '.*?name.*?a.*?>(.*?)</a>'
        '.*?star.*?>(.*?)</p>'
        '.*?releasetime.*?>(.*?)</p>'
        '.*?integer.*?>(.*?)</i>'
        '.*?fraction.*?>(.*?)</i>.*?</dd>', re.S
    )
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2].strip(),
            'actor': item[3].strip()[3:] if len(item[3]) > 3 else '',
            'time': item[4].strip()[5:] if len(item[4]) > 5 else '',
            'score': item[5].strip() + item[6].strip(),
        }


# write to file
def write_to_file(content):
    with open('result.text', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


# insert into mysql database
def insert_to_mysql_database(content):

    import pymysql.cursors

    # Connect to the database
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='147258',
                                 db='test',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `top100` (`title`, `score`, `index`, `actor`, `time`, `image`) " \
                  "VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (content['title'],
                                 content['score'],
                                 content['index'],
                                 content['actor'],
                                 content['time'],
                                 content['image'],))

        connection.commit()
    finally:
        connection.close()

# insert into mongo database
def insert_to_mongo_database(content):
    import pymongo

    client = pymongo.MongoClient("localhost", 27017)
    db = client.test
    collection = db['top100']
    collection.insert_one(content)


def main(offset):
    url = 'https://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        pprint(item)
        # write_to_file(item)
        # insert_to_mysql_database(item)
        insert_to_mongo_database(item)


if __name__ == "__main__":
    for i in range(10):
        main(offset=i * 10)
        time.sleep(1)
    # pool = Pool(processes=5)
    # pool.map(main, [i * 10 for i in range(10)])
