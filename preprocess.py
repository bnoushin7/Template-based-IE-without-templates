
import os

print("{}".format(os.getcwd()))
def func(inputDirectory, outputpath):
    i = 0
    os.chdir(os.path.expanduser('~') + os.sep + "Downloads/stanford-corenlp-full-2017-06-09")
    for file in __import__('os').listdir(inputDirectory):
        command = 'java -cp "*" -Xmx8g edu.stanford.nlp.pipeline.StanfordCoreNLP -outputFormat conll -outputDirectory %s -annotators tokenize,ssplit,truecase,pos,lemma,ner,depparse -file %s -truecase.overwriteText'%(outputpath, inputDirectory+"/"+file)

        os.system(command)
        #print(command)
        i +=1
        print(i)
        print ("done {}".format(file))
func("/home/noushin/summerTask/sub_files", "muc_outputs")
print("Done!")

