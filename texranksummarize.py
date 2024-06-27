from __future__ import unicode_literals
import networkx as nx
import numpy as np
import math
import nltk
 
#from nltk.tokenize.punkt import PunktSentenceTokenizer
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer

class TextRankSummarizer:

##    def __init__(self):
##        self.sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
##        #self.sentence_tokenizer = PunktSentenceTokenizer()

    def reorder_sentences( self, output_sentences, doc ):
        output_sentences.sort( lambda s1, s2:doc.find(s1) - doc.find(s2) )
        return output_sentences
	    
    def textranksummarize(self,document,percent):
        sentences = sent_tokenize(document)
        n = len(sentences)
        f = math.ceil(percent*n)
        bow_matrix = CountVectorizer().fit_transform(sentences)
        normalized = TfidfTransformer().fit_transform(bow_matrix)
     
        similarity_graph = normalized * normalized.T
     
        nx_graph = nx.from_scipy_sparse_matrix(similarity_graph)
        scores = nx.pagerank(nx_graph)
        u = sorted(((scores[i],s) for i,s in enumerate(sentences)),
                      reverse=True)
        output_sentences = [s[1] for s in u][:int(f)]
        # sort the output sentences back to their original order
        output_sentences = self.reorder_sentences(output_sentences, document)
        # concatinate the sentences into a single string
        return "  ".join(output_sentences)
