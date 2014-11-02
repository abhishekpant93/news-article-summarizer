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



TARGET_ARTICLE_PATH = '../test_articles/test_2.txt'

NUMBER_OF_ARTICLES = 4.0
WEIGHT_LUHN = 1 / NUMBER_OF_ARTICLES
WEIGHT_KEYPHRASE = 1 / NUMBER_OF_ARTICLES
WEIGHT_WORDNET = 1 / NUMBER_OF_ARTICLES
WEIGHT_PAGERANK = 1 / NUMBER_OF_ARTICLES

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
	if len(body_sent)/3>10:
		K = 10
	else:
		K = len(body_sent)/3
	# print '\nLuhn\n'
	scores_luhn = luhn.luhn_summarizer(document)
	normalized_scores_luhn = normalizeScores(scores_luhn);
	# print scores_luhn;
	# print normalized_scores_luhn;
	# print '\nPagerank\n'
	scores_pagerank = pagerank.textrank(document)
	normalized_scores_pagerank = normalizeScores(scores_pagerank)
	# print scores_pagerank
	# print normalized_scores_pagerank
	# print '\nKeyPhrase\n'
	scores_keyphrase = keyphrase_summarizer.summarize(document)
	normalized_scores_keyphrase = normalizeScores(scores_keyphrase)
	# print scores_keyphrase
	# print normalized_scores_keyphrase;
	# print '\nWordnet\n'
	scores_wordnet = wordnet_summarizer.summarize(document)
	normalized_scores_wordnet = normalizeScores(scores_wordnet)
	# print scores_wordnet
	# print normalized_scores_wordnet;
	total_score = {}#[0.0 for x in scores_luhn]
	for i in xrange(len(body_sent)):
		total_score[i] = (normalized_scores_luhn[i] * WEIGHT_LUHN) + (normalized_scores_keyphrase[i] * WEIGHT_KEYPHRASE) + (normalized_scores_wordnet[i] * WEIGHT_WORDNET) + (normalized_scores_pagerank[i] * WEIGHT_PAGERANK)
	# print '\nTotal Scores\n'
	# print total_score
	scores = sorted(total_score.items(), key=operator.itemgetter(1), reverse = True)[0 : K + 1]
	# print scores
	scores = sorted(scores, key = operator.itemgetter(0))    

	summary = []
	if scores[0][0] != 0:
		summary.append(body_sent[0])#, 0, total_score[0]))
	for score in scores:
		summary.append(body_sent[score[0]])#, score[0], score[1])
	summary_string = ''
	for element in summary:
		summary_string+=element
	print summary_string
	
main()