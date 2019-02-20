from webCrawlers import *
class Node:
	def __init__(self, url, parent):
		self.url = url
		self.parent = parent

class Frontier:
	def __init__(self,baseURL,inverted = False):
		self.explored = []
		self.unexplored = [Node(baseURL,None)]



def fetchFullPath(node):
	path = []

	curNode = node
	while curNode != None:
		path.append(curNode.url)
		curNode = curNode.parent
	return list(reversed(path))
