#! /usr/bin/env python
# coding:utf-8
#author: ID3055

import re
import sys

import requests

# reload(sys)
# sys.setdefaultencoding("utf-8")
# requests.packages.urllib3.disable_warnings()

class GithubLogin(object):
    def __init__(self, username, password):
        self.__username = username
        self.__password = password
        self.__cookie = None
        self.__session = requests.Session()
        self.__header = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Host": "github.com",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
        }
        self.__Login()

    def __getToken(self):
        html = self.__session.get('https://github.com/login', headers=self.__header)
        pattern = re.compile(r'authenticity_token[\s\S]*?value="([\s\S]*?)" />')
        authenticity_token = pattern.findall(html.content)[0]
        return authenticity_token

    def __Login(self):
        payload = {
            'login': self.__username,
            'password': self.__password,
            'commit': 'Sign+in',
            'authenticity_token': self.__getToken(),
            'utf8': '%E2%9C%93'
        }
        r = self.__session.post('https://github.com/session', data=payload, headers=self.__header)
        self.__cookie = r.cookies

    @property
    def cookie(self):
        return self.__cookie

    
if __name__ == '__main__':
    username = ''
    password = ''
    github = GithubLogin(username, password)
    cookie = github.cookie
    print cookie
