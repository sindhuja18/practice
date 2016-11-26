import urllib2
from bs4 import BeautifulSoup
import bs4

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
url = "https://gadgets360.com/shop/smartron-t-phone-sunrise-orange-313935322d33333935"
page = opener.open(url)
soup = BeautifulSoup(page.read(),'html.parser')
prices = soup.find('span', attrs={"class":"selling_price"})



# print(soup.prettify())

# for price in prices:
# 	for element in price.find_all("tr"):
# 		key = element.find_all('td', attrs={"class":"specsKey"})
# 		value = element.find_all('td', attrs={"class":"specsValue"})
# 		if key and value:
# 			print key[0].text,' :  ',value[0].text.strip()
# for price in prices:

strings = [x for x in prices if isinstance(x, (bs4.element.NavigableString)) and x.strip()]
if strings[0]:
	price = float(strings[0].replace(',',''))

print price