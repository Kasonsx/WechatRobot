# -*- coding: utf-8 -*-
import requests

GET_INDEX_API = "https://m.weibo.cn/api/container/getIndex"

HEADER = {
    "Connection": "keep-alive",
    "Host": "passport.weibo.cn",
    "Upgrade-Insecure-Requests": "1",
    "Referer": "https://passport.weibo.cn/signin/login?entry=mweibo&r=http%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt=",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36"
}

AFTER_HEADER = {
    "Accept": "application/json, text/plain, */*",
    "Host": "m.weibo.cn",
    "Origin": "https://m.weibo.cn",
    "Referer": "https://m.weibo.cn/u/",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

class Weibo(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.request = requests.session()
        self.cookies = None
        self.st = None
        self.userid = None
    
    def login_for_sso(self):
        login_url = 'https://passport.weibo.cn/sso/login'
        data = {
            'username': self.username,
            'password': self.password,
            'savestate': '1',
            'r': 'http://weibo.cn/',
            'ec': '0',
            'pagerefer': '',
            'entry': 'mweibo',
            'wentry': '',
            'loginfrom': '',
            'client_id': '',
            'code': '',
            'qq': '',
            'mainpageflag': '1',
            'hff': '',
            'hfp': ''
        }
        headers = HEADER
        requestLogin = self.request.post(url=login_url, data=data, headers=headers)
        if not requestLogin.text.__contains__('20000000'):
            raise Exception('login for sso failed')

        self.cookies = requestLogin.cookies.get_dict()

    def get_uid(self):
        response = self.request.get(url='https://m.weibo.cn/', cookies=self.cookies)
        if response.status_code == 200 and response.text.__contains__('uid') > 0:
            self.userid = response.text[response.text.index('"uid":"') + len('"uid":"'):response.text.index('","ctrl"')]
    
    def get_st(self):
        response = self.request.get(url='https://m.weibo.cn/u/' + self.userid, cookies=self.cookies)
        if response.status_code == 200 and response.text.__contains__("st") > 0:
            _response = response.text
            if str(_response).__contains__("st: '") > 0:
                self.st = _response[_response.index("st: '") + len("st: '"): _response.index("',\n            login:")]
            elif str(_response).__contains__('"st":"') > 0:
                self.st = _response[_response.index('"st":"') + len('"st":"'):_response.index('","isInClient')]

    def check_cookie_expired(self):
        response = self.request.get(url='https://m.weibo.cn/', cookies=self.cookies)
        if response.status_code == 200:
            return response.text.__contains__(self.userid)
        return False

    def check_cookies(self):
        if self.cookies is None or not self.check_cookie_expired():
            return False
        return True

    def re_login(self):
        self.login_for_sso()
        self.get_uid()
        self.get_st()

    def _weibo_getIndex(self, userid):
        api = 'http://m.weibo.cn/api/container/getIndex'
        param = {"type": "uid", "value": userid}
        return self.request.get(url=api, params=param)

    def _weibo_content(self, containerid, page=1):
        api = "https://m.weibo.cn/api/container/getIndex"
        params = {"containerid": containerid, "page": page}
        return self.request.get(url=api, params=params)
