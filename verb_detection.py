'''
Sample code for detecting verbs out of corpus
@author: Noushin Behboudi
'''

import nltk


def verb_detection(input_file, output_name):
    output_verb = open('{0}_verb.txt'.format(output_name), 'w')
    testset = open(input_file).readlines()
    verbs = []
    #y = 0
    for line in testset:
        line_clean = line.lower().strip()
        tokens = nltk.word_tokenize(line_clean)
        poss = nltk.pos_tag(tokens)
        for word, pos in poss:
            if (pos == 'VB' or pos == 'VBD' or pos == 'VBG' or pos == 'VBN' or pos == 'VBZ' or pos == 'VBP'):
                output_verb.write(word + "\n")
                verbs.append(word)
        output_verb.write(u"----------------------------------------------\n")
    output_verb.close()
    return  verbs
    print("verbs: {}  ".format(len(verbs)))


'''
sample calling!
verb_detection("dev-muc3-0001-0100","outp")
'''
