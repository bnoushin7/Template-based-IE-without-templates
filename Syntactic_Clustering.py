
import sys
from os.path import dirname

textFilePath = "/home/noushin/summerTask/conll_full_parser.py"
textFileFolder = dirname(textFilePath)

sys.path.append(textFileFolder)
import selectional_preferences

import coref_Vector

from sklearn.metrics.pairwise import cosine_distances

import numpy as np


def initialize(vectors):
    clusters = dict()
    clusters = {i: [i] for i in range(len(vectors))}
    return (clusters)


# def r(clusters, cluster1, cluster2):
def r(clusters, cluster1, cluster2, dist_matrix):
    non_zero_count = 0

    similarity_matrix = 1 - dist_matrix
    for clus1_member in clusters[cluster1]:
        for clus2_member in clusters[cluster2]:
            if similarity_matrix[clus1_member, clus2_member] > 0:
                non_zero_count += 1

    return (non_zero_count / (len(clusters[cluster1]) * len(clusters[cluster2])))


# def score(clusters, cluster1,cluster2 ):
def score(clusters, cluster1, cluster2, dist_matrix):
    similarity_matrix = 1 - dist_matrix
    similarity_sum = 0

    for clus1_member in clusters[cluster1]:
        for clus2_member in clusters[cluster2]:
            similarity_sum += similarity_matrix[clus1_member, clus2_member]

    return (similarity_sum * r(clusters, cluster1, cluster2, dist_matrix))


# def clusters_distance(clusters, cluster1 , cluster2 , dist_type):
def clusters_distance(clusters, cluster1, cluster2, dist_type, dist_matrix):
    distance = 0

    if dist_type == "simple":
        for clus1_member in clusters[cluster1]:
            for clus2_member in clusters[cluster2]:
                distance += dist_matrix[clus1_member, clus2_member]

        distance /= len(clusters[cluster1]) * len(clusters[cluster2])

    if dist_type == "sparse_scoring":  # as described in section 4.3.2 of the paper.
        distance = 1 - score(clusters, cluster1, cluster2, dist_matrix)

    return (distance)


# def find_closest_clusters (clusters, dist_type ):
def find_closest_clusters(clusters, dist_type, dist_matrix):
    closest = dict()
    min_distance = np.inf

    for clus1 in range(len(clusters)):
        for clus2 in range(clus1 + 1, len(clusters)):
            # distance=clusters_distance(clusters,clus1, clus2 , dist_type)
            distance = clusters_distance(clusters, clus1, clus2, dist_type, dist_matrix)

            if distance < min_distance:
                min_distance = distance
                merge_candid1 = clus1
                merge_candid2 = clus2

    closest[1] = merge_candid1
    closest[2] = merge_candid2
    return (closest)


# def stop_condition(clusters, stop_type,dist_type, clusters_number, minimum_score):
def stop_condition(clusters, stop_type, dist_type, clusters_number, minimum_score, dist_matrix):
    max_count = 0
    stop = False

    if (len(clusters) == 1):
        return (True)

    if stop_type == "maximum _cluster_members":
        for clus in range(len(clusters)):
            max_count = max(max_count, len(clusters[clus]))
        if max_count > 40:
            stop = True

    if stop_type == "maximum_clusters_number":
        if len(clusters) == clusters_number:
            stop = True

    if stop_type == "minimum_similarity_score":
        # next_closest_clusters=find_closest_clusters (clusters, dist_type )
        next_closest_clusters = find_closest_clusters(clusters, dist_type, dist_matrix)
        # if score(clusters, next_closest_clusters[1],next_closest_clusters[2] ) <minimum_score:
        if score(clusters, next_closest_clusters[1], next_closest_clusters[2], dist_matrix) < minimum_score:
            stop = True

    return (stop)


def merge_clusters(clusters, clus1, clus2):
    new_clusters = dict()
    clusters[clus1].extend(clusters[clus2])
    del clusters[clus2]

    clus = 0
    for key in clusters.keys():
        new_clusters[clus] = clusters[key]
        clus += 1

    return (new_clusters)


# def run_clustering(vectors , clusters_number,dist_type, stop_type, minimum_score ):
def run_clustering(vectors, clusters_number, dist_type, stop_type, minimum_score, dist_matrix):
    clusters = initialize(vectors)

    # while not stop_condition(clusters, stop_type,dist_type, clusters_number,minimum_score):
    while not stop_condition(clusters, stop_type, dist_type, clusters_number, minimum_score, dist_matrix):
        # closest_pair=find_closest_clusters (clusters, dist_type )
        closest_pair = find_closest_clusters(clusters, dist_type, dist_matrix)
        cluster1 = closest_pair[1]
        cluster2 = closest_pair[2]

        clusters = merge_clusters(clusters, cluster1, cluster2)
    return (clusters)


# -----------------------------------------------------------------------
# ----------------------Syntactic Clustering Section ----------------------------

def mix_SP_CR_similarity(CR_dist_matrix, SP_dist_matrix):
    N = CR_dist_matrix.shape[0]
    dims = (N, N)
    mixed_dist_matrix = np.ones(dims, dtype=np.float)

    CR_sim_matrix = 1 - CR_dist_matrix
    SP_sim_matrix = 1 - SP_dist_matrix

    for row in range(N):
        for col in range(row + 1, N):
            if max(CR_sim_matrix[row, col], SP_sim_matrix[row, col]) > 0.7:
                mixed_dist_matrix[row, col] = 1 - max(CR_sim_matrix[row, col], SP_sim_matrix[row, col])
            else:
                mixed_dist_matrix[row, col] = 1 - ((CR_sim_matrix[row, col] + SP_sim_matrix[row, col]) / 2)
    return (mixed_dist_matrix)


def is_same_verb_O_S(vector1_name, vector2_name):
    same_verb = False

    # vec1_colon=vector1_name.index(':')
    # vec2_colon=vector2_name.index(':')
    # vec1_colon=vector1_name.index('-')
    # vec2_colon=vector2_name.index('-')
    vec1_colon = vector1_name.index(':')
    vec2_colon = vector2_name.index(':')

    if vector1_name[0:(vec1_colon - 1)] == vector2_name[0:(vec2_colon - 1)]:
        if (vector1_name[-1] == 'o' and vector2_name[-1] == 's') or (
                vector1_name[-1] == 's' and vector2_name[-1] == 'o'):
            same_verb = True

    return (same_verb)


# def refine_dist_matrix(dist_matrix,vectors_name):
def refine_dist_matrix(dist_matrix, vectors_name, CR_dist_matrix):
    N = CR_dist_matrix.shape[0]
    for row in range(N):
        for col in range(row + 1, N):
            if is_same_verb_O_S(vectors_name[row], vectors_name[col]):
                # mixed_dist_matrix[row,col]=100000
                dist_matrix[row, col] = 100000
    # return(mixed_dist_matrix)
    return (dist_matrix)


# *****************************************************************************
# *****************************************************************************

from collections import Counter
import numpy as np
import collections


def insert_to_dict(key, value, Dict):
    if not key in Dict:
        Dict[key] = [value]

    else:
        Dict[key].append(value)


def decompose_SP(sp_dict):
    SP_NER = collections.OrderedDict()
    SP_SYN_FNCT = collections.OrderedDict()

    for key in sp_dict.keys():
        elements = list(sp_dict[key].elements())

        for idx in range(len(elements)):
            synt_fnct = elements[idx][0]
            NER = elements[idx][1]
            insert_to_dict(key, synt_fnct, SP_SYN_FNCT)
            insert_to_dict(key, NER, SP_NER)

    return (SP_SYN_FNCT, SP_NER)


def find_unique_values(Dict):
    all_values = []
    [all_values.extend(value) for value in Dict.values()]
    unique_values = np.unique(all_values)

    return (unique_values)


def find_key_dominant_NER(Dict):
    frequent_NER = collections.OrderedDict()
    for key in Dict:
        frequent_NER[key] = Counter(Dict[key]).most_common(1)[0][0]

    return (frequent_NER)


def flatten_dict(Dict):
    values = []
    for key in Dict.keys():
        values.extend([key] * Dict[key])
    return (values)


def convery_to_flat_values(Dict):
    flat_values_dict = collections.OrderedDict()

    for key in Dict.keys():
        value = Dict[key]
        flat_values_dict[key] = flatten_dict(value)

    return (flat_values_dict)


def generate_vectors_matrix(Dict):
    vectors_name = []
    unique_values = find_unique_values(Dict)
    matrix = np.zeros((len(Dict.keys()), len(unique_values)))

    for row in range(len(Dict.keys())):
        vectors_name.append(list((Dict.keys()))[row])
        for col in range(len(unique_values)):
            matrix[row][col] = Dict[list((Dict.keys()))[row]].count(unique_values[col])

    return (vectors_name, matrix)


def remove_extra_key(Dict, extra_keys):
    for key in extra_keys:
        del Dict[key]
    return (Dict)


def find_Same_NER_Index(SP_Dominant_NER, Vectors_Name):
    same_NER_Idx = dict()

    for idx in range(len(Vectors_Name)):
        insert_to_dict(SP_Dominant_NER[Vectors_Name[idx]], idx, same_NER_Idx)

    return (same_NER_Idx)


def generate_same_order_keys(Dict1, Dict2):
    newDict1 = dict()
    newDict2 = dict()

    for key in Dict1.keys():
        newDict1[key] = Dict1[key]
        newDict2[key] = Dict2[key]

    return (newDict1, newDict2)


def set_Member_Names(final_clusters, vectors_name):
    cluster_members_name = dict()
    for key in final_clusters:
        cluster_members_name[key] = [vectors_name[idx] for idx in final_clusters[key]]
    return (cluster_members_name)


# ----------------Run-------
# --Example:


SP_Dict = dict()

SP_Dict['v1-o'] = Counter({('o1', 'OTHER'): 1, ('o2', 'OTHER'): 2})
SP_Dict['v9-o'] = Counter({('s1', 'OTHER'): 2, ('s2', 'OTHER'): 4})

SP_Dict['v2-o'] = Counter({('o3', 'OTHER'): 1, ('o2', 'OTHER'): 1})
SP_Dict['v3-s'] = Counter({('s1', 'Person'): 2, ('s2', 'Person'): 1, ('s5', 'Location'): 1})
SP_Dict['v4-s'] = Counter({('s1', 'Person'): 1, ('s2', 'Person'): 4})
SP_Dict['v6-s'] = Counter({('s1', 'Person'): 2, ('s2', 'Person'): 1})
SP_Dict['v7-o'] = Counter({('o1', 'OTHER'): 1, ('o2', 'OTHER'): 2})
SP_Dict['v8-s'] = Counter({('s1', 'Person'): 1, ('s2', 'Person'): 4})

CR_Dict = dict()

CR_Dict['v1-o'] = {'v6:o': 2, 'v3:o': 2}
CR_Dict['v2-o'] = {'v3:o': 3, 'v5:o': 1}
CR_Dict['v3-s'] = {'v7:s': 1, 'v8:s': 2}
CR_Dict['v4-s'] = {'v8:s': 3, 'v7:s': 1}
CR_Dict['v5-s'] = {'v2:s': 3, 'v3:s': 1}
CR_Dict['v7-o'] = {'v6:o': 2, 'v3:o': 2}
CR_Dict['v8-s'] = {'v8:s': 3, 'v7:s': 1}
CR_Dict['v9-o'] = {'v8:s': 4, 'v3:o': 4}


def syntactic_clustering(CR_Dict, SP_Dict):
    CR_Keys = CR_Dict.keys()
    SP_Keys = SP_Dict.keys()
    Common_Keys = set(CR_Keys).intersection(set(SP_Keys))

    CR_Extra_Keys = set(CR_Keys).difference(Common_Keys)
    SP_Extra_Keys = set(SP_Keys).difference(Common_Keys)

    CR_Dict = remove_extra_key(CR_Dict, CR_Extra_Keys)
    SP_Dict = remove_extra_key(SP_Dict, SP_Extra_Keys)

    two_dicts = decompose_SP(SP_Dict)
    SP_SYN_FNCT = two_dicts[0]

    Flat_Value_Dict = convery_to_flat_values(CR_Dict)
    Flat_Value_Dict, SP_Dict = generate_same_order_keys(Flat_Value_Dict, SP_SYN_FNCT)

    CR_Vectors_Name, CR_Vectors = generate_vectors_matrix(Flat_Value_Dict)
    SP_Vectors_Name, SP_Vectors = generate_vectors_matrix(SP_Dict)

    SP_NER = two_dicts[1]
    SP_Dominant_NER = find_key_dominant_NER(SP_NER)
    NER_Vectors_Index = find_Same_NER_Index(SP_Dominant_NER, SP_Vectors_Name)

    NER_Clusters = dict()
    for NER in NER_Vectors_Index.keys():
        NER_SP_Vectors = SP_Vectors[NER_Vectors_Index[NER], :]
        NER_CR_Vectors = CR_Vectors[NER_Vectors_Index[NER],]
        vectors_name = [SP_Vectors_Name[idx] for idx in NER_Vectors_Index[NER]]

        CR_dist_matrix = cosine_distances(NER_CR_Vectors)
        SP_dist_matrix = cosine_distances(NER_SP_Vectors)
        mixed_dist_matrix = mix_SP_CR_similarity(CR_dist_matrix, SP_dist_matrix)

        # dist_matrix=refine_dist_matrix(mixed_dist_matrix ,vectors_name )
        dist_matrix = refine_dist_matrix(mixed_dist_matrix, vectors_name, CR_dist_matrix)
        # final_clusters=run_clustering(NER_CR_Vectors , 1,"sparse_scoring","minimum_similarity_score",0.5)
        final_clusters = run_clustering(NER_CR_Vectors, 1, "sparse_scoring", "minimum_similarity_score", 0.5,
                                        dist_matrix)
        # final_clusters=run_clustering(NER_CR_Vectors , 2,"simple","maximum_clusters_number",0)
        clusters_with_members_names = set_Member_Names(final_clusters, vectors_name)
        NER_Clusters[NER] = clusters_with_members_names

    return (NER_Clusters)









