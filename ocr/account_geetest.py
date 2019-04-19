# @Time    : 2019/4/19 4:36
# @Author  : Noah
# @File    : account_geetest.py
# @Software: PyCharm
# @description: 实现极限验证码的识别过程
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

EMAIL = ''
PASSWORD = ''


class CrackGreet():
    def __init__(self):
        self.url = 'https://auth.geetest.com/login/'
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 20)
        self.email = EMAIL
        self.password = PASSWORD

def main():
    pass


if __name__ == "__main__":
    main()