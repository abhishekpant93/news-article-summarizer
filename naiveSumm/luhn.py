import nltk
import math
import json
from nltk.tokenize import sent_tokenize 
from nltk.tokenize.punkt import PunktSentenceTokenizer
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
import re
import operator

number_of_lines = 5
fraction_of_lines = 3
take_fraction = True

def luhn_summarizer(document):

	stop_words_list = stopwords.words('english')
	doc_word_list = re.split(r'[,;.\s]\s*',document)
	sentences = sent_tokenize(document)
	st = LancasterStemmer()
	
	word_frequency_dict = dict()
	for sent in sentences:
		sent_word_list = re.split(r'[,;.\s]\s*',sent)
		for (i,word) in enumerate(sent_word_list):
			if len(word)==0 or word.lower() in stop_words_list:
				continue
			stem_word = st.stem(word)
			if stem_word in word_frequency_dict.keys():
				word_frequency_dict[stem_word] = word_frequency_dict[stem_word]+1
			else:
				word_frequency_dict[stem_word] = 1
			if i!=0 and word[0].isupper()==True:
				word_frequency_dict[stem_word] = word_frequency_dict[stem_word] + 0.2 #Adhoc weight

	print word_frequency_dict

	sentence_scores = [[0.0,x] for x in xrange(len(sentences))]
	for (i,sent) in enumerate(sentences):
		sent_word_list = re.split(r'[,;.\s]\s*',sent)
		if len(sent_word_list) <= 5: #Eliminate sentences of less than 5 words
			continue
		significance_vector = []
		for word in sent_word_list:
			if len(word)==0:
				continue
			if word.lower() in stop_words_list:
				significance_vector.append(0)
			stem_word = st.stem(word)
			print stem_word
			if stem_word in word_frequency_dict.keys():
				stem_word_freq = word_frequency_dict[stem_word]
			else:
				stem_word_freq = 0
			if(stem_word_freq>1):
				significance_vector.append(stem_word_freq)
			else:
				significance_vector.append(0)
		print word_frequency_dict
		cluster_score = []
		blankCount = 0
		clusterCount = 0
		clusterSum = 0
		for idx in xrange(len(significance_vector)):
			clusterSum  = clusterSum+significance_vector[idx]
			clusterCount = clusterCount+1
			if significance_vector[idx]==0:
				blankCount = blankCount+1
			if(blankCount>4):
				cluster_score.append(clusterSum/(clusterCount**2))
				blankCount=0
				clusterCount=0
				clusterSum=0
		if clusterCount>0:
			cluster_score.append(clusterSum/(clusterCount**2))
		sentence_scores[i][0] = max(cluster_score)

	sorted_list = sorted(sentence_scores,reverse=True)
	topK = []

	#Can swap out number_of_lines for fraction of article lines here
	for i in xrange(number_of_lines):
		topK.append([sorted_list[i][1],sorted_list[i][0]])
	final_sent_list = sorted(topK)

	for sent_score in final_sent_list:
		print sentences[sent_score[0]]





			