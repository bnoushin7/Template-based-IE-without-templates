'''
Code which indexes sentences and searches and makes distance matrix for each two words
@author: Noushin
'''

import nltk,numpy as np
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import math


class Distance_Calc(object):
    # text = "Ali arm hand tongue. Ali He good bad foot hand toe basketball. Ali arm ball goes"



    def __init__(self):
        self.word_sent = dict()
        self.mylist = list()

    def sentence_indexing(self, input_file):
        text = open(input_file).read()
        sents = nltk.sent_tokenize(text)
        allwords = nltk.word_tokenize(text)
        stop_words = set(stopwords.words('english'))
        filtered_words = [w for w in allwords if not w in stop_words]
        index = 0
        for s in sents:
            index += 1
            for w in nltk.word_tokenize(s):
                if w in self.word_sent:
                    self.word_sent[w].append(index)
                else:
                    self.word_sent[w] = [index]
                    # print(word_sent)

    def Gwi_wj(self,key1, key2):
        t = []
        res = 0
        l1 = self.word_sent.get(key1)
        l2 = self.word_sent.get(key2)
        for b in range(len(l1)):
            for e in range(len(l2)):
                t.append(abs(l1[b] - l2[e]) + 1)
                res = min(t)
        # print('res of {} and {} is {} {}'.format(key1, key2,t,res))
        return (res)

    D = [1, 2]

    def C_dist(self, _matrix,  _row, _col):
        rows = _matrix.shape[0]
        cols = _matrix.shape[1]
        for d in range(D):
            for i in rows:
                for j in cols:
                    res = (1 - math.log(_matrix[_row][_col], 4))
                print(res)
        return res

    '''
    tmp = 0
    for i in k:
        for i2 in l:
            k +=C_dist(Wi,Wj)/tmp
    '''

    def fill_matrix(self, output_file):
        self.mylist = self.word_sent.keys()
        g_matrix = np.zeros((len(self.mylist), len(self.mylist)))
        C_matrix = np.zeros((len(self.mylist), len(self.mylist)))
        output = open("{0}_matrix.txt".format(output_file), "w")
        for i in range(len(self.mylist)):
            for j in range(len(self.mylist)):
                g_matrix[i, j] = self.Gwi_wj(self.mylist[i], self.mylist[j])

        for i in range(len(self.mylist)):
            for j in range(len(self.mylist)):
                C_matrix[i, j] = self.C_dist(g_matrix, i, j)

        np.savetxt(output, C_matrix, fmt="%i", delimiter=' ', newline='\n')
        return C_matrix



        # np.savetxt(output, g_matrix, fmt = "%i", delimiter=' ', newline='\n')
       # np.savetxt(output, g_matrix, fmt="%i", delimiter=' ', newline='\n')
        # output.write(g_matrix)

        # output.close()

    def calculate_distance(self, input_file, output_file, key1, key2):
        self.sentence_indexing(input_file)
        res = self.Gwi_wj(key1, key2)
        print(res)
        self.fill_matrix(output_file)
        return (res)


ola = Distance_Calc()
out = ola.calculate_distance("dev-muc3-0001-0100", "out", 'SOURCE', 'KILLED')
print('result is: {}'.format(out))
y = np.loadtxt("out_matrix.txt", dtype=int)
print(y)

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