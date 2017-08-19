'''
Created on 8/17/17
Sample code for
@author: Noushin
'''

class Line:
  def __init__(self, wordIndex, token, lemma, POS, NER, head, depRel):
      self.wordIndex = wordIndex
      self.token = token
      self.lemma =lemma
      self.POS = POS
      self.NER = NER
      self.head = head
      self.depRel = depRel



def selectional_preferencer(indata, out_dict):
    with open(indata, "r") as file:
        lines = file.readlines()
    output = open('{0}_output.txt'.format(out_dict), 'w')

    verbs = set(["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"])
    subjects = set(["nsubj", "nsubjpass", "csubj", "csubjpass"])
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
                # verb_obj.append(lemma+": verb")
            if line.strip().split("\t")[-1] == "dobj":
                if line.strip().split("\t")[4] == "O" and line.strip().split("\t")[3] != "PRP":
                    dobj = line.strip().split("\t")[1]
                    index_v = int(line.strip().split("\t")[-2])
                    try:
                        verb_of_obj = verb_dict_temp[index_v]
                        verb_obj.append(verb_of_obj + ": object : " + dobj)
                    except:  # since sometimes the index does not exist in verb dictionary
                        pass

                elif line.strip().split("\t")[4] != "O":
                    NER_type = line.strip().split("\t")[4]
                    index_ner = int(line.strip().split("\t")[-2])
                    try:
                        verb_of_obj = verb_dict_temp[index_ner]
                        # verb_obj.append(str(verb_of_obj + ":" + NER_type))
                        verb_obj.append(verb_of_obj + ":" + NER_type)
                    except:
                        pass

            if line.strip().split("\t")[-1] in subjects:
                if line.strip().split("\t")[4] == "O" and line.strip().split("\t")[3] != "PRP":
                    dobj = line.strip().split("\t")[1]
                    index_v = int(line.strip().split("\t")[-2])
                    try:
                        verb_of_obj = verb_dict_temp[index_v]
                        verb_obj.append(verb_of_obj + ": subject : " + dobj)
                    except:  # since sometimes the index does not exist in verb dictionary
                        pass

                elif line.strip().split("\t")[4] != "O":
                    NER_type = line.strip().split("\t")[4]
                    index_ner = int(line.strip().split("\t")[-2])
                    try:
                        verb_of_obj = verb_dict_temp[index_ner]
                        # verb_obj.append(str(verb_of_obj + ":" + NER_type))
                        verb_obj.append(verb_of_obj + ":" + NER_type)
                    except:
                        pass

    output.write(str(main_dict))
    output.close()
    return (main_dict)


selectional_preferencer("simple_test.conll", "select")

