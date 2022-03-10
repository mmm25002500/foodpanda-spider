#  -*- coding: utf-8 -*-
import bs4
import requests
import time
import os
import argparse
import sys

# help python2 main.py --help
parser=argparse.ArgumentParser(
    description='''(C) Copyright Cutespirit Team 2022(C)
		This is a Foodpanda-Spider which is made by TershiXia
		You can use this application to check the new stores or menus and prices.
		''',
    epilog="""You can edit all files or commercial used. Share it with your friends.
			Open Source Python Script.
		""")
parser.add_argument('-v','--version' ,action='version' , version = 'Tershi Foodpanda Version 1.5')
args=parser.parse_args()


CityURL= 'https://www.foodpanda.com.tw'
result = requests.get(CityURL)

sp = bs4.BeautifulSoup(result.content , "html.parser")								# 取的所有城市選單的HTML
all_a = sp.find_all("a",class_="city-tile")											# 取得連結子HTML
all_link = [CityURL+a.get("href") for a in all_a ]									# 得到一堆城市的網址
# print(all_link)																	# 印出所有城市連結 (串列)

for CityIndex in range(0,len(all_link)):											# 印出所有城市連結 (單個)
	# 城市
	# print(all_link[CityIndex])
	InCityResult = requests.get(all_link[CityIndex])								# 得到各地方城市的HTML
	all_CityTitle = sp.find_all("span" ,class_="city-name")							# 得到一堆城市的span程式
	all_CityTitleName = [c.text for c in all_CityTitle]								# 得到一堆城市的名字
	# print str(all_CityTitleName[]).decode("unicode-escape")						# Unicode反解
	print(u'地區:' + all_CityTitleName[CityIndex])									# 顯示台北市
	for title in range(0,len(all_CityTitleName)):									# 將所有城市的名字的數目下去做索引
		# 店家
		InCitySp = bs4.BeautifulSoup(InCityResult.content , "html.parser")			# 解析各程式HTML
		InCityAllA = InCitySp.find_all("a",class_="hreview-aggregate url")			# 查找所有a
		InCityAllLink = [CityURL + b.get("href") for b in InCityAllA]				# 將所有連結弄上來
		# print(InCityAllLink)														# 印出所有商店連結
		for StoreIndex in range(0,len(InCityAllLink)):								# 將所有商店連結的長度計次
			StoreResult = requests.get(InCityAllLink[StoreIndex])					# 將商店變成HTML
			StoreSp = bs4.BeautifulSoup(StoreResult.content, "html.parser")			# 解析
			StoreName = StoreSp.find_all("h1",class_="fn")							# 查找h1的類別為fn
			# print(StoreName)														# 印出店家HTML
			print(u'店家:' + StoreName[0].text)										# 印出店家
			print('\t產品:')															# 印出"產品"
			MainProduct = StoreSp.find_all("h3" ,class_="dish-name fn p-name")		# 查找品名稱
			for MainProductIndex in range(len(MainProduct)):						# 索引計次
				# print('\t\t'+MainProduct[MainProductIndex].text)					# 測試印出
				print('\t\t'+(MainProduct[MainProductIndex].text.replace('\n','')))	# 印出產品
				Price = StoreSp.find_all("span" , class_="price p-price")			# 尋找價格
				print(u"\t\t價格" + Price[MainProductIndex].text)					# 印出價格

