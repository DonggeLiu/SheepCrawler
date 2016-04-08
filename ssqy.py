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
	# Place the ids of shops that you are not interested in [] below
	if i in [9999,9998]:
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
	
	# Place the ids of the categories you are not interested in the [] below. Use '' to quote them.
	if commodityGoodscategoryId in ['9999','9998']:
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


	

