'''
Sample code for detecting nouns out of corpus
@author: Noushin Behboudi
'''

import nltk
from nltk.tokenize import word_tokenize, sent_tokenize

def noun_detection(input_file, output_name):
    output_noun = open('{0}_noun.txt'.format(output_name),'w')
    testset = open(input_file).readlines()
    nouns = []
    for line in testset:
        line_clean = line.lower().strip()
        tokens = nltk.word_tokenize(line_clean)
        poss = nltk.pos_tag(tokens)
        for word,pos in poss:
            if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS'):
                output_noun.write(word + "\n")
                nouns.append(word)
        output_noun.write(u"----------------------------------------------\n")
    output_noun.close()
    print("nouns: {}  ".format(len(nouns)))


'''
sample calling!
noun_detection("dev-muc3-0001-0100","outp")
'''

































def verbs_detection(input_file, output_name):
    output = open('{0}.txt'.format(output_name),'w')
    output_noun = open('{0}_noun.txt'.format(output_name),'w')
    output_verb = open('{0}_verb.txt'.format(output_name),'w')
    testset = open(input_file).readlines()
    nouns = []
    verbs = []
    y = 0
    for line in testset:
        line_clean = line.lower().strip()
        tokens = nltk.word_tokenize(line_clean)
        poss = nltk.pos_tag(tokens)
        output.write(line)
        tempPOS = ""
        for word,pos in poss:
            y +=1
            if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS'):
                nouns.append(word)
                output_noun.write(word + "\n")
            if (pos == 'VB' or pos == 'VBD' or pos == 'VBG' or pos == 'VBN' or pos == 'VBZ' or pos == 'VBP'):
            #if (pos == 'VB' or pos == 'VBD' or pos == 'VBG' or pos == 'VBN' or pos == 'VBZ' or pos == 'VBP' or pos == 'MD'):
                output_verb.write(word + "\n")
                verbs.append(word)
            tempPOS += word + "|" + pos + " "
        output.write(tempPOS.strip() + "\n")
        tempPOS = ""
        output.write(u"----------------------\n")
        output_verb.write(u"----------------------\n")
        output_noun.write(u"----------------------\n")
    output.close()
    output_verb.close()
    output_noun.close()
    print("nouns: {}  verbs: {}  all: {}".format(len(nouns) , len(verbs), y))