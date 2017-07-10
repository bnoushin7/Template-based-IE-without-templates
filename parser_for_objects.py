'''
Sample code for detecting verbs : objects of the corpus
It searches to find "verb:dobj"
@author: Noushin
'''

import nltk
#nltk.download('maxent_treebank_pos_tagger')
from nltk.parse.stanford import StanfordParser
from nltk.parse.stanford import StanfordDependencyParser
from nltk.parse.stanford import StanfordNeuralDependencyParser
from nltk.tag.stanford import StanfordPOSTagger, StanfordNERTagger
from nltk.tokenize.stanford import StanfordTokenizer
import os
os.environ['JAVA_HOME'] = "/usr/lib/jvm/java-8-openjdk-amd64"
stanford_pos_dir = '/home/noushin/stanford-postagger-full-2015-04-20/'
eng_model_filename= stanford_pos_dir + 'models/english-left3words-distsim.tagger'
my_path_to_jar= stanford_pos_dir + 'stanford-postagger.jar'

stanford_parser_dir = '/home/noushin/stanford-parser-full-2015-04-20/'
path_to_jar = stanford_parser_dir  + "stanford-parser.jar"
path_to_models_jar = stanford_parser_dir + "stanford-parser-3.5.2-models.jar"

dependency_parser = StanfordDependencyParser(path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar)

def to_utf8(text):
    if type(text) is tuple:
        return [ to_utf8(i) for i in text]
    elif type(text) is unicode:
        return text.encode('utf8')
    else:
        return text

def verb_obj_parsing(input_file, output_file):
    import re
    output = open("{0}.txt".format(output_file), 'w')
    dataset = open(input_file,"r")

    #file = open("dev-muc3-0001-0100", "r")
    # file = open("test.txt", "r")
    doclist = [line for line in dataset]
    docstr = ''.join(doclist)
    sents = re.split(r'[.!?]', docstr)
    print(len(sents))

    result = dependency_parser.raw_parse_sents(sents)

    for sentence in result:
        tmp = list(sentence.next().triples())
        # tmp = list(sentence.triples())
        for triple in tmp:
            #print("type tmp is {}  triple {}  sentence {}".format(type(tmp), type(triple), type(sentence)))
            if triple[1] == u'dobj':
                # print(triple[1], triple[0][0] ,triple[2][0] )
                tmp_str = triple[0][0], ": ", triple[2][0]
                output.write(' '.join(to_utf8(tmp_str)))
                output.write('\n')
    output.close()




'''
sample calling!
verb_obj_parsing("dev-muc3-0001-0100","outp")
'''







