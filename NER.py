'''
Sample code for Name Entity Recognition for a corpus
@author: Noushin
'''

import nltk
from nltk.tokenize import word_tokenize, sent_tokenize



def NER(input_file, output_file):
    output = open('{0}_NER.txt'.format(output_file), 'w')
    testset = open(input_file).readlines()
    for line in testset:
        line_clean = line.lower().strip()
        tokens = nltk.word_tokenize(line_clean)
        poss = nltk.pos_tag(tokens)
        mylist = []
        for w in poss:
            s = list(w)
            s1 = s[0].upper()
            tmp = (s1, w[1])
            mylist.append(tmp)
        ner_ = nltk.ne_chunk(mylist)
        output.write(str(ner_))
        output.write(u"----------------------\n")
    output.close()

#output = open('output.txt','w')
#testset = open("dev-muc3-0001-0100").readlines()

NER("dev-muc3-0001-0100","output")
'''
Sample calling:
NER("dev-muc3-0001-0100","output")
'''