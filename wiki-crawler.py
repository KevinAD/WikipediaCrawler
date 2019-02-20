from frontier import *
from webCrawlers import *

import requests, sys, time
from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer

def prettyPath(path):
	for url in path:
		print(url.replace("_"," ")[6:])

	
def breadthFirstSearch(startURL,destURL):

	frontier = Frontier(startURL)
	
	while len(frontier.unexplored) > 0:
		curNode = frontier.unexplored.pop(0)
		for neighbor in fetchOutgoingLinks(wikiBase+curNode.url):
			if neighbor not in frontier.explored:
				#Create new node with url and pointer back to parent
				newNode = Node(neighbor,curNode)
				
				#If neighbor url is destination, return full path.
				if newNode.url == destURL:
					return fetchFullPath(newNode)
				#Otherwise update unexplored and explored
				frontier.unexplored.append(newNode)
				frontier.explored.append(neighbor)
	return []
		
#Poopy Trash Garbage. Doesn't work cuz im dumb boy
def biDirectional(startURL,destURL):

	forFront = Frontier(startURL) #Forward search from startURL
	invFront = Frontier(destURL) #Inverted search from destURL

	while(len(forFront.unexplored) > 0 and len(invFront.unexplored) > 0):
		#Forward search from start url
		curNode = forFront.unexplored.pop(0)
		for neighbor in fetchOutgoingLinks(wikiBase+curNode.url):
			#Create new node with url and pointer back to parent
			newNode = Node(neighbor,curNode)
			
			#If neighbor url is destination, return full path.
			for invertNode in invFront.unexplored:
				if newNode.url == invertNode.url:
					return fetchFullPath(newNode) + list(reversed(fetchFullPath(invertNode)))[1:]
			#Otherwise update unexplored and explored
			forFront.unexplored.append(newNode)
			forFront.explored.append(neighbor)

		#Inverted search from destination url
		curNode = invFront.unexplored.pop(0)
		for neighbor in fetchIncomingLinks(curNode.url):
			#Create new node with url and pointer back to parent
			newNode = Node(neighbor,curNode)
			
			#If neighbor url is destination, return full path.
			for forwardNode in forFront.unexplored:
				if newNode.url == forwardNode.url:
					return fetchFullPath(forwardNode) + list(reversed(fetchFullPath(newNode)))[1:]
			#Otherwise update unexplored and explored
			invFront.unexplored.append(newNode)
			invFront.explored.append(neighbor)
	return []		
					
assert(len(sys.argv) >= 3)

startURL = '/wiki/' + sys.argv[1].replace(" ","_")
destURL = '/wiki/' + sys.argv[2].replace(" ","_")

if("-v" in sys.argv or "--verbose" in sys.argv):
	verbose = True
	#Clean this up later
	try:
		sys.argv.remove("-v")
	except:
		pass
	try:	
		sys.argv.remove("--verbose")
	except:
		pass
else:
	verbose = False

if verbose:
	print("Start URL:",startURL)
	print("Destination URL:",destURL)
	print("Beginning Search...")
	startTime = time.time()
path = biDirectional(startURL,destURL)
if verbose: print("Best path found in {} seconds!\n".format(time.time()-startTime))
prettyPath(path)





		
