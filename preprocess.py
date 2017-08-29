import os

os.chdir(os.path.expanduser('~') + os.sep + "Downloads/stanford-corenlp-full-2017-06-09")
def func(filename, outputpath):
    command = """java -cp "*" -Xmx8g edu.stanford.nlp.pipeline.StanfordCoreNLP -outputFormat conll -outputDirectory %s -annotators tokenize,ssplit,truecase,pos,lemma,ner,depparse -filelist %s -truecase.overwriteText"""%(outputpath, filename)

    os.system(command)    
func("list.ls", "muc3")
