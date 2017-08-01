
import nounOfVerbFinder

def reverse_dictionary(first_fmt):
    scnd_fmt = dict()
    for key, value in first_fmt.items():
        for item in value:
            if item in scnd_fmt.keys():
                scnd_fmt[item].append(key)
            else:
                scnd_fmt[item] = [key]

    return scnd_fmt
    print(scnd_fmt)


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

            if verb_obj:
                main_dict[sentence_index] = verb_obj
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
                noun_list = nounOfVerbFinder.noun_finder(lemma)
                verb_obj.extend(noun_list)
                for ii in noun_list:
                    print("nouns of {} is {}".format(lemma, ii))

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
    correct_dict = reverse_dictionary(main_dict)
    print(correct_dict)
    return correct_dict

#parse_full_conll("testkol.test","dict")
parse_full_conll("dev-muc3-0001-0100.conll","dict")

