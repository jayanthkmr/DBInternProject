from __future__ import unicode_literals
import nltk,pickle
from nltk.util import ngrams
from nltk.tokenize import PunktWordTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from nlpsenti import Splitter,POSTagger,Dictionary,sentiment_score
from finddomain import *

class Sentiment(object):

    def __init__(self):
        self.wnl = WordNetLemmatizer()
        self.splitter = Splitter()
        self.postagger = POSTagger()
        self.dicttagger = Dictionary([ 'nlpwordpkl/pos.pkl', 'nlpwordpkl/neg.pkl','nlpwordpkl/inc.pkl','nlpwordpkl/dec.pkl','nlpwordpkl/polshift.pickle'])
        self.classifier = pickle.load(open("Classifiers/naive2.pickle"))

    def findsentiment(self, text):
        splitted_sentences = self.splitter.split(text)
        splitted_words = [item for sublist in splitted_sentences for item in sublist]
        postagedsent = nltk.pos_tag(splitted_words)
        words = [u[0] for u in postagedsent if u[1]!="NNP"]
        lemwords = [self.wnl.lemmatize(word) if word!="have" and word!="has" else "have" for word in words]

        pos_tagged_sentences = self.postagger.pos_tag(splitted_sentences)
        dict_tagged_sentences = self.dicttagger.tag(pos_tagged_sentences)
        score1 = sentiment_score(dict_tagged_sentences)
        if (score1[0]+score1[1])>0:
            posscore = score1[0]/(score1[0]+score1[1])
            negscore = score1[1]/(score1[0]+score1[1])
        else:
            posscore = 0
            negscore = 0
        if posscore > (negscore + .05):
            out = "Positive"
        elif negscore > (posscore + .05):
            out = "Negative"
        else:
            out = "Neutral"
        
        feats = dict([(word, True) for word in lemwords + ngrams(lemwords, 2)])
        pro = self.classifier.prob_classify(feats)
        p = self.classifier.classify(feats)

        if p == out:
            resultclass = p
            if p == "Positive":
                resultvalue = max(pro.prob('Positive'),posscore)
            elif p == "Negative":
                resultvalue = max(pro.prob('Negative'),negscore)
            else:
                resultvalue = pro.prob('Neutral')
        elif p=="Neutral":
            resultclass = out
            if out == "Positive":
                resultvalue = max(pro.prob('Positive'),posscore)
            else:
                resultvalue = max(pro.prob('Negative'),negscore)
        elif out == "Neutral":
            resultclass = p
            if p == "Positive":
                resultvalue = max(pro.prob('Negative'),negscore)
            else:
                resultvalue = max(pro.prob('Negative'),negscore)
        else:
            resultclass = "Neutral"
            resultvalue = 1
        if resultclass == "Positive":
            r = 1
        elif resultclass == "Negative":
            r = -1
        else:
            r = 0
        listsenti = [r,resultvalue]
        return listsenti
        
