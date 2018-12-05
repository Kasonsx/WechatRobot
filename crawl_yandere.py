# -*- coding: utf-8 -*-
#yande.re网下载图片爬虫
import requests
from parsel import Selector
import os
tags = "asuna_%28sword_art_online%29"#搜索关键词，需要罗马音或英文,请百度
#url = 'https://yande.re/post?tags=' + tags
testurl = 'https://yande.re/post?page=1&tags=asuna_%28sword_art_online%29'#搜索亚丝娜

request_headers = {
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'Accept-Encoding':'gzip, deflate, br',
	'Accept-Language':'zh-CN,zh;q=0.8',
	'Connection':'keep-alive',
	'Cookie':'vote=1; login=Kason; pass_hash=9c33ce2689ebe2d3a61dec24ba47e5a4e23db9a0; forum_post_last_read_at=%221960-01-01T00%3A00%3A00.000Z%22; user_id=244389; user_info=244389%3B30%3B0; has_mail=0; comments_updated=1; block_reason=; resize_image=0; show_advanced_editing=0; my_tags=; held_post_count=0; country=CN; tag-script=; mode=view; yande.re=UHBQRDhadnZMZFV4cFVQMzRuNmJPa2lCK0ZKZm9jaHhhR1JFTHd3QVZrd1pMV09Ld0hscTBoYlZhRVdIZHZmMVI0dEI4bDdRQTB3Y2VFbkNVMXpGZHdWM1FVdzBwdVlIem1wZEFwNzJaeGlYTG9JYWJEcE1WTEh1dmVNUjNvUEE3YWwxQWpveEFSR1E0Z2dmTVU1MFZreHExbWJSV2hZSU5vdmZOOGpLVVRSSkx1R21tRDdUd1JPN2NacXNpajkzOXZXTlVEUXFKL2lUN3B2TCs4YVlaUT09LS01WklPN1BLZWUycWFpcUlMMG5xOU93PT0%3D--ee86537fcf268b5ff10f01aadd91083e4112b21e; __utmt=1; __utma=5621947.45632091.1505721323.1505721323.1505873619.2; __utmb=5621947.21.10.1505873619; __utmc=5621947; __utmz=5621947.1505721323.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic',
	'Host':'yande.re',
	'Referer':'https://yande.re/post',
	'Upgrade-Insecure-Requests':'1',
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36'
}
xpath = '//a[@class="directlink largeimg"]/@href'#图片地址
#pages = sel.xpath('//div[@class="pagination"]/a[last()-1]/text()').extract()[0]#总页码

def downloadImage(url):
	try:
		response = requests.get(url, headers=request_headers, timeout=10)
		if response.status_code == 200:
			sel = Selector(text=response.text)
			#print(sel.xpath(xpath).extract())#当前页的所有图片地址
			imageurls = []#保存所有图片链接
			for img in sel.xpath(xpath).extract():
				imageurls.append(img)
			saveUrls(imageurls)
			print("搜索完成")
	except requests.exceptions.ConnectionError:
		print("网络连接失败！")
	# print(response.text)
	
	# 下载图片：	
	# num = 1
	# amount = len(imageurls)
	# error = 0
	# print('开始下载图片...')
	# for i in imageurls:
	# 	filename = i.split('/')[-1]
	# 	try:
	# 		img = requests.get(i, headers=request_headers, timeout=10)
	# 	except requests.exceptions.ConnectionError:
	# 		print("当前图片 ",filename," 下载失败！")
	# 		error += 1
	# 		continue
	# 	# folder = os.path.join(os.path.abspath('.'),tags)
	# 	# os.makedirs(folder)
	# 	# os.chdir(folder)
	# 	print('正在下载当前页的第%s/%s张图片' % (num,amount))
	# 	with open(filename, 'wb') as f:
	# 		f.write(img.content)
	# 	num += 1
	# print('当前页有',error,'张图片下载失败！')
	# 获取下一页地址
	try:
		nextpage = sel.xpath('//div[@class="pagination"]/a[@class="next_page"]/@href').extract()[0]
		if nextpage:
			next_url = 'https://yande.re' + nextpage
			print(next_url)
			downloadImage(next_url)
	except IndexError:
		print("没有下一页了！")
# 保存图片链接
def saveUrls(imageurls):
	with open('ImageURLs.txt','a+') as f:
		for i in imageurls:
			f.write(i + "\r\n")

if __name__ == '__main__':
	# tags = input('输入搜索关键词的罗马音或英文')
	# url = 'https://yande.re/post?tags=' + str(tags)
	downloadImage(testurl)
	print('下载完成')


