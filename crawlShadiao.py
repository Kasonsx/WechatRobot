# -*- coding: utf-8 -*-
import requests
from parsel import Selector
import os


# 爬虫地址 weibo
url = 'https://m.weibo.cn/api/container/getIndex'


headers = {
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'Accept-Encoding':'gzip, deflate, br',
	'Accept-Language':'zh-CN,zh;q=0.8',
	'Connection':'keep-alive',
	'Cookie':'p_ab_id=7; p_ab_id_2=8; _ga=GA1.2.168375158.1505697943; device_token=1b69bf565a154a1b8f0284784a1709bb; login_ever=yes; __utma=235335808.168375158.1505697943.1505697943.1505697943.1; __utmc=235335808; __utmz=235335808.1505697943.1.1.utmcsr=link.zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=7424306=1^9=p_ab_id=7=1^10=p_ab_id_2=8=1^11=lang=zh=1; is_sensei_service_user=1; bookmark_tag_type=count; bookmark_tag_order=desc; howto_recent_view_history=64967449%2C65304741; a_type=0; b_type=1; PHPSESSID=7424306_720c4622895bfa72f0a7bb217d1321f6; module_orders_mypage=%5B%7B%22name%22%3A%22recommended_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22everyone_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22following_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22mypixiv_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22fanbox%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22featured_tags%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22contests%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22user_events%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22sensei_courses%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22spotlight%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22booth_follow_items%22%2C%22visible%22%3Atrue%7D%5D',
	'Host':'m.weibo.cn',
	'Referer':'https://m.weibo.cn/',
	'Upgrade-Insecure-Requests':'1',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

# 获取网页的selector用于xpath检索
def url_request(url):
	try:
		response = requests.get(url, headers=headers, timeout=10)
		#print(response.status_code)
		if response.status_code == 200:
			sel = Selector(text=response.text)
			return sel
	except requests.exceptions.ConnectionError:
		print("网络连接失败！")
	except requests.exceptions.ReadTimeout:
		print("连接超时！")

# 获取页面中所有图片的原图链接，默认jpg格式（部分原图为png需另外处理）
def get_img(url):
	selector = url_request(url)
	imageurls = []
	crawl_xpath = ''
	for img in selector.xpath(crawl_xpath).extract():
		if img is not None:
			imageurls.append(img)
	return imageurls

# 将获取的链接保存在本地文件中
def saveUrls(imageurls):
	with open('ImageURLs.txt','a+') as f:
		for i in imageurls:
			f.write(i + "\r\n")

# 跳转下一页
def nextpage(url):
	selector = url_request(url)
	next_xpath = ''
	next_page = selector.xpath(next_xpath).extract_first()
	nexturl = ""
	if next_page is not None:
		nexturl =  next_page
		print(nexturl)
	else:
		print("没有下一页了！")
	return nexturl

def justSaveUrls(url):
	num = 1
	while(url):
		imageurls = get_img(url)
		saveUrls(imageurls)
		url = nextpage(url)
		print("完成第%s页保存" % num)
		num += 1 

	print("保存链接完成！")

def onepage_urls(url):
	saveUrls(get_img(url))

# 下载图片，将原图为png格式的进行转化
def downloadImage(url):
	imageurls = get_img(url)
	#下载图片
	for img in imageurls:
		try:
			image = requests.get(img, headers=headers, timeout=10)
			if image.status_code != 200:
				img = img.replace('.jpg', '.png')
				image = requests.get(img, headers=headers, timeout=10)
		except:
			print("图片链接有误")
			
		filename = img.split('/')[-1]
		with open(filename, 'wb') as f:
			f.write(image.content)
		print("已下载好", filename)

if __name__ == '__main__':
	# downloadImage(url)
	# justSaveUrls(url) #保存所有链接
	onepage_urls(url) #保存特定页的链接
	# print('下载完成')

