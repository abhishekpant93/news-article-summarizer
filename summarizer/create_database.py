import sys
sys.path.insert(0, '../naiveSumm/')
sys.path.insert(1, '../wordnet_summarizer/')
import luhn
import pagerank
import keyphrase_summarizer
import wordnet_summarizer
import nltk
import nltk.data
import operator

TARGET_ARTICLE_PATH = '../test_articles/news1.article'
TARGET_SUMMARY_PATH = '../test_articles/news1.summary'

def read_article(path):
    fp = open(path)
    lines = fp.readlines()

    body = ""

    for line in lines:
        body += line.rstrip('\n') + " "

    return  body

def normalizeScores(scores):
	max = scores[0]
	min = scores[0]
	
	for score in scores:
		if score > max:
			max = score
		if score < min:
			min = score
	normalized = [0.0 for x in scores]
	for (i, score) in enumerate(scores):
		normalized[i] = (score - min) / (max - min)
	return normalized;

def main():
	document = read_article(TARGET_ARTICLE_PATH)
	sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
	body_sent = sent_tokenizer.tokenize(document)
	manual_summary = read_article(TARGET_SUMMARY_PATH)
	summ_sent = sent_tokenizer.tokenize(manual_summary)
	
	scores_manual = [0 for i in xrange(len(body_sent))]
	for (i, sent) in enumerate(body_sent):
		has = False
		for _sent in summ_sent:
			if sent.strip() == _sent.strip():
				has = True
		if(has):
			scores_manual[i] = 4

	scores_luhn = luhn.luhn_summarizer(document)
	normalized_scores_luhn = normalizeScores(scores_luhn);
	scores_pagerank = pagerank.textrank(document)
	normalized_scores_pagerank = normalizeScores(scores_pagerank)
	scores_keyphrase = keyphrase_summarizer.summarize(document)
	normalized_scores_keyphrase = normalizeScores(scores_keyphrase)
	scores_wordnet = wordnet_summarizer.summarize(document)
	normalized_scores_wordnet = normalizeScores(scores_wordnet)
	
	for i in xrange(len(body_sent)):
		print scores_manual[i], normalized_scores_pagerank[i], normalized_scores_luhn[i], normalized_scores_keyphrase[i],  normalized_scores_wordnet[i]
	
main()