import nltk
import nltk.data
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
import operator
import math

TARGET_ARTICLE_PATH = '../test_articles/test_1.txt'
NUM_NP = 10
#K = 10
stopword_list = stopwords.words('english')

DEBUG = True

def read_article(path):
    fp = open(path)
    lines = fp.readlines()

    headline = None
    body = ""

    for line in lines:
        body += line.rstrip('\n') + " "

    return headline, body

def preprocess(body):
    sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')    

    body = sent_tokenizer.tokenize(body)
    body = [word_tokenize(sent) for sent in body]
    body = [nltk.pos_tag(sent) for sent in body]

    return body

def acceptable_phrase(phrase):
    l = [word for word in phrase.split() if word not in stopword_list and len(word) > 3]
    return len(l) > 0

def cleaned_phrase(phrase):
    cleaned = ""
    for word in phrase.split():
        if acceptable_phrase(word):
            cleaned = word + " "
    cleaned = cleaned.strip()
    return cleaned
    
def leaves_NP(tree):
    for subtree in tree.subtrees(filter = lambda t: t.label()=='NP'):
        yield subtree.leaves()

def get_NP_trees(body_pos):
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
    return trees

def get_keyphrases(NP_trees):
    trees = NP_trees    
    NP = {}
    for tree in trees:
        for leaf_NP in leaves_NP(tree):
            phrase = ""
            for word in leaf_NP:
                phrase += str(word[0]).lower() + " "
            phrase = phrase.strip()
            phrase = cleaned_phrase(phrase)
            
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

    return keyphrases

def compute_similarity(phrase1, phrase2):
    match = None
    if(phrase1 == phrase2):
        match = 1
    elif len(phrase1.split()) == 1 and len(phrase2.split()) == 1:
        synset_p1 = wn.synsets(phrase1)
        synset_p2 = wn.synsets(phrase2)
        if len(synset_p1) == 0 or len(synset_p2) == 0:
            match = 0
        else:
            match = wn.path_similarity(synset_p1[0], synset_p2[0])
    else:
        match = 0    

    if match is None:
        match = 0
    # if DEBUG:
    #     print 'match between ', phrase1, ' & ', phrase2, ': ', match
    return match
                
def get_sentence_score(keyphrases, sent_phrases, sent_words):
    score = 0
    #print 'sent_phrases: ', sent_phrases
    #print 'sent_words: ', sent_words
    for phrase in sent_phrases.items():
        #print phrase
        score_phrase = max(kp[1] * compute_similarity(phrase[0], kp[0]) * math.sqrt(phrase[1]) for kp in keyphrases)
        if score_phrase != 0:
            score += score_phrase
            #print 'score_phrase = ', score_phrase
        else:
            score_words = 0
            for word in phrase[0].split():
                if acceptable_phrase(word) and word in sent_words:
                    score_words += max(kp[1] * compute_similarity(word, kp[0]) * math.sqrt(sent_words[word]) for kp in keyphrases)
            score += score_words
            #print 'score_words = ', score_words    
    #if DEBUG:
    #    print sent_phrases, ' | ', sent_words, ' | ', score            

    #print 'score: ', score
    #print '\n'
    return score
    
def get_sentence_scores(keyphrases, trees):
    scores_dict = {}
    sent_scores = [0.0 for x in trees]
    for i, tree in enumerate(trees):
        score = 0
        freq_phrases = {}
        freq_words = {}
        for leaf_NP in leaves_NP(tree):
            phrase = ""
            for word in leaf_NP:
                phrase += str(word[0]).lower() + " "
            phrase = phrase.strip()
            phrase = cleaned_phrase(phrase)
            
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

        score = get_sentence_score(keyphrases, freq_phrases, freq_words)
        scores_dict[i] = score
        sent_scores[i] = score

    return scores_dict, sent_scores
        
def summarize(body):

    body_pos = preprocess(body)
    trees = get_NP_trees(body_pos)
    keyphrases = get_keyphrases(trees)

    if DEBUG:
        print keyphrases, '\n'
        
    if len(body_pos)/3>10:
        K = 10
    else:
        K = len(body_pos)/3
    K = K+1
    scores_dict, sent_scores = get_sentence_scores(keyphrases, trees)
    scores = sorted(scores_dict.items(), key=operator.itemgetter(1), reverse = True)[0 : K + 1]

    # contains_first = True if len([score for score in scores if score[0] == 0]) > 0 else False
    # if DEBUG:
    #     print 'contains first: ', contains_first
    #     #print scores_dict
    # if not contains_first:
    #     if DEBUG:
    #         print 'setting score for sent 0 = score for sent ', scores[K][0], ' = ', scores[K][1], ' (orig score for sent 0 = ', scores_dict[0] , ')'
    #     sent_scores[0] = scores[K][1]
    #     scores_dict[0] = scores[K][1]    
    #     scores[K] = (0, scores[K][1])
        
    scores = sorted(scores, key = operator.itemgetter(0))    
    if DEBUG:
        print scores, '\n'
    
    sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    body_sent = sent_tokenizer.tokenize(body)
    
    summary = []
    if scores[0][0] != 0:
        summary.append((body_sent[0], 0, scores_dict[0]))
    for score in scores:
        summary.append((body_sent[score[0]], score[0], score[1]))
                       
    #return summary
    if DEBUG:
        print "Wordnet"
        for line in summary:
            print line
        
    return sent_scores
    
def main():
    
    headline, body = read_article(TARGET_ARTICLE_PATH)

    summary = summarize(body)
    
    # print '\n'                   
    # for line in summary:
    #     print line, '\n'

if DEBUG:
    main()
