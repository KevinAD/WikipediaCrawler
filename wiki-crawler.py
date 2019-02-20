from frontier import *
from webCrawlers import *

import requests, sys, time

#Print path with character replacements
def prettyPath(path):
	for url in path:
		print(url.replace("_"," ")[6:])

	
def breadthFirstSearch(startURL,destURL):
	
	#Set frontier
	frontier = Frontier(startURL)
	
	#While there are unexplored nodes
	while len(frontier.unexplored) > 0:
		#get current node to expand
		curNode = frontier.unexplored.pop(0)
		#For all neighbors of current node that have not been explored
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
	#If frontier runs out, return failed path
	return ['No Path']

#Bi-directional breadth first search		
def biDirectional(startURL,destURL):

	#Define frontiers
	forFront = Frontier(startURL) #Forward search from startURL
	invFront = Frontier(destURL) #Inverted search from destURL

	#While frontiers have unexplored nodes
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
	return ['No Path']		


#Check if verbose flag is set
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

#Set starting and ending urls for search
for i in range(1,3):
	if(sys.argv[i] == '-r' or sys.argv[i] == '--random'):
		randURL = requests.get(wikiBase+'/wiki/Special:Random').url[30:]
		sys.argv[i] = randURL
	
startURL = '/wiki/' + sys.argv[1].replace(" ","_")
destURL = '/wiki/' + sys.argv[2].replace(" ","_")

#Print information if verbose
if verbose:
	print("Start URL:",startURL)
	print("Destination URL:",destURL)
	print("Beginning Search...")
	startTime = time.time()

#Run search
path = biDirectional(startURL,destURL)

#Print search time and data
if verbose: print("Best path found in {} seconds!\n".format(time.time()-startTime))

#Print path
prettyPath(path)


		
