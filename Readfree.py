#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import requests
from bs4 import BeautifulSoup
from PIL import Image

try:
    import cookielib
except:
    import http.cookiejar as cookielib

# 构造 Request headers
agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'
headers = {
    "Host": "readfree.me",
    "Referer": "http://readfree.me/accounts/login/?next=/",
    'User-Agent': agent
}

# Get the soup and ready for cookie
all_url = 'http://readfree.me/accounts/login/?next=/'
s = requests.session()
s.cookies = cookielib.LWPCookieJar(filename='cookies')
try:
    s.cookies.load(ignore_discard=True)
except IOError:
    print('Cookie未加载！')

rq = s.get(url=all_url, headers=headers)
soup = BeautifulSoup(rq.text, 'lxml')


def get_csrf():
    _csrf = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
    return _csrf


def get_captcha1():
    curl = soup.find('img', {'class': 'captcha'})['src']
    captcha_url = 'http://readfree.me/captcha/image' + curl
    response = s.get(captcha_url, headers=headers)
    with open('captcha.jpg', 'wb') as f:
        f.write(response.content)
        f.close()
    im = Image.open('captcha.jpg')
    im.show()
    im.close()
    captcha = input('captcha code： ')
    return captcha


def get_captcha0():
    captchacode = soup.find('input', {'name': 'captcha_0'})['value']
    return captchacode


def login(email, password):
    # Post the login imformation to the server
    data = {
        'csrfmiddlewaretoken': get_csrf(),
        'email': email,
        'password': password,
        'captcha_1': get_captcha1(),
        'captcha_0': get_captcha0(),
    }
    result = s.post(all_url, data=data, headers=headers)
    s.cookies.save(ignore_discard=False, ignore_expires=False)


# To verfy the login
def is_login():
    if os.path.isfile('username.txt'):
        user_name = open('username.txt', 'r', encoding='utf-8').read()
    else:
        user_name = str(input('请输入你的用户名\n>  '))
        with open('username.txt', 'w', encoding='utf-8') as f:
            f.write(user_name)

    purl = 'http://readfree.me/accounts/profile/' + user_name + '/checkin/'
    login_code = s.get(
        purl, headers=headers, allow_redirects=False).status_code
    if login_code == 200:
        return True
    else:
        return False


def sign():
    sign_url = 'http://readfree.me/accounts/checkin'
    sign_code = requests.get(sign_url).status_code
    if sign_code == 200:
        return True
        print('签到成功')
    else:
        return False
        print('签到失败')


if __name__ == '__main__':
    if is_login():
        print('您已经登录')
        sign()
        print('签到成功')
    else:
        print('登录失败')
        account = input('请输入你的邮箱\n>  ')
        secret = input('请输入你的密码\n>  ')
        login(account, secret)
        print('请再次运行此脚本')
