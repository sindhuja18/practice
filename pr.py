import urllib2
from bs4 import BeautifulSoup
import bs4

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
url = "https://gadgets360.com/shop/mobiles/smart-phone?sort=selling_price"
page = opener.open(url)
soup = BeautifulSoup(page.read(),'html.parser')
print soup
prices = soup.findall('span', attrs={"class":"acctual_price"})


# print prices.text

for x in prices:
	print x