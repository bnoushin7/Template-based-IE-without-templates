'''
Created on 8/17/17
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
    Nouns = set(["NN" ,"NNP", "NNS", "NNPS"])
    subjects = set(["nsubj", "nsubjpass", "csubj", "csubjpass"])
    objects = set(["dobj", "iobj"])
    sentence_index = 0
    verb_dict_temp = {}
    new_dict = {}


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

            if depRel in objects:
                isObject = True

            if depRel in subjects:
                isSubject = True

            if NER != "O":
                isNER = True


            if isObject or isSubject:
                if POS != "PRP" and POS !="DT" and POS !="WDT" and POS in Nouns:
                    index_v = int(head)
                    verb_of_obj = None

                    try:
                        verb_of_obj = verb_dict_temp[index_v]

                    except KeyError:
                        #print("this key doesn't exist:", index_v)

                        #print("looking for line:", index_v)
                        bc = -1 if block_counter == 0 else block_counter
                        nline = lines[bc + index_v]
                        nlinearr = nline.split("\t")
                        nwordIndex = nlinearr[0]
                        nlemma = nlinearr[2]
                        #print("new entry:", nwordIndex, nlemma)
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
                                new_dict[previous_key].append((lemma,"OTHER"))
                            else:
                                new_dict[previous_key] = [(lemma,"OTHER")]

                        if isObject and not isNER:
                            previous_key = verb_of_obj + "-object"
                            if previous_key in new_dict:
                                new_dict[previous_key].append((lemma,"OTHER"))
                            else:
                                new_dict[previous_key] = [(lemma,"OTHER")]

                        if isObject and isNER:
                            previous_key = verb_of_obj + "-object"
                            if previous_key in new_dict:
                                new_dict[previous_key].append((NER_type, NER_type))
                            else:
                                new_dict[previous_key] = [(NER_type, NER_type)]



    #my_dict = {k:Counter(v) for k,v in new_dict.iteritems()}
    my_dict = {k: Counter(v) for k, v in new_dict.items()}
    #print(my_dict['eat-object']['apple'])


    with open('{0}_output.txt'.format(out_dict), 'w') as output:
        output.write(str(my_dict))

        output.close()

    uniques_list = list(set(vals for values in my_dict.values() for vals in values)) # #list of all unique tupples (name and NER)


    indexing_dict = {val:idx for idx,val in enumerate(uniques_list)} # I have used this dictionary to know the index of each syntactic relations in the list to be
                                                                   # able toaccesseach element count later.
    person_list = [first for first, second in uniques_list if second == "PERSON"]
    organization_list = [first for first, second in uniques_list if second == "ORGANIZATION"]
    location_list = [first for first, second in uniques_list if second == "LOCATION"]
    other_list = [first for first, second in uniques_list if second == "OTHER"] # The tree above lists have only 1 element when printing,
    #maybe they should not be unique?


    final_dict = {} # This is the dictionary, with each syntactic relation as its keys and the feature_vector for each key, as its value
    vec_length = len(uniques_list)
    #for i in my_dict.iterkeys():
    for i in my_dict.keys():  # Here I try to to find the number of occurance of each related syntactic relation using indexing_dict
        final_dict[i] = [0] * vec_length
        val_list = my_dict[i]

        #for j in val_list.iterkeys():
        for j in val_list.keys():
            val_index = indexing_dict[j]
            final_dict[i][val_index] = my_dict[i][j]



    return (my_dict) # I am not sure what to return, maybe we need to retrn final_dict too?


#selectional_preferencer("simple_test.conll", "selec")
selectional_preferencer("dev-muc3-0001-0100.conll_bk", "select_pe")
