from frontier import *
from webCrawlers import *
from searchFunctions import *

import requests, sys, time

#Print path with character replacements
def prettyPath(path):
	for url in path:
		print(url.replace("_"," ")[6:])

#Print search parameters
def printSearchParams():
	algorithmNames = ['Bi Directional Breadth First', 'Breadth First']
	print("Start URL: {}".format(wikiBase + startURL))
	print("Dest  URL: {}".format(wikiBase + destURL))
	print("Algorithm: {}".format(algorithmNames[algorithm]))
	if algorithm in [3]:
		print("Bound:     {}".format(bound))

#Print help page	
if(len(sys.argv) == 1 or sys.argv[1] == "-h" or sys.argv[1] == "--help"):
	helpMessage = """
Usage: wiki-crawler.py [options] <start URL> <destination URL>
Example: wiki-crawler.py -v -r -r
Example: wiki-crawler.py -v \"Colorado\" \"Chicago Cubs\"

Note: You only need to input the last part of the wikipedia URL, everything that comes after \"/wiki/\"

===== General Options =====
-h or --help			Display this help message and exit
-v or --verbose			Verbose ouput

===== URL replacements ====
-r or --random			Selects a random Wikipedia article, use in place of start or destination URL

==== Search Algorithms ====	Default algorithm is bi-directional breadth first search
-a <mode> or --algorithm <mode>	Selects search algorithm
-b <int>  or --bound <int>	Sets bound limit for bounded search (default: 6)

	Search Modes:
	0			Bi-directional breadth first search
	1			Breadth first search from start URL
	2			[NOT YET IMPLEMENTED] Inverted Breadth first search from goal URL
	3			[NOT YET IMPLEMENTED] Bounded depth first search
	"""
	print(helpMessage)
	exit()

#Remove "wiki-crawler.py" from list of args
sys.argv.pop(0)

#Define starting parameters
verbose = False
startURL = ""
destURL = ""
bound = 6
algorithm = 0

#assert that there are enough arguments
assert(len(sys.argv) >=2)

#Handle options
while(len(sys.argv) > 2):
	curArg = sys.argv.pop(0)
	
	if(curArg == '-v' or curArg == '--verbose'):
		verbose = True
	
	if(curArg == '-a' or curArg == '--algorithm'):
		try:
			assert(int(sys.argv[0]) in list(range(4)))
		except:
			print("Invalid algorithm mode {}.".format(sys.argv[0]))
			exit()
		
		algorithm = int(sys.argv.pop(0))
	if(curArg == '-b' or curArg == '--bound'):
		try:
			assert(int(sys.argv[0])>0)
		except:
			print("Invalid search bound {}.".format(sys.argv[0]))
			print("Must be positive integer.")
			exit()
		bound = int(sys.argv.pop(0))

#Assert that there are still enough arguments
try:
	assert(len(sys.argv) == 2)
except:
	print("Must specify starting URL and destination URL")
	print("Remaining Arguments: {}".format(sys.argv))
	exit()

#Handle start and dest URLs
for i,URL in enumerate(sys.argv):
	if URL == '-r' or URL == '--random':
		sys.argv[i] = getRandomArticle()

#assign URLs
startURL = ('/wiki/'+sys.argv[0]).replace(" ","_")
destURL  = ('/wiki/'+sys.argv[1]).replace(" ","_")

#Print params if verbose
if verbose: 
	printSearchParams()
	print("Starting search...\n")

startTime = time.time()

#Run search
path = ['No Path']
algorithms = [biDirectional,breadthFirstSearch]
path = algorithms[algorithm](startURL,destURL)
endTime = time.time()

if verbose: print("Path found in {} seconds!".format(endTime-startTime))
prettyPath(path)
exit()
if(algorithm == 0):
	path = biDirectional(startURL,destURL)
if(algorithm == 1):
	path = breadthFirstSearch(startURL,destURL)


		

	
