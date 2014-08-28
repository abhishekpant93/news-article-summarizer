import json
import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist 
from nltk.corpus import stopwords
import unicodedata
corpusPath = '../scraper/nytimes_scraper/corpus/nytimes_corpus.json'
testFile = 'test';
teststr = "u'Two weeks after the killing of Michael Brown, we have become painfully familiar with his parents through their public appearances and television interviews, their faces drawn, their sorrow apparent.'"

def readFromFIle(fileName):
	f = open(fileName)
	ftest = open(testFile,'w')
	corpus = json.load(f)
	corpus = corpus
	print str((corpus[3]['text']))
	#print str(teststr)


readFromFIle(corpusPath);
