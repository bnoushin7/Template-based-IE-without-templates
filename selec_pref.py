'''
Created on 11/12/17
Sample code for  
@author: Noushin
'''

from collections import Counter
from nltk.chunk.named_entity import NEChunkParser


def selectional_preferencer(indata, out_dict):
    with open(indata, "r") as file:
        lines = file.readlines()
    lines = lines + ['\n']
    verbs = set(["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"])
    Nouns = set(["NN", "NNP", "NNS", "NNPS"])
    subjects = set(["nsubj", "nsubjpass", "csubj", "csubjpass"])
    sentence_index = 0
    verb_dict_temp = {}
    new_dict = {}
    verb_obj = []
    main_list = []
    cnt1 = 0
    cnt2 = 0
    cnt3 = 0
    cnt4 = 0

    block_counter = 0

    for c, line in enumerate(lines):
        line = line.strip()

        if not line:

            verb_dict_temp.clear()
            sentence_index += 1
            block_counter = c

        else:

            linearr = line.split("\t")
            wordIndex = linearr[0]
            token = linearr[1]
            lemma = linearr[2]
            POS = linearr[3]
            NER = linearr[4]
            head = linearr[5]
            depRel = linearr[6]

            if POS in verbs:
                verb_dict_temp[int(wordIndex)] = lemma

            isObject = False
            isSubject = False
            isNER = False

            if depRel == "dobj":
                isObject = True

            if depRel in subjects:
                isSubject = True

            if NER != "O":
                isNER = True

            if isObject or isSubject:
                if POS != "PRP" and POS != "DT" and POS != "WDT" and POS in Nouns:
                    index_v = int(head)
                    verb_of_obj = None

                    try:
                        verb_of_obj = verb_dict_temp[index_v]

                    except KeyError:

                        bc = -1 if block_counter == 0 else block_counter
                        nline = lines[bc + index_v]
                        nlinearr = nline.split("\t")
                        nwordIndex = nlinearr[0]
                        nlemma = nlinearr[2]
                        verb_dict_temp[int(nwordIndex)] = nlemma
                        if nlinearr[3] in verbs:
                            verb_of_obj = verb_dict_temp[index_v]

                    if verb_of_obj is not None:

                        if isNER:
                            NER_type = NER

                        if isSubject and isNER:
                            previous_key = verb_of_obj + "-subject"
                            if previous_key in new_dict:
                                new_dict[previous_key].append((NER_type, NER_type))
                            else:
                                new_dict[previous_key] = [(NER_type, NER_type)]

                        if isSubject and not isNER:
                            previous_key = verb_of_obj + "-subject"
                            if previous_key in new_dict:
                                new_dict[previous_key].append((token, "OTHER"))
                            else:
                                new_dict[previous_key] = [(token, "OTHER")]

                        if isObject and not isNER:
                            previous_key = verb_of_obj + "-object"
                            if previous_key in new_dict:
                                new_dict[previous_key].append((token, "OTHER"))
                            else:
                                new_dict[previous_key] = [(token, "OTHER")]

                        if isObject and isNER:
                            previous_key = verb_of_obj + "-object"
                            if previous_key in new_dict:
                                new_dict[previous_key].append((NER_type, NER_type))
                            else:
                                new_dict[previous_key] = [(NER_type, NER_type)]

    my_dict = {k: Counter(v) for k, v in new_dict.iteritems()}
    print(my_dict)

    with open('{0}_moutputm.txt'.format(out_dict), 'w') as output:
        output.write(str(my_dict))
        output.close()
    return (my_dict)


############################# Testing with a .conll file
selectional_preferencer("dev-muc3-0001-0100.conll", "SP")