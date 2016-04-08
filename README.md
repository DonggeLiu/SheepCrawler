# SheepCrawler

If you are living in LuoYang(洛阳), China:

You can always visit www.ssqy.cc to win free/discount meals, hotel rooms, etc.

Or you can use this script to do that for you automatically. 


Before start:

1. Check if you have Python 3 installed. If not, you can use homebrew to install it:

	brew intall Python3

2. Check if you have BeautifulSoup4 installed. If not, you can use pip3 to install it:

	pip3 install beautifulsoup4

3. Check if you have requests installed. If not, you can use pip3 to install it:

	pip3 install requests

4. Change the 'txtUserName' and 'txtPassword' in the ssqy.py to your own username and password.

Recommendations:

1. You can run it directly in terminal with: Python3 ssqy.py or

2. Use Crontab to run it automatically, for example:

	  0 9 * * * /usr/local/bin/Python3 /Users/.../SSQY/ssqy.py
	
Remember using absolute path in Crontab.

Donation:

[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.me/DonggeLiu)







