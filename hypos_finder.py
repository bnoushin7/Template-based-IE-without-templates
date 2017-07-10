'''
Sample code for detecting verbs and nouns out of corpus
@author: Noushin Behboudi
'''

import nltk
from nltk.corpus import wordnet


def hypo_set(event_word):
    event_synsets = wordnet.synsets(event_word)

    for i in event_synsets:
        print(i)

    for i in event_synsets:
        print(i.name().split(".")[0])

    print('-----------------------------------------------------\n')

    for syns in event_synsets:
        hypers = syns.hypernyms()
        for j in hypers:
            jj = j.name().split(".")[0]
            print(jj)
    print('-----------------------------------------------------\n')

    for syns in event_synsets:
        hypos = syns.hyponyms()
        for k in hypos:
            kk = k.name().split(".")[0]
            print(kk)
    print('-----------------------------------------------------\n')

'''
Sample calling!
hypo_set("computer")
'''




