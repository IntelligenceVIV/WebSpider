# @Time    : 2019/4/21 4:38
# @Author  : Noah
# @File    : youdao_words.py
# @Software: PyCharm
# @description: word translation
import random
import time

import requests
import json

HEADERS = {
    'Origin': 'http://fanyi.youdao.com',
    'Referer': 'http://fanyi.youdao.com/?keyfrom=dict2.index',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}

# change url =>  _o(x)
URL = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'


# Analysis
# var r = function(e) {
#         var t = n.md5(navigator.appVersion),
#         r = "" + (new Date).getTime(),
#         i = r + parseInt(10 * Math.random(), 10);
#         return {
#             ts: r,
#             bv: t,
#             salt: i,
#             sign: n.md5("fanyideskweb" + e + i + "@6f#X3=cCuncYssPsuRUE")
#         }
#     };


def encryption_function(sign):
    import hashlib

    md5 = hashlib.md5()
    md5.update(bytes(sign, encoding='utf-8'))
    sign = md5.hexdigest()
    return sign


def main(keyword):
    # salt = int(time.time() * 1000) + random.randint(0, 10)
    # sign = "fanyideskweb" + keyword + str(salt) + "@6f#X3=cCuncYssPsuRUE"
    # sign = encryption_function(sign)
    data = {
        'i': keyword,
        # 'salt': salt,
        # 'sign': sign,
        'doctype': 'json',
        # 'client': 'fanyideskweb',
        # 'keyfrom': 'fanyi.web'
    }
    try:
        response = requests.post(URL, data=data, headers=HEADERS)
        if response.status_code == 200:
            text = json.loads(response.text)
            text = text['translateResult'][0][0]['tgt']
            print('The {keyword} of the translation is: {text}'.format_map({'keyword': keyword, 'text': text}))
    except ConnectionError:
        print("Connection Error")


if __name__ == "__main__":
    while True:
        keyword = input("Please enter what you want to translate: ")
        if keyword == 'q':
            break
        main(keyword)
