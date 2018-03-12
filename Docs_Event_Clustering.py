import time
import sys
from os.path import dirname

textFilePath = "conll_full_parser.py"
textFileFolder = dirname(textFilePath)  # = "/home/me/somewhere/textfiles"

sys.path.append(textFileFolder)

import nounOfVerbFinder

import scipy.cluster.hierarchy as sch
# import distance_matrix_calculation
# from distance_matrix_calculation import *
# import conll_full_parser



import numpy as np
from collections import Counter
# import scipy.cluster.hierarchy as sch
# import distance_matrix_calculation
# from distance_matrix_calculation import *
import conll_full_parser
import sys

import nltk
from nltk.corpus import stopwords
import math

# from collections import Counter





conll = dict()
idx = 0

for file in __import__('os').listdir("Conll/"):
    conll[idx] = (word_sent_dict, cntr) = conll_full_parser.parse_full_conll("Conll/" + file, file)
    idx += 1

# kidnap_lst=list()
# for doc_idx in range(len(conll)):
#    if ( ('ransom' in conll[doc_idx][0].keys() ) & ('kidnap' in conll[doc_idx][0].keys()) ):
#        kidnap_lst.append(doc_idx)







# len(all_keys)
all_keys = list()
P_Words = list()
C_Dist = dict()

def Gwi_wj(lst1, lst2):
    t = []
    res = 0
    for b in range(len(lst1)):
        for e in range(len(lst2)):
            t.append(abs(lst1[b] - lst2[e]) + 1)
    res = min(t)
    # res=min(res1 , 2)
    # res=min(res1 , 2)
    return res


# word_sent=list()
# for doc_idx in range(250) :
#    word_sent.append( conll[doc_idx])

word_sent = conll
print("#####################avali###################################################")
#print(word_sent)
# conll.clear()
len1 = len(word_sent)

for doc_idx in range(len(word_sent)):
    keys = word_sent[doc_idx][0].keys()
    for key in keys:
        word_sent[doc_idx][0][key] = np.unique(word_sent[doc_idx][0][key])
len2 = len(word_sent)
print("######################dovomi##################################################")
#print(word_sent)

for doc_idx in range(len(word_sent)):
    doc_keys = word_sent[doc_idx][0].keys()
    # doc_keys= np.sort( list(doc_keys) )
    all_keys.extend(doc_keys)

all_keys = list(np.unique(all_keys))

len(all_keys)

Count = [0] * len(all_keys)
for word_idx in range(len(all_keys)):
    for doc_idx in range(len(word_sent)):
        if (all_keys[word_idx] in word_sent[doc_idx][0].keys()):
            Count[word_idx] = Count[word_idx] + len(word_sent[doc_idx][0][all_keys[word_idx]])

len(Count)

great_1_idx = np.where(np.array(Count) > 1)[0]
#print(np.where(np.array(Count) > 1))
less_500_idx = np.where(np.array(Count) < 500)[0]

frequent_words_idx = np.array(list(set(great_1_idx) & set(less_500_idx)))

len(frequent_words_idx)
#print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=")
#print(len(Count))
#print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=")
Count = np.array(Count)[frequent_words_idx]
#print(len(Count))
len(Count)
#print(len(all_keys))
all_keys = np.array(all_keys)[frequent_words_idx]  # only worods with occurance count of at lest 2 times are selected.
len(all_keys)
#print(len(all_keys))
np.max(Count)

words_dict = dict()
for word_idx in range(len(all_keys)):
    words_dict[all_keys[word_idx]] = Count[word_idx]

all_keys = np.sort(all_keys)
'''
print("count e ghabli")
print(Count)
print("**************************************************************")
'''

Count = [0] * len(all_keys)
for word_idx in range(len(all_keys)):
    Count[word_idx] = words_dict[all_keys[word_idx]]
'''
print("count e jadid")
print(Count)
print("**************************************************************")
'''

# np.where( all_keys=='ransom' )
# Count[2045]



# ----------------------C_Dist Calculation-----------------------
C_Dist = dict()
for doc_idx in range(len(word_sent)):
    doc_keys = word_sent[doc_idx][0].keys()
    doc_keys = np.sort(list(doc_keys))
    # all_keys.extend(doc_keys)
    for key1_idx in range(len(doc_keys) - 1):
        for key2_idx in range((key1_idx + 1), len(doc_keys)):
            key1 = doc_keys[key1_idx]
            key2 = doc_keys[key2_idx]
            if ((key1 in words_dict.keys()) & (key2 in words_dict.keys())):
                if ((key1, key2) in C_Dist.keys()):
                    C_Dist[(key1, key2)] += (
                    1 - math.log(Gwi_wj(word_sent[doc_idx][0][key1], word_sent[doc_idx][0][key2]), 4))
                else:
                    C_Dist[(key1, key2)] = (
                    1 - math.log(Gwi_wj(word_sent[doc_idx][0][key1], word_sent[doc_idx][0][key2]), 4))

len(C_Dist.keys())

for key in C_Dist.keys():
    C_Dist[key] = max(C_Dist[key], 0.05)

# C_Dist.values()


# all_keys=list(np.unique(all_keys) )

# len(all_keys)





# ---------P_words calcuation ------------
all_words_freq = sum(Count)
P_Words = list(np.array(Count) / all_words_freq)

# ----------------------pmi  calculation-------------------

C_Dist_Sum = sum(C_Dist.values())
P_Dist = C_Dist

# C_Dist.clear()

for key in P_Dist.keys():
    P_Dist[key] = P_Dist[key] / C_Dist_Sum

pmi_matrix = np.zeros((len(all_keys), len(all_keys)))

for word1_idx in range(len(all_keys) - 1):
    for word2_idx in range((word1_idx + 1), len(all_keys)):
        word1 = all_keys[word1_idx]
        word2 = all_keys[word2_idx]
        if ((word1, word2) in P_Dist.keys()):
            print(P_Dist[(word1, word2)])
            print(P_Words[word1_idx])
            print(P_Words[word2_idx])
            if(P_Words[word1_idx] * P_Words[word2_idx] == 0):
                continue
            else:
                pmi_matrix[word1_idx, word2_idx] = P_Dist[(word1, word2)] / (P_Words[word1_idx] * P_Words[word2_idx])
                pmi_matrix[word2_idx, word1_idx] = pmi_matrix[word1_idx, word2_idx]

P_Dist.clear()
C_Dist.clear()

# distance_matrix= np.zeros(  (len(all_keys) , len(all_keys) ) )
max_pmi = np.max(pmi_matrix)

distance_matrix = max_pmi - pmi_matrix

# for word
# _idx in range(len(all_keys)-1 ) :
#    for word2_idx in range( (word1_idx+1),len(all_keys) ) :
#        distance_matrix[word1_idx , word2_idx]= max_pmi - pmi_matrix[word1_idx ,word2_idx]
#        distance_matrix[word2_idx ,word1_idx]= distance_matrix[word1_idx ,word2_idx]


del (pmi_matrix)

# --------------Clustering-----------------
N = distance_matrix.shape[0]  # vector number
dist = distance_matrix[np.triu_indices(N, 1)]

del (distance_matrix)

clust_tree = sch.linkage(dist, method='average')

del (dist)
n_clusters = 220
y = sch.fcluster(clust_tree, n_clusters, 'maxclust')  # 100

cls_cnt = Counter(y)
cls_cnt.most_common(10)

# ------------------------Clusters Members ---------------
# --------------------kidnapp cluster------
kidnap_idx = np.where(all_keys == 'kidnap')
kidnap_cls = y[kidnap_idx]
members_idx = np.where(y == kidnap_cls)
all_keys[members_idx]

# -------------Cluster1--------------------
large_cls_idx = cls_cnt.most_common(10)[0][0]
cls_members_idx = np.where(y == large_cls_idx)

np.array(all_keys)[cls_members_idx]

# -------------Cluster2--------------------
large_cls_idx = cls_cnt.most_common(10)[1][0]
cls_members_idx = np.where(y == large_cls_idx)

np.array(all_keys)[cls_members_idx]

# -------------Cluster3--------------------

large_cls_idx = cls_cnt.most_common(10)[2][0]
cls_members_idx = np.where(y == large_cls_idx)

np.array(all_keys)[cls_members_idx]

# -------------Cluster4--------------------
large_cls_idx = cls_cnt.most_common(10)[3][0]
cls_members_idx = np.where(y == large_cls_idx)

np.array(all_keys)[cls_members_idx]

# -------------Cluster5--------------------

large_cls_idx = cls_cnt.most_common(10)[4][0]
cls_members_idx = np.where(y == large_cls_idx)

np.array(all_keys)[cls_members_idx]

# -------------Cluster6--------------------

large_cls_idx = cls_cnt.most_common(10)[5][0]
cls_members_idx = np.where(y == large_cls_idx)

np.array(all_keys)[cls_members_idx]

# -------------Cluster7--------------------

large_cls_idx = cls_cnt.most_common(10)[6][0]
cls_members_idx = np.where(y == large_cls_idx)

np.array(all_keys)[cls_members_idx]

# -------------Cluster8--------------------

large_cls_idx = cls_cnt.most_common(10)[7][0]
cls_members_idx = np.where(y == large_cls_idx)

np.array(all_keys)[cls_members_idx]

# -------------Cluster9--------------------

large_cls_idx = cls_cnt.most_common(10)[8][0]
cls_members_idx = np.where(y == large_cls_idx)

np.array(all_keys)[cls_members_idx]

# -------------Cluster10--------------------

large_cls_idx = cls_cnt.most_common(10)[9][0]
cls_members_idx = np.where(y == large_cls_idx)

np.array(all_keys)[cls_members_idx]




