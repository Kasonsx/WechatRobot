# -*- coding: utf-8 -*-
import itchat
import sys
from itchat.content import *
import requests
import os
import random

API_KEY = 'd1cfba0fde3c44208c1973cb4b88ab51'
os.chdir('./image/')
# get all photos' path once
file_list = [ x for x in os.listdir('.')]

def response(msg):#robot reply
	apiUrl = 'http://www.tuling123.com/openapi/api'
	data = {
		'key':API_KEY,
		'info':msg,
		'userid':'robot'
	}
	try:
		r = requests.post(apiUrl, data=data).json()
		code = r.get('code')
		result = '???'
		if code == 100000: #文本类 "text"就是回复内容
			result = r.get('text')
		elif code == 200000: #链接类 实际内容在"url"中
			result = "{0}\n{1}".format(r.get('text'),r.get('url'))
		return result
	except:
		print('server has encountered a problem.')

# 返回随机的图片路径
def get_imgUrl():
	# 本地图片库('project_root/image/')随机获取图片url
	# local directory
	# print(os.path.abspath('.'))
	rand_img = file_list[random.randrange(len(file_list))]
	img_path = os.path.join(os.path.abspath('.'), rand_img)
	return img_path

# 私聊回复
@itchat.msg_register(TEXT)
def auto_reply(msg):
	#print(msg.isAt)
	default_reply = 'I received:' + msg['Text']
	print(msg.FromUserName,':',msg['Text'])
	if msg.text.find('沙雕') != -1:
		# itchat.send_image('test.jpg', toUserName=msg.FromUserName)
		msg.user.send('@img@%s' % get_imgUrl())
		# msg.user.send('你是女娲捏出来的吗？')
	else:
		reply = response(msg['Text'])
		msg.user.send(reply or default_reply)

# 群聊回复，只有被@才回复
@itchat.msg_register(TEXT, isGroupChat = True)
def group_reply(msg):
	if msg.isAt:
		default_reply = 'I received:' + msg['Text']
		print(msg.FromUserName,':',msg['Text'])
		if msg.text.find('沙雕') != -1:
			msg.user.send('@img@%s' % get_imgUrl())
			# msg.user.send('你是女娲捏出来的吗？')
		elif msg.text == '':
			msg.user.send('???')
		else:
			reply = response(msg['Text'])
			msg.user.send(reply or default_reply)

def lc():#loginCallback
	print('login successfully!')
def ec():#exitCallback
	print('exit!')

itchat.auto_login(hotReload=True)

# 获取uin，用户或群聊的唯一标识
@itchat.msg_register(SYSTEM)
def get_uin(msg):
    if msg['SystemInfo'] != 'uins': return
    ins = itchat.instanceList[0]
    fullContact = ins.memberList + ins.chatroomList + ins.mpList
    print('** Uin Updated **')
    for username in msg['Text']:
        member = itchat.utils.search_dict_list(
            fullContact, 'UserName', username)
        print(('%s: %s' % (
            member.get('NickName', ''), member['Uin']))
            .encode(sys.stdin.encoding, 'replace'))

itchat.run()
