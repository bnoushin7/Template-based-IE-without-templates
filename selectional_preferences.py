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
    verb_obj = []
    #main_dict = {}
    main_list = []
    cnt1 = 0
    cnt2 = 0
    cnt3 = 0
    cnt4 = 0

    block_counter = 0

    for c, line in enumerate(lines):
        line = line.strip()

        #if the line is empty, clear verb_obj and verb_dict_temp
        if not line:
            #if verb_obj:
            #main_dict[sentence_index] = verb_obj
            ##main_list.extend(verb_obj)
            verb_dict_temp.clear()
            ##verb_obj = []
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

            #if depRel == "dobj":
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
                        ##print("this key doesn't exist:", index_v)

                        ##print("looking for line:", index_v)
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
                                #new_dict[previous_key].append(NER_type)
                                new_dict[previous_key].append((NER_type, NER_type))
                            else:
                                #new_dict[previous_key] = [NER_type]
                                new_dict[previous_key] = [(NER_type, NER_type)]

                        
                        if isSubject and not isNER:
                            previous_key = verb_of_obj + "-subject"
                            if previous_key in new_dict:
                                #new_dict[previous_key].append(token)
                                new_dict[previous_key].append((lemma,"OTHER"))
                            else:
                                #new_dict[previous_key] = [token]
                                new_dict[previous_key] = [(lemma,"OTHER")]

                        if isObject and not isNER:
                            previous_key = verb_of_obj + "-object"
                            if previous_key in new_dict:
                                #new_dict[previous_key].append(token)
                                new_dict[previous_key].append((lemma,"OTHER"))
                            else:
                                #new_dict[previous_key] = [token]
                                new_dict[previous_key] = [(lemma,"OTHER")]

                        if isObject and isNER:
                            previous_key = verb_of_obj + "-object"
                            if previous_key in new_dict:
                                #new_dict[previous_key].append(NER_type)
                                new_dict[previous_key].append((NER_type, NER_type))
                            else:
                                #new_dict[previous_key] = [NER_type]
                                new_dict[previous_key] = [(NER_type, NER_type)]



    my_dict = {k:Counter(v) for k,v in new_dict.iteritems()}
    #print(my_dict)
    #print(my_dict['eat-object']['apple'])
    print("----------------EEEEEE----------------------------")
    #print(my_dict['grant-object'][('status', 'OTHER')])
    print("------------------EEEEE--------------------------")



    with open('{0}_output.txt'.format(out_dict), 'w') as output:
        output.write(str(my_dict))

        output.close()

    uniques_list = list(set(vals for values in my_dict.values() for vals in values))
    #print(uniques_list)



    indexing_dict = {val:idx for idx,val in enumerate(uniques_list)}
    person_list = filter(lambda i: i[1] == 'PERSON', uniques_list)
    organization_list = filter(lambda i: i[1] == 'ORGANIZATION', uniques_list)
    other_list = filter(lambda i: i[1] == 'OTHER', uniques_list)
    location_list = filter(lambda i: i[1] == 'LOCATION', uniques_list)

    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    print(person_list)
    print("%%%%%%%%%")
    print(other_list)
    print("%%%%%%%%%")
    print(organization_list)
    print("%%%%%%%%%")
    print(location_list)
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

    #print(indexing_dict)



    final_dict = {}
    vec_length = len(uniques_list)
    for i in my_dict.iterkeys():
        final_dict[i] = [0] * vec_length
        val_list = my_dict[i]

        for j in val_list.iterkeys():
            val_index = indexing_dict[j]
            final_dict[i][val_index] = my_dict[i][j]

    #print(final_dict)


    return (my_dict)


#selectional_preferencer("simple_test.conll", "selec")
selectional_preferencer("dev-muc3-0001-0100.conll_bk", "select_pe")
print("lis")