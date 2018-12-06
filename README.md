# WechatRobot
 Replying message in wechat automatically and crawling silly photos when asking.

## TODO
 - [x] auto reply message in wechat by using [tuling robot]('http://www.tuling123.com/') api
 - [ ] crawl silly photo(planning to crawl weibo) (x)
   - [ ] simulatly login weibo (x)

## Modules
 - itchat: wechat api
 - requests: web request
 - parsel(Selector) (optional)
 - aiohttp (optional)

## Install dependencies
```
 pip install -r requirements.txt
```

## Run project 
```
 python wechat_robot.py
```
 Then, scanning the qrcode to login in.

## Friendship attachment(proxy needed)
 - pixiv photo crawling 
 - yandere photo crawling 