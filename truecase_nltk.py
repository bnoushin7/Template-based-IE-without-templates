'''
Created on 7/22/17
Sample code for  
@author: Noushin
'''

import nltk

def truecase(text):
    tagged_sent = nltk.pos_tag([word.lower() for word in nltk.word_tokenize(text)])
    normalized_sent = [w.capitalize() if t in ["NNP", "NNPS"] else w for (w, t) in tagged_sent]
    true_cased = normalized_sent[0].capitalize() + ' '+ ' '.join(normalized_sent[1:])
    return true_cased

text = "Ali arm hand tongue . Ali He good bad foot hand toe basketball . Ali and Sarah arm ball goes Samsung in Germany."
print(truecase(text))