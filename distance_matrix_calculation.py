
import nltk, numpy as np
from nltk.corpus import stopwords
import math
from collections import Counter


class Distance_Calc(object):

    def __init__(self, word_sent, cntr):
        self.mylist = list()
        self.g_matrix = None
        self.Cdist_matrix = None
        self.pmi_matrix = None
        self.word_sent = word_sent
        self.cntr = cntr

    def Gwi_wj(self, key1, key2):
        t = []
        res = 0
        l1 = self.word_sent.get(key1)
        l2 = self.word_sent.get(key2)
        for b in range(len(l1)):
            for e in range(len(l2)):
                t.append(abs(l1[b] - l2[e]) + 1)
        res = min(t)
        return res

    def C_dist(self, wi, wj):
        res = (1 - math.log(self.Gwi_wj(wi, wj), 4))
        return (max(res, 0.05))  ## same as line 1364 in CountTokenPair.java of Java implementation

    def fill_G_matrix(self):
        self.mylist = self.word_sent.keys()
        self.g_matrix = np.zeros((len(self.mylist), len(self.mylist)))

        for i in range(len(self.mylist)):
            for j in range(len(self.mylist)):
                self.g_matrix[i, j] = self.Gwi_wj(self.mylist[i], self.mylist[j])

        return self.g_matrix

    def fill_Cdist_matrix(self):

        self.Cdist_matrix = np.zeros((len(self.mylist), len(self.mylist)))


        for i in range(len(self.mylist)):
            for j in range(len(self.mylist)):
                self.Cdist_matrix[i, j] = self.C_dist(self.mylist[i], self.mylist[j])

        return self.Cdist_matrix

    def fill_pmi_matrix(self):

        self.pmi_matrix = np.zeros((len(self.mylist), len(self.mylist)))

        for i in range(len(self.mylist)):
            for j in range(len(self.mylist)):
                self.pmi_matrix[i][j] = self.pmi(self.mylist[i], self.mylist[j])


        return self.pmi_matrix

    def P_word(self, in_word):
        word_cnt = len(self.word_sent[in_word])
        denominator = self.cntr
        res = float(word_cnt) / denominator
        return res


    def Pdist(self, wi, wj):

        m = len(self.mylist) - 1
        denom = sum(sum(self.Cdist_matrix[i][i - m:]) for i in xrange(m))

        wi_index = self.mylist.index(wi)
        wj_index = self.mylist.index(wj)

        res = float(self.Cdist_matrix[wi_index][wj_index]) / denom
        return res

    def pmi(self, wi, wj):
        denom = self.P_word(wi) * self.P_word(wj)
        res = float(self.Pdist(wi, wj)) / denom
        return res

    def calculate_distance(self):

        self.fill_G_matrix()
        print("g_matrix\n {}".format(self.g_matrix))
        self.fill_Cdist_matrix()


        self.fill_pmi_matrix()

        print(self.pmi_matrix)
        return (self.pmi_matrix)



