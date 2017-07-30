
def parse_full_conll(indata, out_dict):
    with open(indata, "r") as file:
        lines = file.readlines()
    output = open('{0}_output.txt'.format(out_dict), 'w')

    # VB VBD VBG VBN VBP VBZ
    verbs = set(["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"])
    sentence_index = 1
    verb_dict_temp = {}
    verb_obj = []
    main_dict = {}
    for line in lines:
        if not line.strip():
            main_string = " ".join(verb_obj)
            if not main_string.strip():
                pass
            else:
                #main_dict[sentence_index] = str(" ".join(verb_obj))
                main_dict[sentence_index] = " ".join(verb_obj)
            verb_dict_temp.clear()
            verb_obj = []
            sentence_index += 1
            continue
        else:

            word_index = line.strip().split("\t")[0]
            lemma = line.strip().split("\t")[2]
            if line.strip().split("\t")[3] in verbs:
                verb_dict_temp[int(word_index)] = lemma
                verb_obj.append(lemma)

            if line.strip().split("\t")[4] != "O" and line.strip().split("\t")[-1] == "dobj":
                NER_type = line.strip().split("\t")[4]
                index_ner = int(line.strip().split("\t")[-2])
                try:
                    verb_of_obj = verb_dict_temp[index_ner]
                    #verb_obj.append(str(verb_of_obj + ":" + NER_type))
                    verb_obj.append(verb_of_obj + ":" + NER_type)
                except:
                    pass
    output.write(str(main_dict))
    output.close()
    print main_dict
    return main_dict

parse_full_conll("testkol.test","dict")