# -*- coding: utf-8 -*-
import aiohttp
import asyncio

headers = {
    'Host': 'm.weibo.cn',
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Mobile Safari/537.36',
    'Referer': 'https://m.weibo.cn/u/5108265142?uid=5108265142&luicode=10000011&lfid=100103type%3D1%26q%3D%E6%B2%99%E9%9B%95%E5%9B%BE',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': '_T_WM=96b6649536f2756bfa5bcde465ecc195; WEIBOCN_FROM=1110006030; MLOGIN=0; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D100103type%253D1%2526q%253D%25E6%25B2%2599%25E9%259B%2595%25E5%259B%25BE%26fid%3D1076035108265142%26uicode%3D10000011'
}


url = 'https://m.weibo.cn/api/container/getIndex'
params = b'uid=5108265142&luicode=10000011&lfid=100103type%3D1%26q%3D%E6%B2%99%E9%9B%95%E5%9B%BE&type=uid&value=5108265142&containerid=1076035108265142'
uid = '5108265142'
luicode = '10000011'
lfid = '100103type=1&q=沙雕图'
type = 'uid'
value = '5108265142'
containerid = '1076035108265142'

async def init(session):
    config_url = 'https://m.weibo.cn/api/config'
    resp = await session.get(config_url)
    async with resp:
        if resp.status == 200:
            return resp.headers

async def getData(session,url):
    async with session.post(url,data=b'uid=5108265142&luicode=10000011&lfid=100103type%3D1%26q%3D%E6%B2%99%E9%9B%95%E5%9B%BE&type=uid&value=5108265142&containerid=1076035108265142') as response:
        return await response.json()

async def main_session(url,headers):
    async with aiohttp.ClientSession(headers=headers) as session:
        init_resp = await init(session)
        print(init_resp)
        content = await getData(session,url)
        print(content)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_session(url,headers))


