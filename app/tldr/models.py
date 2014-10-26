from django.db import models

import networkx as nx
import numpy as np
import nltk
import math
from nltk.tokenize import sent_tokenize 
from nltk.tokenize.punkt import PunktSentenceTokenizer
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer

class Summarizer(models.Model):

	numberOfLines = 5
	fractionOfLines = 0.3
	takeFraction = True 

	@staticmethod
	def textrank(document):
		sentences = sent_tokenize(document) 
		bow_matrix = CountVectorizer().fit_transform(sentences)
		normalized = TfidfTransformer().fit_transform(bow_matrix)
		similarity_graph = normalized * normalized.T
		nx_graph = nx.from_scipy_sparse_matrix(similarity_graph)
		scores = nx.pagerank(nx_graph)
		return  sorted(((scores[i],i,s) for i,s in enumerate(sentences)),
		  reverse=True)

	@staticmethod
	def getScore(item):
		return item[0]	

	@staticmethod
	def getTextOrderKey(item):
		return item[1]

	@staticmethod
	def getText(item):
		return item[2]		

	@staticmethod
	def summarize(document):
		topK=0
		sortedSencence = Summarizer.textrank(document)

		if Summarizer.takeFraction:
			topK = int(math.ceil(Summarizer.fractionOfLines*len(sortedSencence)))
		else:
			if(Summarizer.numberOfLines>len(sortedSencence)):
				topK=len(sortedSencence)
			else:
				topK=Summarizer.numberOfLines
		# print topK
		del(sortedSencence[topK:])
		values =  sorted(sortedSencence, key=Summarizer.getTextOrderKey)
		result = [ Summarizer.getText(sentence) for sentence in values]
		del values
		return result

