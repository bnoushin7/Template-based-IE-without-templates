'''
Created on 8/17/17
Sample code for
@author: Noushin
'''


def selectional_preferencer(indata, out_dict):
    with open(indata, "r") as file:
        lines = file.readlines()
    lines = lines + ['\n']
    verbs = set(["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"])
    subjects = set(["nsubj", "nsubjpass", "csubj", "csubjpass"])
    sentence_index = 0
    verb_dict_temp = {}
    verb_obj = []
    #main_dict = {}
    main_list = []

    block_counter = 0

    for c, line in enumerate(lines):
        line = line.strip()

        #if the line is empty, clear verb_obj and verb_dict_temp
        if not line:
            #if verb_obj:
            #main_dict[sentence_index] = verb_obj
            main_list.extend(verb_obj)
            verb_dict_temp.clear()
            verb_obj = []
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
                if POS != "PRP":
                    index_v = int(head)
                    verb_of_obj = None

                    try:
                        verb_of_obj = verb_dict_temp[index_v]

                    except KeyError:
                        print("this key doesn't exist:", index_v)

                        print("looking for line:", index_v)
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
                            verb_obj.append(verb_of_obj + ": subject : " + NER_type)

                        if isSubject and not isNER:
                            verb_obj.append(verb_of_obj + ": subject : " + token)

                        if isObject and not isNER:
                            verb_obj.append(verb_of_obj + ": object : " + token)

                        if isObject and isNER:
                            verb_obj.append(verb_of_obj + ": object : " + NER_type)

    with open('{0}_output.txt'.format(out_dict), 'w') as output:
        output.write(str(main_list))

        output.close()
    return (main_list)


#selectional_preferencer("simple_test.conll", "selectt")
selectional_preferencer("dev-muc3-0001-0100.conll_bk", "select_pe")