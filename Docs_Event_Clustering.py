
import time
import sys
import pickle, os
from os.path import dirname

#import cProfile, pstats, io

"""
def profile(fnc):
    #A decorator that uses cProfile to profile a function

    def inner(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        retval = fnc(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return retval

    return inner
"""




#textFilePath = "D:/summer_task-dev/conll_full_parser.py"
textFilePath = "/home/noushin/summerTask/conll_full_parser.py"
textFileFolder = dirname(textFilePath)  # = "/home/me/somewhere/textfiles"
output_file = open("output_file.txt", "w")

sys.path.append(textFileFolder)


import nounOfVerbFinder

import Syntactic_Clustering

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


import coref_Vector
import selectional_preferences

conll = dict()
idx = 0
start_time =time.time()
if os.path.isfile("/home/noushin/summerTask/pickles/conll_dict.pickle"):
    conll = pickle.load( open( "/home/noushin/summerTask/pickles/conll_dict.pickle", "rb" ) )
    print("loaded")
else:
    for file in __import__('os').listdir("/home/noushin/summerTask/Conll/"):
        conll[idx] = (word_sent_dict, cntr) = conll_full_parser.parse_full_conll(
            "/home/noushin/summerTask/Conll/" + file, file)
        idx += 1
    pickle.dump( conll, open( "/home/noushin/summerTask/pickles/conll_dict.pickle", "wb" ) )
    print("dumped")
elapsed_time = (time.time() - start_time )
##("akheish {}".format(elapsed_time))
#sys.exit(0)
"""
for file in __import__('os').listdir("/home/noushin/summerTask/Conll/"):
    conll[idx] = (word_sent_dict, cntr) = conll_full_parser.parse_full_conll("/home/noushin/summerTask/Conll/" + file, file)
    idx += 1
    #print(idx)
"""


# kidnap_lst=list()
# for doc_idx in range(len(conll)):
#    if ( ('ransom' in conll[doc_idx][0].keys() ) & ('kidnap' in conll[doc_idx][0].keys()) ):
#        kidnap_lst.append(doc_idx)







# len(all_keys)
all_keys = list()
P_Words = list()
C_Dist = dict()
#@profile
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
# conll.clear()
len(word_sent)

for doc_idx in range(len(word_sent)):
    keys = word_sent[doc_idx][0].keys()
    for key in keys:
        word_sent[doc_idx][0][key] = np.unique(word_sent[doc_idx][0][key])

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
less_500_idx = np.where(np.array(Count) < 500)[0]

frequent_words_idx = np.array(list(set(great_1_idx) & set(less_500_idx)))

len(frequent_words_idx)

Count = np.array(Count)[frequent_words_idx]

len(Count)

all_keys = np.array(all_keys)[frequent_words_idx]  # only worods with occurance count of at lest 2 times are selected.
len(all_keys)
##print(type(all_keys))

np.max(Count)
i = 0
words_dict = dict()
for word_idx in range(len(all_keys)):
    words_dict[all_keys[word_idx]] = Count[word_idx]

all_keys = np.sort(all_keys)

Count = [0] * len(all_keys)
for word_idx in range(len(all_keys)):
    Count[word_idx] = words_dict[all_keys[word_idx]]

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

a = len(C_Dist.keys())
##print(a)
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
            pmi_matrix[word1_idx, word2_idx] = P_Dist[(word1, word2)] / (P_Words[word1_idx] * P_Words[word2_idx])
            pmi_matrix[word2_idx, word1_idx] = pmi_matrix[word1_idx, word2_idx]

P_Dist.clear()
C_Dist.clear()

# distance_matrix= np.zeros(  (len(all_keys) , len(all_keys) ) )
max_pmi = np.max(pmi_matrix)

distance_matrix = max_pmi - pmi_matrix

# for word1_idx in range(len(all_keys)-1 ) :
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
n_clusters = 6
y = sch.fcluster(clust_tree, n_clusters, 'maxclust')  # 100

cls_cnt = Counter(y)
#print(cls_cnt)
#cls_cnt.most_common(6)
cls_cnt.most_common(6)


# ------------------------Clusters syntactic -----------------------------


def extract_cluster_syntactic(cls_members):
    cls_syntactics = []
    for idx in range(len(cls_members)):
        if ':' in cls_members[idx]:
            colon_idx = cls_members[idx].index(':')
            verb = cls_members[idx][0:colon_idx]
            cls_syntactics.append(verb + ':o')
            cls_syntactics.append(verb + ':s')
        else:
            verb = cls_members[idx]
            cls_syntactics.append(verb + ':o')
            cls_syntactics.append(verb + ':s')
    cls_syntactics = np.unique(cls_syntactics)
    return (cls_syntactics)


def extract_Cluster_CR_SP(cls_syntactics):
    Cluster_CR = dict()
    Cluster_SP = dict()
    for idx in range(len(cls_syntactics)):
        if cls_syntactics[idx] in CR_Dict.keys():
            Cluster_CR[cls_syntactics[idx]] = CR_Dict[cls_syntactics[idx]]
        if cls_syntactics[idx] in SP_Dict.keys():
            Cluster_SP[cls_syntactics[idx]] = SP_Dict[cls_syntactics[idx]]
    return Cluster_CR, Cluster_SP


# --------------------------Selectional Preferences for all Documents------------
SP = dict()
idx = 0

for file in __import__('os').listdir("Conll/"):
    SP[idx] = selectional_preferences.selectional_preferencer("/home/noushin/summerTask/Conll/" + file,
                                                              "/home/noushin/summerTask/select_pe")
    idx += 1

SP_Dict = dict()
SP_Dict = SP[0]
#print("SP_Dict: ", SP_Dict)

for sp_idx in range(1, len(SP)):
    for key in SP[sp_idx].keys():
        if key in SP_Dict.keys():
            SP_Dict[key] = SP_Dict[key] + SP[sp_idx][key]
        else:
            SP_Dict[key] = SP[sp_idx][key]
#print("SP_Dict jadid: ", SP_Dict)
# sp_out=selectional_preferencer("D:/summer_task-dev/dev-muc3-0001-0100.conll_bk", "D:/summer_task-dev/select_pe")


# ----------------Coreference Resolution for all XMLs --------------
#path = 'D:/summer_task-dev/xml_files'
path = '/home/noushin/summerTask/xml_files'

allFilesSentences = coref_Vector.returnSentences(path)
allFilesCoreferences = coref_Vector.returnCoRefs(path)
allFilesSentencesDependencies = coref_Vector.returnDependencies(path)
CR_Dict = coref_Vector.returnCorefVectors(allFilesSentences, allFilesCoreferences, allFilesSentencesDependencies)
##testfile.write("Coref {}".format(CR_Dict))
##testfile.write("Selec {}".format(SP_Dict))

# --------------------------------------------kidnapp cluster-----------------------------
kidnap_idx = np.where(all_keys == 'kidnap')
##print("all_keys: kidnap:   ",all_keys)
output_file.write("kidnap_idx: {}\r\n".format(kidnap_idx))

"""

print(all_keys)
print("type(kidnap_idx): ",type(kidnap_idx))
print("(kidnap_idx): ",kidnap_idx)
print("(len kidnap_idx): ",len(kidnap_idx))

print("y,type(y), len(y)",y,type(y), len(y))
"""
kidnap_cls = y[kidnap_idx]
##print("(kidnap_cls):  ",(kidnap_cls))
output_file.write("kidnapp clusters: {}\r\n".format(kidnap_cls))

"""
print("type(kidnap_cls):  ",type(kidnap_cls))
print("(kidnap_cls):  ",kidnap_cls)
print("(len  kidnap_cls):  ",len(kidnap_cls))
"""
members_idx = np.where(y == kidnap_cls)
##print("(members_idx)",members_idx)
output_file.write("members_idx: {}\r\n".format(members_idx))

"""
print("type(members_idx): ",type(members_idx))
print("(members_idx)",members_idx)
print("(len members_idx)",len(members_idx))
"""
cls_members = all_keys[members_idx]
##print("(cls_members): ",cls_members)
output_file.write("cls_members: {}\r\n".format(cls_members))

"""
print("type(cls_members): ",type(cls_members))
print("(cls_members): ",cls_members)
print("(len cls_members)",len(cls_members))
"""
# ------------cluster syntactic relation extraction --------
cls_syntactics = extract_cluster_syntactic(cls_members)
##print("cls_syntactics ", cls_syntactics )
output_file.write("cls_syntactics: {}\r\n".format(cls_syntactics))


# ------------Cluster CR adn SP  Extraction-------------------
Cluster_CR, Cluster_SP = extract_Cluster_CR_SP(cls_syntactics)
##print("Cluster_CR", Cluster_CR)
##print("Cluster_SP", Cluster_SP)
# ----------syntactic clustering--------------

clusters = Syntactic_Clustering.syntactic_clustering(Cluster_CR, Cluster_SP)
##print(clusters)
output_file.write("clusters: {} \r\n".format(clusters))


#--------------------------------------------------
attack_idx = np.where(all_keys == 'attack')
"""

print(all_keys)
print("type(kidnap_idx): ",type(kidnap_idx))
print("(kidnap_idx): ",kidnap_idx)
print("(len kidnap_idx): ",len(kidnap_idx))

print("y,type(y), len(y)",y,type(y), len(y))
"""
attack_cls = y[attack_idx]
"""
print("type(kidnap_cls):  ",type(kidnap_cls))
print("(kidnap_cls):  ",kidnap_cls)
print("(len  kidnap_cls):  ",len(kidnap_cls))
"""
members_idx = np.where(y == attack_cls)
"""
print("type(members_idx): ",type(members_idx))
print("(members_idx)",members_idx)
print("(len members_idx)",len(members_idx))
"""
cls_members = all_keys[members_idx]
"""
print("type(cls_members): ",type(cls_members))
print("(cls_members): ",cls_members)
print("(len cls_members)",len(cls_members))
"""
# ------------cluster syntactic relation extraction --------
cls_syntactics = extract_cluster_syntactic(cls_members)

# ------------Cluster CR adn SP  Extraction-------------------
Cluster_CR, Cluster_SP = extract_Cluster_CR_SP(cls_syntactics)

# ----------syntactic clustering--------------

clusters = Syntactic_Clustering.syntactic_clustering(Cluster_CR, Cluster_SP)

#--------------------------------------------------
output_file.write("Attack cluster: \r\n")
output_file.write("attack_idx: {}\r\n".format(attack_idx))
output_file.write("attack clusters: {}\r\n".format(attack_cls))
output_file.write("members_idx: {}\r\n".format(members_idx))
output_file.write("cls_members: {}\r\n".format(cls_members))
output_file.write("cls_syntactics: {}\r\n".format(cls_syntactics))
output_file.write("clusters: {} \r\n".format(clusters))

# ----------------------------------------------Cluster1--------------------
large_cls_idx = cls_cnt.most_common(10)[0][0]
cls_members_idx = np.where(y == large_cls_idx)

cls_members = np.array(all_keys)[cls_members_idx]

# ------------cluster syntactic relation extraction --------
cls_syntactics = extract_cluster_syntactic(cls_members)

# -------------Cluster CR adn SP  Extraction-------------------
Cluster_CR, Cluster_SP = extract_Cluster_CR_SP(cls_syntactics)

# ----------syntactic clustering--------------

clusters = Syntactic_Clustering.syntactic_clustering(Cluster_CR, Cluster_SP)
#print(clusters)
#print("11111111111111111111111111111111111111111")
output_file.write("First_cluster cluster: \r\n")
output_file.write("cls_members_idx: {}\r\n".format(cls_members_idx))
output_file.write("cls_members: {}\r\n".format(cls_members))
output_file.write("cls_syntactics: {}\r\n".format(cls_syntactics))
output_file.write("clusters: {} \r\n".format(clusters))

# -----------------------------------------------Cluster2--------------------
large_cls_idx = cls_cnt.most_common(10)[1][0]
cls_members_idx = np.where(y == large_cls_idx)

cls_members = np.array(all_keys)[cls_members_idx]

# ------------cluster syntactic relation extraction --------
cls_syntactics = extract_cluster_syntactic(cls_members)

# -------------Cluster CR adn SP  Extraction-------------------
Cluster_CR, Cluster_SP = extract_Cluster_CR_SP(cls_syntactics)

# ----------syntactic clustering--------------

clusters = Syntactic_Clustering.syntactic_clustering(Cluster_CR, Cluster_SP)
#print(clusters)
#print("11111111111111111111111111111111111111111")
# -------------Cluster3--------------------
##
"""

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
print("done done done")


"""

output_file.close()

