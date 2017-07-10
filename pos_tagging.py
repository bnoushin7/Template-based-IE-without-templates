'''
Sample code for POS tagging!
@author: Noushin Behboudi
'''

import nltk

def pos_tagging(input_file, output_file):
    output = open('{0}_pos.txt'.format(output_file), 'w')
    testset = open(input_file).readlines()
    for line in testset:
        line_clean = line.lower().strip()
        tokens = nltk.word_tokenize(line_clean)
        poss = nltk.pos_tag(tokens)
        output.write(line)
        tempPOS = ""
        for word, pos in poss:
            tempPOS += word + "|" + pos + " "
        output.write(tempPOS.strip() + "\n")
        tempPOS = ""
        output.write(u"----------------------\n")
    output.close()



'''
Sample calling:
pos_tagging("dev-muc3-0001-0100","output")
'''

