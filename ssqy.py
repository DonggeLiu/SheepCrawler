from bs4 import BeautifulSoup
import requests
import json
import re
import time

headers = { 'Content-Type' : 'application/x-www-form-urlencoded' }
sheepCount = 0
QUANTITY = 1



def zhuaYang():
	for i in range(294, 700):
		time.sleep(1)
		url = 'http://www.ssqy.cc/goods_show.aspx?id=' + str(i)
		commoditySite = user.get(url)
		user.close()
		commodityPage = commoditySite.text
		soup = BeautifulSoup(commodityPage, "html.parser")
		
		if pick(soup, i) :
			sheep = Yang(soup)
			if sheep != None:
				qianYang(sheep)


def pick(soup, i):
	# 236: 猫工厂， 486: 粤品烧鹅, 664: 德恒楼, 319: 九姑娘酸菜鱼, 672: 快乐的鱼
	if i in [236, 486, 664, 319, 672]:
		print("ID = "  + str(i) + ': Not Interested')
		return False

	if soup.find(id = 'commodityArticleId') == None:
		print('ID = ' + str(i) + ': Empty')
		return False
		

	if (soup.find(specid="10") or soup.find(specid="9")) == None:
		print('ID = ' + str(i) + ': Far')
		return False

	print('ID = ' + str(i) + ':')
	return True



# Fetch Info of Yang
def Yang(soup):

	# Collect commodityGoodscategoryId
	commodityGoodscategoryIdTag = soup.find(id = 'commodityGoodscategoryId')
	commodityGoodscategoryIdPartern = re.compile('<input id="commodityGoodscategoryId" type="hidden" value="(.*)"/>')
	commodityGoodscategoryIdContent = str(commodityGoodscategoryIdTag)
	commodityGoodscategoryId = commodityGoodscategoryIdPartern.search(commodityGoodscategoryIdContent).group(1)
	
	# 100: lessons; 84: beauty salon; 42, 49, 50, 78, 96, 99: hotel; 89: flower shop; 104, 106: foot-club; 92: pets; 54: KTV； 61: internet cafe; 91: Tea Art; 107: Dancing Club;
	# 108: photo studio, 86, 83: car repairing, 88: cigarette, 112: piano
	if commodityGoodscategoryId in ['100', '84', '42', '49', '50', '78', '96', '99', '89', '104', '106', '92', '54', '61', '91', '107', '108', '86', '83', '88', '112']:
		print( 'Not Interested')
		return None

	print( 'Category: ' + commodityGoodscategoryId)

	# Collect commodityArticleId
	commodityArticleIdTag = soup.find(id = 'commodityArticleId')
	commodityArticleIdPartern = re.compile('<input id="commodityArticleId" type="hidden" value="([0-9]*)"/>')
	commodityArticleIdContent = str(commodityArticleIdTag)
	commodityArticleId = int(commodityArticleIdPartern.search(commodityArticleIdContent).group(1))

	# Collect commodityArticleTitle
	commodityArticleTitleTag = soup.find(id = 'commodityArticletitle')
	commodityArticleTitlePartern = re.compile('<input id="commodityArticletitle" type="hidden" value="(.*)"/>')
	commodityArticleTitleContent = str(commodityArticleTitleTag)
	commodityArticleTitle = commodityArticleTitlePartern.search(commodityArticleTitleContent).group(1)
	print( 'Name: ' + commodityArticleTitle)

	sheep = {
		'commodityGoodscategoryId': commodityGoodscategoryId,
		'commodityArticleId': commodityArticleId,
		'commodityArticleTitle': commodityArticleTitle
	}

	return sheep




# Click QianYang Button
def qianYang(sheep):
	
	global sheepCount

	clickData = {
		"article_id": sheep['commodityArticleId'],
		"quantity": QUANTITY,
		"goods_title": sheep['commodityArticleTitle'],
		"category_id": sheep['commodityGoodscategoryId']
		}
	try:
		t = user.post("http://www.ssqy.cc/tools/submit_ajax.ashx?action=order_save_qy", data=clickData, headers=headers, timeout = 20)
	except requests.exceptions.Timeout:
		print( "Timeout")
	print( t.text)
	sheepCount += 1
	print( 'sheepCount : ' + str(sheepCount))


def login(userInfo):

	# specify we're sending parameters that are url encoded
	global user
	
	user = requests.Session()
	r = user.post("http://www.ssqy.cc/tools/submit_ajax.ashx?action=user_login&site=main", data=userInfo, headers=headers)

	print( userInfo['txtUserName'])
	print( r.text)

	print( 'sheepCount : ' + str(sheepCount))
	return user



if __name__ == '__main__':

	# user1 parameters
	userInfo = {
		'txtUserName': 'yourUsername',
		'txtPassword': 'yourPassword',
		'btnSubmit': 'btnSubmit'
	}
	login(userInfo)
	zhuaYang()

	print( 'Finished! caught ' + str(sheepCount) + ' sheep')


	

