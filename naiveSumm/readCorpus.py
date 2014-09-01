import json
corpusPath = '../scraper/nytimes_scraper/corpus/nytimes_corpus.json'


def readFromFile(fileName):
	f = open(fileName)
	corpus = json.load(f)
	
	for i in range(0,len(corpus)):
		corpus[i]['headline'] = str(corpus[i]['headline'])
		corpus[i]['text'] = str(corpus[i]['text'])
		corpus[i]['keywords'] = str(corpus[i]['keywords'])
		

	#corpus = corpus
	#print str((corpus[0]['headline']))
	#print str(teststr)
	return corpus


readFromFile(corpusPath)
