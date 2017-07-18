'''
Created on 7/14/17
Sample code for  
@author: Noushin
'''

import verb_detection
import calc_distance_matrix
import nounOfVerbFinder
import nltk,numpy as np
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import math
from collections import Counter


class data_preprocessing():
    
    def __init__(self,input_file):
        self.trigerw_sent = dict()
        self.triggerlist = list()
        self.text = open(input_file).read()
        self.sents = nltk.sent_tokenize(self.text)
        self.stop_words = set(stopwords.words('english'))

    def trig_finder(self):
        event_patterns = []
        filtered_words = [w for w in self.allwords if not w in self.stop_words]
        while "." in filtered_words: filtered_words.remove(".")

        #Reading the corpus




#Sentify


        allwords = nltk.word_tokenize(self.text)

        filtered_words = [w for w in allwords if not w in stop_words]
        while "." in filtered_words: filtered_words.remove(".")
        print(filtered_words)
        index = 0
        for s in sents:
            index += 1
            #for w in nltk.word_tokenize(s):
            for w in filtered_words:
                if w in self.word_sent:
                    self.word_sent[w].append(index)
                else:
                    self.word_sent[w] = [index]




#POS and exract verbs, add it to the dictionary with list of sentence index

    verbs = verb_detection()


#NER and search for NEs


#For each sentence, extract verbs and the NEs




#For each verb, extract its Nouns from wordnet
list_of_related_nouns = noun_finder(verb_word)

#Feed it (call distance)

self.Gwi_wj(key1, key2)
self.C_dist(key1, key2)
# print(res)
self.fill_G_matrix()
self.fill_Cdist_matrix()
# print(self.Cdist_matrix)

res = self.pmi(key1, key2)
# print(res)
self.fill_pmi_matrix()
