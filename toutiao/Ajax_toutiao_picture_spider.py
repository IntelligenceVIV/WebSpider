# @Time    : 2019/4/18 20:08
# @Author  : Noah
# @File    : Ajax_toutiao_picture_spider.py
# @Software: PyCharm
# @description: picture spider
import requests
from urllib.parse import urlencode


# from multiprocessing.pool import Pool


def get_page(offset):
    # 构造请求的GET参数
    params = {
        'offset': offset,
        'format': 'json',
        'keyword': '街拍',
        'autoload': 'true',
        'count': 20,
        'cur_tab': '1',
    }
    url = 'https://www.toutiao.com/api/search/content/?' + urlencode(params)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError:
        return None


def get_images(json):
    if json.get('data'):
        for item in json.get('data'):
            title = item.get('title')
            images = item.get('image_list')
            if images:
                for image in images:
                    yield {
                        'image': image.get('url'),
                        'title': title
                    }


def handle_Invalid_argument(filename):
    lst = list(filename)
    for i in lst:
        if i in ['|', '<', '>', '"', '/', '*', '!']:
            lst.remove(i)
    return ' '.join(lst)


def save_image(item):
    import os
    from hashlib import md5

    directory_name = handle_Invalid_argument(item.get('title'))
    if not os.path.exists(directory_name):
        os.mkdir(directory_name)

    try:
        response = requests.get(item.get('image'))
        if response.status_code == 200:
            file_path = '{0}/{1}.{2}'.format(directory_name, md5(response.content).hexdigest(), 'jpg')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(response.content)
            else:
                print("Already Download", file_path)

    except requests.ConnectionError:
        print("Failed to Save Image")


def main(offset):
    json = get_page(offset)
    for item in get_images(json):
        print(item)
        save_image(item)


GROUP_START = 1
GROUP_END = 20

if __name__ == "__main__":
    # pool = Pool()
    groups = ([x * 20 for x in range(GROUP_START, GROUP_END + 1)])
    for i in groups:
        main(i)
    # pool.map(main, groups)
    # pool.close()
    # pool.join()
