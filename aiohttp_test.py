# -*- coding: utf-8 -*-
import time
import math
import random
import aiohttp
import asyncio
import json

global headers
headers = {
    'Host': 'passport.weibo.cn',
    'Connection': 'keep-alive',
    'Content-Length': '152',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Origin': 'https://passport.weibo.cn',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Mobile Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': '*/*',
    'Referer': 'https://passport.weibo.cn/signin/login',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': 'coutSecond=48; _T_WM=96b6649536f2756bfa5bcde465ecc195; login=94000d604ad0525dbebede421661941a; WEIBOCN_FROM=1110005030; MLOGIN=0; M_WEIBOCN_PARAMS=uicode%3D10000011%26fid%3D231583'
}

url = 'https://m.weibo.cn/api/container/getIndex'
params = b'uid=5108265142&luicode=10000011&lfid=100103type%3D1%26q%3D%E6%B2%99%E9%9B%95%E5%9B%BE&type=uid&value=5108265142&containerid=1076035108265142'
uid = '5108265142'
luicode = '10000011'
lfid = '100103type=1&q=沙雕图'
type = 'uid'
value = '5108265142'
containerid = '1076035108265142'

async def prelogin(session):
    pre_url = 'https://login.sina.com.cn/sso/prelogin.php'
    params = {
        'checkpin':'1',
        'entry':'mweibo',
        'su':'MTY2NzU1NDE2ODc=',
        'callback':'jsonpcallback' + str(int(time.time() * 1000) + math.floor(random.random() * 100000))
    }
    response = await session.post(pre_url,params=params)
    async with response:
        if response.status == 200:
            print('Login page')
            print(response.text)

async def login(session):
    login_url = 'https://passport.weibo.cn/sso/login'
    account = input("Account:")
    password = input("Password:")
    params = {
        'username': account,
        'password': password,
        'savestate':'1',
        'r':'',
        'ec':'0',
        'pagerefer':'',
        'entry':'mweibo',
        'wentry':'',
        'loginfrom':'',
        'client_id':'',
        'code':'',
        'qq':'',
        'mainpageflag':'1',
        'hff':'',
        'hfp':''
    }
    response = await session.post(login_url,params=params)
    async with response:
        if response.status == 200:
            print('Login successfully.')
            js = response.json()
            formatedData = json.loads(js)
            print(formatedData)

async def getData(session,url):
    headers['Host'] = "login.sina.com.cn"
    async with session.post(url,data=b'uid=5108265142&luicode=10000011&lfid=100103type%3D1%26q%3D%E6%B2%99%E9%9B%95%E5%9B%BE&type=uid&value=5108265142&containerid=1076035108265142') as response:
        return await response.json()

async def main_session(url,headers):
    async with aiohttp.ClientSession(headers=headers) as session:
        await prelogin(session)
        await login(session)
        content = await getData(session,url)
        print(content)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_session(url,headers))


