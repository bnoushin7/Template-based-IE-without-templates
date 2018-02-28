'''
What are our data structures?
1- all_unique_words : all unique words of all documents, for all documents, extract all the words and then make them unique
2- all_templates_triggers : dictionary of key: template, values all trigger words for templates
3- clusterWords_docs: dictionay of



### extract all documents of a template

Make_IR_corpus --> for each template, find all the documents that are related to that template
1- if IR(d,c)> 0.4
Then what is IR ?
if coverage(d,c) > min(3, |c|/4)
    it is equal to avgm
else 0

So calc IR(d,c)
cvgm is what? number of seen cluster words, so the number of times each word of cluster has been seen.
It can be repeated

What is avgm then? this is match score and is the average of number of times the words in cluster c apperas in document d.

### Document classification
''
Now document classification starts, how? if a document has at least one trigger word (how trigger words are defined?)
And P(w,t) > 0.2

then What is P(w,t)?

P(w,t) = (PIRt(w))/(for all s PIRs(w))

Then what is PIRt(w) = (Ct(w))/(for all words Ct(v))
Indeed it is the number of times word w has been repeated in IR-corpus of template t

I think in the end, it is the number of times word "w" has been repeated in IR_corpus of template t devided by the number of times
each word has been seen in IR corpus of template t, I mean the whole words of Ir corpus of t?
Devided by this things for word w in IR corpus of all templates, does it mean the whole size of our big big template?

Frequency tells us for each word of a template, each documents (or the referred document), how many wih repeat words have
but IR_count tells us for all related documents of a template, how many times a "word" has been seen
R_corpus[template]
template_clusters che sakhtari ast va inke chizi hast kalame haye template ha ro dashte bashe?

contains trigger check if in whole triggers, whole triggers of all templates
'''
from __future__ import division
import numpy



def word_count(word, doc_words):
    count = 0
    for wrd in doc_words:
        if wrd == word:
            count += 1
    return (count)


def word_frequency(Doc_words, cluster):
    clusterWords_docs = dict()
    for word in cluster:
        for doc in Doc_words.keys():
            if word in clusterWords_docs:
                clusterWords_docs[word].append(word_count(word, Doc_words[doc]))
            else:
                clusterWords_docs[word] = [word_count(word, Doc_words[doc])]

    return (clusterWords_docs)


def avgm(document, cluster, clusterWords_docs):  # average number of times for cluster words in document

    count_sum = 0
    for word in cluster:
        count_sum += clusterWords_docs[word][document]
    count_average = count_sum / len(cluster)
    return (count_average)


def cvg(document, cluster, clusterWords_docs):  # word coverage : number of seen cluster words.
    visited_word_count = 0
    for word in cluster:
        if clusterWords_docs[word][document] > 0:
            visited_word_count += 1

    return (visited_word_count)


def ir(document, cluster):  # equvalent to the ir(d,c) formula of the paper.
    clusterWords_docs = word_frequency(Doc_words, cluster)
    if cvg(document, cluster, clusterWords_docs) > min(3, len(cluster) / 4):
        output = avgm(document, cluster, clusterWords_docs)
    else:
        output = 0
    return (output)


def is_retrieved(document,
                 cluster):  # equvalent to the ir(d,c) > 0.4 of the 4.2 section of the paper. if a document is retrieved for a cluster
    if ir(document, cluster) > 0.4:
        return (True)
    else:
        return (False)


def template_IR_corpus(template_cluster):  # return IR_corpus for a template ( relevant documents fo the template)
    corpus = []
    for doc in range(len(Doc_words)):
        if is_retrieved(doc, template_cluster):
            corpus.append(doc)
    return (corpus)


#



def make_IR_corpus():  # generating IR_corpus, i.e. for all templates identifies related documents.
    Template_IR_crpus = dict()
    for temp_clus in range(len(template_clusters)):
        Template_IR_crpus[temp_clus] = template_IR_corpus(template_clusters[temp_clus])
    return (Template_IR_crpus)


def extract_all_words(Doc_words):  # extracting all unique words of the documents of the IR_corpus
    all_words = []
    for doc in range(len(Doc_words)):
        all_words.extend(Doc_words[doc])
    return (numpy.unique(all_words))


def IR_corpus_word_count(template, word):  # equvalent to the Ct(w) of the formula 9 of the paper.
    word_count_sum = 0
    for doc in IR_corpus[template]:
        word_count_sum += word_count(word, Doc_words[doc])
    return (word_count_sum)


def Prob_IR_corpus(template, word):  # equvalent to the formula 9 of the paper.
    word_freq_sum = IR_corpus_word_count(template, word)
    all_word_frequency = 0
    for word in range(len(all_unique_words)):
        all_word_frequency += IR_corpus_word_count(template, all_unique_words[word])

    if all_word_frequency == 0:
        return (0)
    return (word_freq_sum / all_word_frequency)


def conditional_prob(template, word):  # equvalent to the formula 8 of the paper.
    all_template_prob = 0

    template_prob = Prob_IR_corpus(template, word)

    for temp in range(len(template_clusters)):
        all_template_prob += Prob_IR_corpus(temp, word)

    if all_template_prob == 0:
        return (0)
    return (template_prob / all_template_prob)


def template_triggers(template):  # for a template return trigger words of the template.
    triggers = []
    for word in range(len(all_unique_words)):
        if conditional_prob(template, all_unique_words[word]) > 0.2:
            triggers.append(all_unique_words[word])

    return (triggers)


def extract_templates_triggers():  # for all templates, extract triggers words of them.
    all_template_triggers = dict()
    for temp in range(len(template_clusters)):
        all_template_triggers[temp] = template_triggers(temp)
    return (all_template_triggers)


# --------------------Classification of new Documents ---------------
# ------------------------------------------------


def contains_trigger(new_doc, template):  # first condition for classification (section 5.1 of the  paper)

    for word in new_Doc_words[new_doc]:
        if word in all_templates_triggers[template]:
            return (True)
    return (False)


def document_triggers(
        new_doc):  # return for each new doc, triggers of templates which new doc contains those. this is necessary for information extraction step(section 5.2 of the paper)
    template_triggers = dict()
    for temp in range(len(template_clusters)):
        for word in new_Doc_words[new_doc]:
            if word in all_templates_triggers[temp]:
                if temp in template_triggers.keys():
                    template_triggers[temp].append(word)
                else:
                    template_triggers[temp] = [word]
    return (template_triggers)


def average_conditional_prob(template, new_doc):  # second condition for classification.(section 5.1 of the  paper)
    sum_prob = 0
    for word in new_Doc_words[new_doc]:
        sum_prob += conditional_prob(template, word)
    return (sum_prob / len(new_Doc_words[new_doc]))


def classify_document(new_doc, threshold):  # for each new document identifes related templates.
    related_templates = []
    for temp in range(len(template_clusters)):
        if contains_trigger(new_doc, temp) and average_conditional_prob(temp, new_doc) > threshold:
            related_templates.append(temp)
    return (related_templates)


def all_documents_classification(threshold):  # for all new documents identifes related templates.
    new_documens_templates = dict()
    for new_doc in range(len(new_Doc_words)):
        new_documens_templates[new_doc] = classify_document(new_doc, threshold)
    return (new_documens_templates)


# -------------------Test for example--------------
# ---Example :

# template clusters
template_clusters=dict()
template_clusters[0]=["ali","hasan", "mohamad"]
template_clusters[1]=["maryam","zahra"]

#documents in IR_corpus
Doc_words=dict()
Doc_words[0]=["ali","ali","hasan", "mohamad"]
Doc_words[1]=["hasan","ali","hasan","ali"]
Doc_words[2]=["maryam","maryam","hhasan","ali"]
Doc_words[3]=["maryam","zahra"]


# new documents for classification and Information extraction
new_Doc_words=dict()
new_Doc_words[0]=["ali", "mohamad"]
new_Doc_words[1]=["hasan","ali"]
new_Doc_words[2]=["maryam","hasan"]
new_Doc_words[3]=["maryam","zahra"]
new_Doc_words[4]=["mmaryam","zzahra"]








all_unique_words = extract_all_words(Doc_words)  # all uniqe words in IR_corpus
#print(all_unique_words)
IR_corpus = make_IR_corpus()  # making IR_corpus for all templates using Doc_words, a dictionary with keys as templates index and values as arrays of relevent documents for the templates.
#print(IR_corpus)
all_templates_triggers = extract_templates_triggers()  # extracting all triggers for all templates using Doc_words, a dictionary with keys as template index and values as trigger words of the template.
print(all_templates_triggers)
all_new_documents_templates = all_documents_classification(
    0.1)  # identifying all related new documents for templates, a dictionary with keys as new documents indices and values as related templates indices.
fist_new_doc_triggers = document_triggers(
    0)  # for first newe doc, extracts triggers of each templates if new doc contains those triggers, this is necessary for section 5.2 of the paper for information extraction step.

# -------------Recall, Precision and F1 measure calculation-----------
from sklearn.metrics import precision_recall_fscore_support


def is_related_to_template(template,
                           threshold):  # for each template, generates a vector with length equal to new documnets number.
    # and vector at index i is one if ith new document is related to the template, other wise is zero.
    related_documents = []
    for new_doc in range(len(new_Doc_words)):
        if contains_trigger(new_doc, template) and average_conditional_prob(template, new_doc) > threshold:
            related_documents.append(1)
        else:
            related_documents.append(0)
    return (related_documents)


is_related_to_template(0, 0.2)


def evaluate_classification_result(template, threshold,
                                   real_labels):  # for each template, using real_labels of template
    # ( vector of lenght new document number, and for related document which specified manually, vector value is one,
    # and otherwise is zero  ), and classification result, calculates precision, recall and F1 measure.

    evaluation = dict()
    all_docs_labels = is_related_to_template(template, threshold)

    classification_accuracy = precision_recall_fscore_support(real_labels, all_docs_labels, average='binary')
    precision = classification_accuracy[0]
    recall = classification_accuracy[1]
    F1 = classification_accuracy[2]
    evaluation["precision"] = precision
    evaluation["recall"] = recall
    evaluation["F1"] = F1

    return (evaluation)


real_labels = [1, 1, 1, 1, 0]
evaluate_classification_result(0, 0.2, real_labels)

