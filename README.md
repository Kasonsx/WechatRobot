# WechatRobot
 Replying message in wechat automatically and crawling silly photos when asking.

## TODO
 - [x] auto reply message in wechat by using [tuling robot](http://www.tuling123.com/) api
 - [x] auto send photo when being @ and receiving a message that contains "沙雕"
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

## Run the robot 
```
 python wechat_robot.py
```
 Then, scanning the QR code to login in wechat.
 The account info will be stored in a local file to keep logined.

## Friendship attachment(proxy needed)
 - pixiv.net photo crawling 
 - yande.re photo crawling 