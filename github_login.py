# @Time    : 2019/4/17 18:17
# @Author  : Noah
# @File    : github_login.py
# @Software: PyCharm
# @description: login github
import requests
import re
import urllib3

# forbid SSL warning => https and http
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LOGIN_HOST = 'https://github.com/login'
SESSION_HOST = 'https://github.com/session'


class Login(object):
    def __init__(self):
        self.session = requests.session()

    def get_token(self):
        response = self.session.get(LOGIN_HOST, verify=False)
        result = response.text
        token = re.findall(r'<input type="hidden" name="authenticity_token" value="(.*?)" />', result)
        if token:
            self.token = token[0]

    def login(self):
        data = {
            'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_token': self.token,
            'login': '',  # 账号
            'password': '',  # 密码
        }
        response = self.session.post(SESSION_HOST, data=data, verify=False)
        code = response.status_code
        if code == 200:
            print('login success')
        else:
            print('login failure')


if __name__ == "__main__":
    login = Login()
    login.get_token()
    login.login()
