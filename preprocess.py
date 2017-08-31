import os

os.chdir(os.path.expanduser('~') + os.sep + "Downloads/stanford-corenlp-full-2017-06-09")
def func(inputDirectory, outputpath):
    for file in __import__('os').listdir(inputDirectory):
        command = """java -cp "*" -Xmx8g edu.stanford.nlp.pipeline.StanfordCoreNLP -outputFormat conll -outputDirectory %s -annotators tokenize,ssplit,truecase,pos,lemma,ner,depparse -filelist %s -truecase.overwriteText"""%(outputpath, inputDirectory)

    os.system(command)    
func("/home/noushin/summerTask/Sub_Files", "muc_output")
