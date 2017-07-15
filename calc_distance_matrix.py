'''
Code which indexes sentences and searches and makes distance matrix for each two words
@author: Noushin
'''

import nltk,numpy as np
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import math
from collections import Counter


class Distance_Calc(object):
    # text = "Ali arm hand tongue. Ali He good bad foot hand toe basketball. Ali arm ball goes"



    def __init__(self,input_file):
        self.word_sent = dict()
        self.mylist = list()
        self.text = open(input_file).read()
        self.g_matrix = None#np.zeros((1,1))
        self.Cdist_matrix = None#np.zeros((1, 1))
        self.pmi_matrix = None  # np.zeros((1, 1))

    def sentence_indexing(self, input_file):

        sents = nltk.sent_tokenize(self.text)
        allwords = nltk.word_tokenize(self.text)
        stop_words = set(stopwords.words('english'))
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

    def Gwi_wj(self,key1, key2):
        t = []
        res = 0
        l1 = self.word_sent.get(key1)
        l2 = self.word_sent.get(key2)
        for b in range(len(l1)):
            for e in range(len(l2)):
                t.append(abs(l1[b] - l2[e]) + 1)
                res = min(t)
        return (res)


    def C_dist(self, wi, wj):
        res = (1 - math.log(self.Gwi_wj(wi,wj), 4))
        return res





    def fill_G_matrix(self):
        self.mylist = self.word_sent.keys()
        self.g_matrix = np.zeros((len(self.mylist), len(self.mylist)))
        #output = open("{0}_matrix.txt".format(output_file), "w")
        for i in range(len(self.mylist)):
            for j in range(len(self.mylist)):
                self.g_matrix[i, j] = self.Gwi_wj(self.mylist[i], self.mylist[j])
        #np.savetxt(output, C_matrix, fmt="%i", delimiter=' ', newline='\n')
        return self.g_matrix


    def fill_Cdist_matrix(self):
        #self.mylist = self.word_sent.keys()
        self.Cdist_matrix = np.zeros((len(self.mylist), len(self.mylist)))

        #output = open("{0}_matrix.txt".format(output_file), "w")
        for i in range(len(self.mylist)):
            for j in range(len(self.mylist)):
                self.Cdist_matrix[i, j] = self.C_dist(self.mylist[i], self.mylist[j])
        #np.savetxt(output, C_matrix, fmt="%i", delimiter=' ', newline='\n')
        return self.Cdist_matrix

    def fill_pmi_matrix(self):
        #self.mylist = self.word_sent.keys()
        self.pmi_matrix = np.zeros((len(self.mylist), len(self.mylist)))
    
        for i in range(len(self.mylist)):
            for j in range(len(self.mylist)):
                self.pmi_matrix[i][j] = self.pmi(self.mylist[i], self.mylist[j])
                #print(self.mylist[i], self.mylist[j])
        # np.savetxt(output, C_matrix, fmt="%i", delimiter=' ', newline='\n')
        return self.pmi_matrix



    def P_word(self, in_word):

        cntr = Counter(self.text.lower().split())
        word_cnt = cntr[in_word.lower()]
        denominator = sum(cntr.values())
        res = float(word_cnt) / denominator
        return res

    def Pdist(self,wi, wj):
        tmp =0
        m = len(self.mylist)-1
        denom = sum(sum(self.Cdist_matrix[i][i - m:]) for i in xrange(m))
        #print("here: {}  {}" ,wi ,wj)
        wi_index = self.mylist.index(wi)
        wj_index = self.mylist.index(wj)
        #print (self.mylist)
        print("i ind {} j ind{}".format(wi_index ,wj_index))
        res =float(self.Cdist_matrix[wi_index][wj_index])/denom
        return res

    def pmi(self, wi, wj):
        denom = self.P_word(wi.lower()) * self.P_word(wj.lower())
        print("denom is {} wi  {}   wj {} ".format(denom, wi, wj))
        res = float(self.Pdist(wi, wj))/denom
        return res



    def calculate_distance(self, input_file, key1, key2):


        for i,j in enumerate(self.mylist):
            print(i,"--->",j)
        key1 = key1.lower()
        key2 = key2.lower()
        self.sentence_indexing(input_file)
        self.Gwi_wj(key1, key2)
        self.C_dist(key1, key2)
        #print(res)
        self.fill_G_matrix()
        self.fill_Cdist_matrix()
        #print(self.Cdist_matrix)

        res = self.pmi(key1,key2)
        #print(res)
        self.fill_pmi_matrix()
        #print("{}, {}, {}", len(self.mylist), np.shape(self.Cdist_matrix), np.shape(self.g_matrix))
        return (res)

ola = Distance_Calc("test_file.txt")
out = ola.calculate_distance("test_file.txt", 'good', 'basketball')
#print('result is: {}'.format(out))
#y = np.loadtxt("out_matrix.txt", dtype=int)
#print(y)

'''
    Sample calling!
    out = calculate_distance("dev-muc3-0001-0100","out",'SOURCE','KILLED'
    print('result is: ',out)
    y = np.loadtxt("test.txt",  dtype= int)
    print(y)
    
    
    ola = Distance_Calc()
    out = ola.calculate_distance("dev-muc3-0001-0100","out",'SOURCE','KILLED'
    print('result is: ',out)
    y = np.loadtxt("test.txt",  dtype= int)
    print(y)
    '''

