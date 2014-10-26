import nltk
import nltk.data
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import operator
import math

TARGET_ARTICLE_PATH = '../test_articles/test_1.txt'
NUM_NP = 10
K = 10
stopword_list = stopwords.words('english')

def read_article(path):
    fp = open(path)
    lines = fp.readlines()

    headline = lines[0]
    body = ""

    for line in lines[1:]:
        body += line.rstrip('\n')

    return headline, body

def preprocess(headline, body):
    sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')    

    headline = word_tokenize(headline)
    headline = nltk.pos_tag(headline)

    body = sent_tokenizer.tokenize(body)
    body = [word_tokenize(sent) for sent in body]
    body = [nltk.pos_tag(sent) for sent in body]

    return headline, body

def leaves_NP(tree):
    for subtree in tree.subtrees(filter = lambda t: t.label()=='NP'):
        yield subtree.leaves()

def acceptable_phrase(phrase):
    l = [word for word in phrase.split() if word not in stopword_list and len(word) > 3]
    return len(l) > 0
    
def get_score(keyphrases, freq_phrases, freq_words):
    score = 0
    for phrase in freq_phrases.items():
        for keyphrase in keyphrases:
            if phrase[0] == keyphrase[0]:
                score += keyphrase[1] * math.sqrt(phrase[1])
                break
                
    for word in freq_words.items():
        for keyphrase in keyphrases:
            if word[0] == keyphrase[0]:
                score += keyphrase[1] * math.sqrt(word[1])
                break
    return score
                
def summarize(headline, body):

    headline_pos, body_pos = preprocess(headline, body)
        
    # grammar = "NP: {<DT>?<JJ>*<NN>}"
    grammar = r"""
    NBAR:
    {<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns
    
    NP:
    {<DT>?<JJ>*<NN>}
    {<NBAR>}
    {<NBAR><IN><NBAR>}  # Above, connected with in/of/etc...
    """
    chunker = nltk.RegexpParser(grammar)
    trees = [chunker.parse(sent) for sent in body_pos]
    trees.append(chunker.parse(headline_pos))
    
    NP = {}
    for tree in trees:
        for leaf_NP in leaves_NP(tree):
            phrase = str(leaf_NP[0][0]).lower()
            if phrase in NP:
                NP[phrase] += 1
            elif acceptable_phrase(phrase):
                NP[phrase] = 1

            if len(phrase.split()) > 1:
                for word in phrase.split():
                    if word in NP:
                        NP[word] += 1.0 / len(phrase.split())
                    elif acceptable_phrase(word):
                        NP[word] = 1.0 / len(phrase.split())

    keyphrases = sorted(NP.items(), key=operator.itemgetter(1), reverse = True)[0 : NUM_NP+1]
    keyphrases = [(phrase[0], float(phrase[1]) / len(NP)) for phrase in keyphrases]
    print keyphrases, '\n'
    
    scores_dict = {}
    for i, tree in enumerate(trees):
        score = 0
        freq_phrases = {}
        freq_words = {}
        for leaf_NP in leaves_NP(tree):
            phrase = str(leaf_NP[0][0]).lower()
            if phrase in freq_phrases:
                freq_phrases[phrase] += 1
            elif acceptable_phrase(phrase):
                freq_phrases[phrase] = 1
                
            if len(phrase.split()) > 1:
                for word in phrase.split():
                    if word in freq_words:
                        freq_words[word] += 1
                    elif acceptable_phrase(word):
                        freq_words[word] = 1

        score = get_score(keyphrases, freq_phrases, freq_words)
        scores_dict[i] = score

    scores = sorted(scores_dict.items(), key=operator.itemgetter(1), reverse = True)[0 : K + 1]
    scores = sorted(scores, key = operator.itemgetter(0))    
    print '\n', scores, '\n'
    sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    body_sent = sent_tokenizer.tokenize(body)
    summary = []
    if scores[0][0] != 0:
        summary.append((body_sent[0], 0, scores_dict[0]))
    for score in scores:
        summary.append((body_sent[score[0]], score[0], score[1]))
                       
    return summary
    
def main():
    
    headline, body = read_article(TARGET_ARTICLE_PATH)

    summary = summarize(headline, body)
    print '\n'                   
    for line in summary:
        print line, '\n'

main()
