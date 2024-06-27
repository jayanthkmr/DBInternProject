from __future__ import unicode_literals
import os
import nltk
import pickle

from nltk.corpus import wordnet as wn
from sentiwordnet import SentiWordNetCorpusReader, SentiSynset

#f = open('test.txt', 'r')
#text = f.read()
#text = ""
class Splitter(object):
    def __init__(self):
        self.nltk_splitter = nltk.data.load('tokenizers/punkt/english.pickle')
        self.nltk_tokenizer = nltk.tokenize.TreebankWordTokenizer()
 
    def split(self, text):
        """
        input format: a paragraph of text
        output format: a list of lists of words.
            e.g.: [['this', 'is', 'a', 'sentence'], ['this', 'is', 'another', 'one']]
        """
        sentences = self.nltk_splitter.tokenize(text)
        tokenized_sentences = [self.nltk_tokenizer.tokenize(sent) for sent in sentences]
        return tokenized_sentences
class POSTagger(object):
    def __init__(self):
        pass
        
    def pos_tag(self, sentences):
        """
        input format: list of lists of words
            e.g.: [['this', 'is', 'a', 'sentence'], ['this', 'is', 'another', 'one']]
        output format: list of lists of tagged tokens. Each tagged tokens has a
        form, a lemma, and a list of tags
            e.g: [[('this', 'this', ['DT']), ('is', 'be', ['VB']), ('a', 'a', ['DT']), ('sentence', 'sentence', ['NN'])],
                    [('this', 'this', ['DT']), ('is', 'be', ['VB']), ('another', 'another', ['DT']), ('one', 'one', ['CARD'])]]
        """
        wnl = nltk.WordNetLemmatizer()
        pos = [nltk.pos_tag(sentence) for sentence in sentences]
        #adapt format
        pos = [[(word, wnl.lemmatize(word) if word!="have" and word!="has" else "have" , [postag]) for (word, postag) in sentence] for sentence in pos]
        return pos

#splitter = Splitter()
#postagger = POSTagger()
 
#splitted_sentences = splitter.split(text)
#pos_tagged_sentences = postagger.pos_tag(splitted_sentences)

class Dictionary(object):
    def __init__(self, dictionary_paths):
        files = [open(path, 'r') for path in dictionary_paths]
        self.wordlist = [pickle.load(opath) for opath in files]
        map(lambda x: x.close(), files)
        self.swn_filename = 'SentiWordNet_3.0.0_20130122.txt'
        self.swn = SentiWordNetCorpusReader(self.swn_filename)
    def tag(self, postagged_sentences):
        return [self.tag_sentence(sentence) for sentence in postagged_sentences]
    def tag_sentence(self,sentence,tag_with_lemmas=False):
        """
        the result is only one tagging of all the possible ones.
        The resulting tagging is determined by these two priority rules:
            - longest matches have higher priority
            - search is made from left to right
        """
        tag_sentence = []
        N = len(sentence)
        i = 0
        while (i < N):
            j = N #avoid overflow
            tagged = False
            while (j > i):
                expression_form = ' '.join([word[0] for word in sentence[i:j]]).lower()
                expression_lemma = ' '.join([word[1] for word in sentence[i:j]]).lower()
                #pos_tag = ' '.join([word[2] for word in sentence[i:j]]).lower()
                if tag_with_lemmas:
                    literal = expression_lemma
                else:
                    literal = expression_form
                if literal in  set([p for q in self.wordlist for p in q ]):
                    #self.logger.debug("found: %s" % literal)
                    is_single_token = j - i == 1
                    original_position = i
                    i = j
                    taggings = []
                    scores = {'posscore' : 0, 'negscore' : 0, 'objscore' : 1}
                    if literal in self.wordlist[0]:
                        taggings.append("positive")
                        scores['posscore'] = .9
                        scores['negscore'] = 0
                        scores['objscore'] = .1
                    elif literal in self.wordlist[1]:
                        taggings.append("negative")
                        scores['posscore'] = 0
                        scores['negscore'] = .9
                        scores['objscore'] = .1
                    elif literal in self.wordlist[2]:
                        taggings.append("incrementer")
                    elif literal in self.wordlist[3]:
                        taggings.append("decrementer")
                    elif literal in self.wordlist[4]:
                        taggings.append("negation")
                    #taggings = ["positive" if literal in self.wordlist[0] else "negative" if literal in self.wordlist[1] else "incrementer" if literal in self.wordlist[2] else "decrementer" if literal in self.wordlist[3] else "negation" if literal in self.wordlist[4]]
                    tagged_expression = (expression_form, expression_lemma, taggings,scores)
                    if is_single_token: #if the tagged literal is a single token, conserve its previous taggings:
                        original_token_tagging = sentence[original_position][2]
                        tagged_expression[2].extend(original_token_tagging)
                        tagged_expression = (tagged_expression[0], tagged_expression[1], tagged_expression[2],scores)
                    tag_sentence.append(tagged_expression)
                    tagged = True
                else:
                    j = j - 1
            if not tagged:
                expression_lemma = sentence[i][1]
                expression_postag = sentence[i][2]
                ws = wn.synsets(expression_lemma)
                ss = self.swn.senti_synsets(expression_lemma)
                if len(ws) == 1 and len(ss)==1:
                    s = ss[0]
                    p = s.pos_score
                    n = s.neg_score
                    o = s.obj_score
                elif (expression_postag[0]!="N" and expression_postag[0]!="J" and expression_postag[0]!="R" and expression_postag[0]!="V") or len(ss) == 0:
                    p = 0
                    n = 0
                    o = 1
                elif expression_postag[0]=="J" and len(ss)>0:
                    sa = self.swn.senti_synsets(w,'a')
                    if len(sa)>0:
                        s = sa[0]
                        p = s.pos_score
                        n = s.neg_score
                        o = s.obj_score
                    else:
                        p = 0
                        n = 0
                        o = 1
                else:
                    sa = self.swn.senti_synsets(expression_lemma,expression_postag[0].lower())
                    if len(sa)>0:
                        s = sa[0]
                        p = s.pos_score
                        n = s.neg_score
                        o = s.obj_score
                    else:
                        p = 0
                        n = 0
                        o = 1
                if expression_postag == "NNP" or expression_postag == "NNPS":
                    p = 0
                    n = 0
                    o = 0
                scores = {'posscore' : 0, 'negscore' : 0, 'objscore' : 1}
                scores['posscore'] = p
                scores['negscore'] = n
                scores['objscore'] = o
                tagged_expression = sentence[i]
                sentence[i] = (tagged_expression[0], tagged_expression[1], tagged_expression[2],scores)
                tag_sentence.append(sentence[i])
                i += 1
        return tag_sentence
    
#dicttagger = Dictionary([ 'pos.pkl', 'neg.pkl','inc.pkl','dec.pkl','polshift.pkl'])
#dict_tagged_sentences = dicttagger.tag(pos_tagged_sentences)

def sentence_score(sentence_tokens, previous_tags, acumpos_score,acumneg_score,acumobj_score):
    #print sentence_tokens,previous_tags
    if not sentence_tokens:
        return [acumpos_score,acumneg_score,acumobj_score]
    else:
        current_token = sentence_tokens[0]
        token_posscore = current_token[3]['posscore']
        token_negscore = current_token[3]['negscore']
        token_objscore = current_token[3]['objscore']
        if previous_tags:
            if 'incrementer' in previous_tags:
                if token_posscore>token_negscore:
                    token_posscore = 2.0*token_posscore
                elif token_posscore<token_negscore:
                    token_negscore = 2.0*token_negscore
                else:
                    token_posscore = 2.0*token_posscore
                    token_negscore = 2.0*token_negscore
            if 'decrementer' in previous_tags:
                if token_posscore>token_negscore:
                    token_posscore = token_posscore/2.0
                elif token_posscore<token_negscore:
                    token_negscore = token_negscore/2.0
                else:
                    token_posscore = token_posscore/2.0
                    token_negscore = token_negscore/2.0
            if 'negation' in previous_tags:
                p = token_posscore
                token_posscore = token_negscore
                token_negscore = p
            total = token_posscore + token_negscore + token_objscore
            token_posscore = token_posscore/total
            token_negscore = token_negscore/total
            token_objscore = token_objscore/total
        previous_tags.extend(current_token[2])
        return sentence_score(sentence_tokens[1:], previous_tags, acumpos_score + token_posscore,acumneg_score + token_negscore,acumobj_score + token_objscore)
    
def listadd(a,b):
	return [a[i]+b[i] for i in range(len(a))]
    
def sentiment_score(review):
    return reduce(listadd,[sentence_score(sentence,[], 0.0,0.0,0.0) for sentence in review])

    
