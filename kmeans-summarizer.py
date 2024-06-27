# -*- coding: cp1252 -*-
from __future__ import division
import nltk
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from numpy import vstack,array
from scipy.cluster.vq import kmeans,vq

f = open('news.txt', 'r')
text = f.read()
sent = nltk.sent_tokenize(text)
t = [nltk.word_tokenize(a) for a in sent]
####
#lem = [[a for a in tr if a not in stopwords.words()] for tr in t ]
####
wnl = nltk.WordNetLemmatizer()
def listcomp(l):
	out = []
	for i in range(0,len(l)):
		p = [wnl.lemmatize(a) for a in l[i]]
		out.append(p)
	return out
lem = listcomp(t)
#t = nltk.word_tokenize(text)
###

tok = nltk.wordpunct_tokenize(text)
ptok = nltk.pos_tag(tok)
imp = [a for a in ptok if a[1][:2]=="NN" or a[1][:2]=="JJ" or a[1][:2]=="RB" or a[1][:2]=="VB" ]
base_words = [word[0].lower() for word in imp]
words = [wnl.lemmatize(word) for word in base_words if word not in stopwords.words()]
word_frequencies = FreqDist(words)
most_frequent_words = [pair[0] for pair in word_frequencies.items()[:int(.8*len(word_frequencies))]]
sfmw = sorted(most_frequent_words)

def vectorize(txt,vec):
	tok = nltk.wordpunct_tokenize(txt)
	wnl = nltk.WordNetLemmatizer()
	w = [wnl.lemmatize(t) for t in tok]
	lt = [t.lower() for t in w]
	twf = nltk.FreqDist(lt)
	a = []
	for i in vec:
		if twf.has_key(i):
			a.append(twf.get(i))
		else:
			a.append(0)
	return a

sentvec = [vectorize(t,sfmw) for t in sent]
data = vstack(sentvec)
centroids,_ = kmeans(data,2)
idx,stdev = vq(data,centroids)
nltk.cluster.util.cosine_distance(sentvec[0],centroids[0])

mina = [(999,999) for i in set(idx)]
for i in range(0,len(sentvec)):
	if mina[idx[i]][1] >= stdev[i]:
		mina[idx[i]] = (i,stdev[i])
sumsent = [sent[mina[i][0]] for i in range(0,len(mina))]

#toklem = [wnl.lemmatize(a) if a!="have" and a!="has" else "have" for a in t]
#ptoklem = nltk.pos_tag(toklem)
#ptoklem = [nltk.pos_tag(toklem) for toklem in lem]
#remptoklem = [[a for a in t if a[1][:2]=="NN" or a[1][:2]=="JJ" or a[1][:2]=="RB" or a[1][:2]=="VB" or a[1][:1] == "W" or a[1][:2]=="CC" or a[1][:2]=="PR" or a[1]=="," or a[1]=="."] for t in ptoklem]
#base_words = [word.lower() for word in nltk.word_tokenize(text)]

#remptoklem = [ a for a in ptoklem if a[1][:2]=="NN" or a[1][:2]=="JJ" or a[1][:2]=="RB" or a[1][:1] == "W"]
