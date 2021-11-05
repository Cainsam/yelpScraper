from bs4 import BeautifulSoup
import requests
import copy
import re

# code adapted from https://levelup.gitconnected.com/scraping-yelp-data-with-python-and-beautiful-soup-39f9088bf633
def yelp_info(location, state):
	restaurant = []
	result = []
	headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
	url='https://www.yelp.com/search?cflt=restaurants&find_loc='+location+'%2C+'+state+'ns=1'
	response=requests.get(url,headers=headers)
	soup=BeautifulSoup(response.content, 'html.parser')
	for item in soup.select('[class*=container]'):
		test = 'none'
		if item.find('h4'):
			name = item.find('h4').get_text()
			for i in range(0, len(name) - 1):
				if name[i] == "\xa0":
					test = name[i+1:]
			if test == 'none':
				test = name

			restaurant.append(test)
			try:
				restaurant.append(item.select('[aria-label*=rating]')[0]['aria-label'])
			except:
				restaurant.append("Rating Info Not Available")
			try:
				restaurant.append(item.select('[class*=priceRange]')[0].get_text())
			except:
				restaurant.append("N/A")
			try:
				temp = 'none'
				details = (item.select('[class*=priceCategory]')[0].get_text())
				for i in range(0, len(details) - 1):
					if details[i] == '$':
						temp = details[:i]
						break
				if temp == 'none':
					temp = details

				res = re.sub("[a-z]+", lambda ele: ele[0] + " ", temp)
				res = re.sub(' +', ' ', res)
				res = res[:len(res) - 1]

				restaurant.append(res)


			except:
				restaurant.append("N/A")
			result.append(copy.deepcopy(restaurant))
			restaurant.clear()
	return result