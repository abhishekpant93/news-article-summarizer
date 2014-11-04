import networkx as nx
import numpy as np
import nltk
import math
import json
from nltk.tokenize import sent_tokenize 
from nltk.tokenize.punkt import PunktSentenceTokenizer
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer

# for error:  Resource u'tokenizers/punkt/english.pickle' not found
# see:	http://stackoverflow.com/questions/4867197/failed-loading-english-pickle-with-nltk-data-load

corpusPath = '../scraper/nytimes_scraper/corpus/nytimes_corpus.json'
summaryPath = '../resource/summary/nytimes_corpus_summary.json'
numberOfLines = 5
fractionOfLines = 0.3
takeFraction = True 

def textrank(document):
	sentences = sent_tokenize(document) 
	bow_matrix = CountVectorizer().fit_transform(sentences)
	normalized = TfidfTransformer().fit_transform(bow_matrix)
	similarity_graph = normalized * normalized.T
	nx_graph = nx.from_scipy_sparse_matrix(similarity_graph)
	scores = nx.pagerank(nx_graph)
	sent_score = [0.0 for x in xrange(len(scores))]
	for i in xrange(len(scores)):
		sent_score[i] = scores[i]
	# return  sorted(((scores[i],i,s) for i,s in enumerate(sentences)),
	  # reverse=True)
	# if len(sentences)/3>10:
	# 	K = 10
	# else:
	# 	K = len(sentences)/3
	# final = sorted(((scores[i],i,s) for i,s in enumerate(sentences)), reverse=True)[0 : K +1]
	# print "Pagerank"
	# for x in final:
	# 	print x[2]
	return sent_score

def getTextOrderKey(item):
	return item[1]
	
def summarise(document):
	topK=0
	sortedSencence = textrank(document)
	for k in sortedSencence:
		print (k)
	if takeFraction:
		topK = int(math.ceil(fractionOfLines*len(sortedSencence)))
	else:
		if(numberOfLines>len(sortedSencence)):
			topK=len(sortedSencence)
		else:
			topK=numberOfLines
	# print topK
	del(sortedSencence[topK:])
	return sorted(sortedSencence, key=getTextOrderKey)

def readFromFile(fileName):
	f = open(fileName)
	corpus = json.load(f)
	f.close()	
	for i in range(0,len(corpus)):
		corpus[i]['headline'] = str(corpus[i]['headline'])
		corpus[i]['text'] = str(corpus[i]['text'])
		corpus[i]['keywords'] = str(corpus[i]['keywords'])
	#corpus = corpus
	#print str((corpus[0]['headline']))
	#print str(teststr)
	return corpus
	
def summariseWholeCorpus():
	corpus = readFromFile(corpusPath)
	for i in range(1,len(corpus)):
		print i;
		#temperory if. To be removed once corpus contatins no news with empty text
		if(len(corpus[i]['text'])<5): 
			corpus[i]['summary']=""
			corpus[i]['summaryLength']=0
			continue;

		sentences = summarise(corpus[i]['text'])
		a=""
		for x in sentences:
			a+=x[2]
		corpus[i]['summary']=a
		corpus[i]['summaryLength']=len(sentences)
	fwrite = open(summaryPath,'w')
	json.dump(corpus,fwrite,indent=0)
	fwrite.close()


if __name__ == "__main__":

	#summariseWholeCorpus()
	corpus = readFromFile(corpusPath)
	sentences = summarise(corpus[2702]['text'])
	a=""
	for x in sentences:
		a+=x[2]
	corpus[2702]['summary']=a
	print len(sentences)