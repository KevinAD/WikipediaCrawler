import requests, sys, time
from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer

#Global variable base wikipedia url
wikiBase = 'https://en.wikipedia.org'

#Fetch random wikipedia article
def getRandomArticle():
	return requests.get(wikiBase+'/wiki/Special:Random').url[30:]

def fetchIncomingLinks(url):
	#So Wikipedia has a tool that shows what other articles link back to an article. It's essential for the bi directional algorithm
	formattedURL = 'https://en.wikipedia.org/w/index.php?title=Special%3AWhatLinksHere&limit=5000&target={}&namespace=0'.format(url[6:])
	page = requests.get(formattedURL) #get url html
	soup = bs(page.text, 'html.parser') #parse with bs4
	articleText = soup.find("ul",{"id":"mw-whatlinkshere-list"}) #extract mw-content-ltr div section
	return [link['href'] for link in articleText.find_all("a") if(link.has_attr('href')
									and "/wiki/" == link['href'][:6]
									)] #return all neighboring wikipedia articles

def fetchOutgoingLinks(url):
	#print("Getting neighbors of: {}".format(url))

	page = requests.get(url) #get url html
	soup = bs(page.text, 'html.parser') #parse with bs4
	articleText = soup.find("div",{"class":"mw-content-ltr"}) #extract mw-content-ltr div section
	return [link['href'] for link in articleText.find_all("a") if(link.has_attr('href') 
									and "/wiki/" == link['href'][:6] 
									and ":" not in link['href']
									and "#" not in link['href']
									and url != link['href'] 
									)] #return all neighboring wikipedia articles
