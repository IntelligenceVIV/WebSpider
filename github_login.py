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
LOGIN_SUCCESS_HOST = 'https://github.com/settings/profile'

HEADERS = {
    'Referer': 'https://github.com/',
    'Host': 'github.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
}


class Login(object):
    def __init__(self):
        self.session = requests.session()

    def get_token(self):
        response = self.session.get(LOGIN_HOST, headers=HEADERS, verify=False)
        result = response.text
        token = re.findall(r'<input type="hidden" name="authenticity_token" value="(.*?)" />', result)
        if token:
            self.token = token[0]

    def login(self, email, password):

        self.get_token()

        data = {
            'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_token': self.token,
            'login': email,
            'password': password,
        }
        response_login = self.session.post(SESSION_HOST, headers=HEADERS, data=data, verify=False)
        if response_login.status_code == 200:
            self.dynamics(response_login.text)

        response_profile = self.session.get(LOGIN_SUCCESS_HOST, headers=HEADERS, verify=False)
        if response_profile.status_code == 200:
            self.profile(response_profile.text)

    def dynamics(self, text):
        pass
    def profile(self, text):
        pass


if __name__ == "__main__":
    login = Login()
    login.login('email', 'password')
