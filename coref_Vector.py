'''
Created on 8/5/17
Sample code for coref vector representation
@author: Noushin
'''

from os import listdir
import xml.etree.ElementTree as ET

# this is maximum number of xml files that you want to process at this time.
numOfDocs = 4


def returnSentences(path):
    files = listdir(path)
    allFilesSentences = {}
    count = numOfDocs;
    for f in files:
        count -= 1
        if count < 0:
            break
        tree = ET.parse(path + "/" + f)
        root = tree.getroot()
        sentences = root.findall("./document/sentences/sentence")
        allSentences = {}
        '''
        this_sentence is a dictionary of dictionary of key=sentence_id and value=the whole this_token dictionary
        '''
        for sent in sentences:
            thisSentence = {}
            sentId = sent.get('id')
            tokens = sent.findall("./tokens/token")
            for t in tokens:
                thisToken = {}
                thisToken["id"] = t.get('id')
                thisToken["pos"] = t.find('POS').text
                thisToken["word"] = t.find('word').text
                thisToken["lemma"] = t.find('lemma').text
                thisToken["NER"] = t.find('NER').text
                thisSentence[thisToken["id"]] = thisToken
                #print("sentencing\n")
            allSentences[sentId] = thisSentence

        allFilesSentences[f] = allSentences
    return allFilesSentences


def returnDependencies(path):
    files = listdir(path)
    allFilesSentencesDependencies = {}
    count = numOfDocs;
    for f in files:
        count -= 1
        if count < 0:
            break
        tree = ET.parse(path + "/" + f)
        root = tree.getroot()
        sentences = root.findall("./document/sentences/sentence")
        allSentencesDependencies = {}

        for sent in sentences:
            sentId = sent.get('id')
            thisSentDepends = {}
            allSeenDeps = {}
            dependencies = sent.findall("./dependencies")
            for depen in dependencies:
                deps = depen.findall("./dep")
                for d in deps:
                    type = d.get('type')
                    if type == 'nsubj' or type == 'dobj' or type == 'iobj' or type == 'nsubjpass':
                        newDep = {}
                        newDep['governor'] = d.getchildren()[0].get('idx')
                        newDep['dependent'] = d.getchildren()[1].get('idx')
                        newDep['type'] = type

                        key = newDep['governor'] + "-" + newDep['type'] + "-" + newDep['dependent']
                        if key in allSeenDeps:
                            continue
                        allSeenDeps[key] = True
                        thisSentDepends[len(thisSentDepends) + 1] = newDep
            allSentencesDependencies[sentId] = thisSentDepends
        allFilesSentencesDependencies[f] = allSentencesDependencies

    return allFilesSentencesDependencies


def returnCoRefs(path):
    files = listdir(path)
    allFilesCoreferences = {}
    count = numOfDocs
    for f in files:
        count -= 1
        if count < 0:
            break
        tree = ET.parse(path + "/" + f)
        root = tree.getroot()
        coreferences = root.findall("./document/coreference/coreference")
        allCoreferences = {}

        for coref in coreferences:
            mens = coref.findall('mention')
            mentions = {}
            for m in mens:
                thisMention = {}
                thisMention["sentId"] = m.find('sentence').text
                thisMention["start"] = m.find('start').text
                thisMention["end"] = m.find('end').text
                thisMention["head"] = m.find('head').text
                thisMention["text"] = m.find('text').text
                mentions[len(mentions) + 1] = thisMention
            allCoreferences[len(allCoreferences) + 1] = mentions
        # print allSentences
        allFilesCoreferences[f] = allCoreferences
    # print 'parsed ', f
    return allFilesCoreferences


def returnCorefVectors(allFilesSentences, allFilesCoreferences, allFilesSentencesDependencies):
    vectors = {}

    for file in allFilesSentences:
        sentences = allFilesSentences[file]
        corefs = allFilesCoreferences[file]

        for c in corefs:
            mentions = corefs[c]
            syntacticRelations = []
            for m in mentions:
                tokenId = mentions[m]['head']
                sentId = mentions[m]['sentId']
                sentence = sentences[sentId]
                dependencies = (allFilesSentencesDependencies[file])[sentId]
                for d in dependencies:
                    dep = dependencies[d]['dependent']  # this is like the noun (sub/obj)
                    gov = dependencies[d]['governor']  # this is like the verb
                    if dep == tokenId:
                        type = dependencies[d]['type']
                        relation = ''
                        if 'subj' in type:
                            relation = ':s'
                        else:
                            relation = ':o'
                        t = sentence[gov]
                        if t['pos'].startswith('V'):
                            syntacticRelations.append(t['lemma'] + relation)

            if len(syntacticRelations) >= 2:
                for s1 in syntacticRelations:
                    v = {}
                    if s1 in vectors:
                        v = vectors[s1]
                    for s2 in syntacticRelations:
                        if s1 == s2:
                            continue
                        if s2 in v:
                            v[s2] = v[s2] + 1
                        else:
                            v[s2] = 1
                    vectors[s1] = v
    print vectors

    feat_vect = vectors.keys() #list of all syntact relations
    vec_length = len(feat_vect) #we wan our features vector be this size
    final_dict = {} # This is the dictionary, with each syntactic relation as its keys and the feature_vector for each key, as its value

    indexing_dict =  {val:idx for idx,val in enumerate(feat_vect)} # I have used this dictionary to know the index of each syntactic relations in the list to be
                                                                   # able toaccesseach element count later.


    for i in vectors.iterkeys(): # Here I try to to find the number of occurance of each related syntactic relation using indexing_dict
        final_dict[i] = [0] * vec_length
        val_dict = vectors[i]

        for j in val_dict.iterkeys():
            idx = indexing_dict[j]
            final_dict[i][idx] = vectors[i][j]


    return vectors # I am not sure what to return, maybe we need to retrn final_dict too?





path = '/home/noushin/summerTask/xml_files'
allFilesSentences = returnSentences(path)
allFilesCoreferences = returnCoRefs(path)
allFilesSentencesDependencies = returnDependencies(path)
returnCorefVectors(allFilesSentences, allFilesCoreferences, allFilesSentencesDependencies)
