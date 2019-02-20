from frontier import *
from webCrawlers import *

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

