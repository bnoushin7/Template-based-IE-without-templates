'''Created on 7/11/17
Code that finds the noun for each Verb, the input of the noun_finder is the verb and it outputs its related nouns.
It just works for lemma
@author: Noushin
'''


import re
from nltk.corpus import wordnet
list_of_related_nouns = []


def noun_finder(verb_word):
    list_of_related_nouns = []
    for lemma in wordnet.lemmas(verb_word):
        for related_form in lemma.derivationally_related_forms():
            for synset in wordnet.synsets(related_form.name()):
                cln = re.sub('Synset\(\'', '', str(synset))
                cln = cln.split('.')[0]
                if cln not in list_of_related_nouns:
                    list_of_related_nouns.append(cln)
    return list_of_related_nouns



ev= wordnet.synset('event.n.01')
exp= wordnet.synsets('explosion')[0]
text = ev.path_similarity(exp)


#print noun_finder("explode")
'''
it just works for lemma
Sample calling
print noun_finder("explode")
or 
_List = noun_finder("explode")
'''



