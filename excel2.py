from __future__ import unicode_literals
from xlrd import open_workbook
from xlwt import Workbook
from finddomain import *
import nltk,pickle
from nltk.util import ngrams
from nltk.tokenize import PunktWordTokenizer
from nlpsenti import Splitter,POSTagger,Dictionary,sentiment_score

splitter = Splitter()
postagger = POSTagger()
dicttagger = Dictionary([ 'nlpwordpkl/pos.pkl', 'nlpwordpkl/neg.pkl','nlpwordpkl/inc.pkl','nlpwordpkl/dec.pkl','nlpwordpkl/polshift.pickle'])
classifier = pickle.load(open("Classifiers/naive2.pickle"))

rb = open_workbook('newsarchiveeurusd.xls')
rsheet = rb.sheet_by_name("news")
wb = Workbook()
wsheet = wb.add_sheet("news")
for col in range(rsheet.ncols):
    wsheet.write(0,col,rsheet.cell(0,col).value)
for row in range(1,rsheet.nrows):
    values = []
    for col in range(rsheet.ncols):
        wsheet.write(row,col,rsheet.cell(row,col).value)
    text = rsheet.cell(row,7).value
    splitted_sentences = splitter.split(text)
    splitted_words = [item for sublist in splitted_sentences for item in sublist]
    postagedsent = nltk.pos_tag(splitted_words)
    words = [u[0] for u in postagedsent if u[1]!="NNP"]
    lemwords = [wnl.lemmatize(word) if word!="have" and word!="has" else "have" for word in words]
    res = finddomain(splitted_words)
    if res > .11:
        wsheet.write(row,col+1,"Business")
    else:
        wsheet.write(row,col+1,"General")    
    pos_tagged_sentences = postagger.pos_tag(splitted_sentences)
    dict_tagged_sentences = dicttagger.tag(pos_tagged_sentences)
    
    score1 = sentiment_score(dict_tagged_sentences)
    
    wsheet.write(row,col+2,score1[0])
    wsheet.write(row,col+3,score1[1])
    wsheet.write(row,col+4,score1[2])

    feats = dict([(word, True) for word in lemwords + ngrams(lemwords, 2)])
    pro = classifier.prob_classify(feats)
    p = classifier.classify(feats)
    wsheet.write(row,col+5,pro.prob('Positive'))
    wsheet.write(row,col+6,pro.prob('Negative'))
    wsheet.write(row,col+7,pro.prob('Neutral'))
    wsheet.write(row,col+8,p)
    print score1, "\t",p
wb.save('newsarchiveeurusdfinal.xls')
