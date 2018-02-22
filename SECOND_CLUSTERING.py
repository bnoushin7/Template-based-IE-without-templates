
from sklearn.metrics.pairwise import cosine_distances

import numpy as np


def initialize(vectors):
    clusters = dict()
    clusters = {i: [i] for i in range(len(vectors))}
    return (clusters)


def r(clusters, cluster1, cluster2):
    non_zero_count = 0

    similarity_matrix = 1 - dist_matrix
    for clus1_member in clusters[cluster1]:
        for clus2_member in clusters[cluster2]:
            if similarity_matrix[clus1_member, clus2_member] > 0:
                non_zero_count += 1

    return (non_zero_count / (len(clusters[cluster1]) * len(clusters[cluster2])))


def score(clusters, cluster1, cluster2):
    similarity_matrix = 1 - dist_matrix
    similarity_sum = 0

    for clus1_member in clusters[cluster1]:
        for clus2_member in clusters[cluster2]:
            similarity_sum += similarity_matrix[clus1_member, clus2_member]

    return (similarity_sum * r(clusters, cluster1, cluster2))


def clusters_distance(clusters, cluster1, cluster2, dist_type):
    distance = 0

    if dist_type == "simple":
        for clus1_member in clusters[cluster1]:
            for clus2_member in clusters[cluster2]:
                distance += dist_matrix[clus1_member, clus2_member]

        distance /= len(clusters[cluster1]) * len(clusters[cluster2])

    if dist_type == "sparse_scoring":  # as described in section 4.3.2 of the paper.
        distance = 1 - score(clusters, cluster1, cluster2)

    return (distance)


def find_closest_clusters(clusters, dist_type):
    closest = dict()
    min_distance = np.inf

    for clus1 in range(len(clusters)):
        for clus2 in range(clus1 + 1, len(clusters)):
            distance = clusters_distance(clusters, clus1, clus2, dist_type)

            if distance < min_distance:
                min_distance = distance
                merge_candid1 = clus1
                merge_candid2 = clus2

    closest[1] = merge_candid1
    closest[2] = merge_candid2
    return (closest)


def stop_condition(clusters, stop_type, dist_type, clusters_number, minimum_score):
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
        next_closest_clusters = find_closest_clusters(clusters, dist_type)
        if score(clusters, next_closest_clusters[1], next_closest_clusters[2]) < minimum_score:
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


def run_clustering(vectors, clusters_number, dist_type, stop_type, minimum_score):
    clusters = initialize(vectors)

    while not stop_condition(clusters, stop_type, dist_type, clusters_number, minimum_score):
        closest_pair = find_closest_clusters(clusters, dist_type)
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

    vec1_colon = vector1_name.index(':')
    vec2_colon = vector2_name.index(':')

    if vector1_name[0:(vec1_colon - 1)] == vector2_name[0:(vec2_colon - 1)]:
        if (vector1_name[-1] == 'o' and vector2_name[-1] == 's') or (
                vector1_name[-1] == 's' and vector2_name[-1] == 'o'):
            same_verb = True

    return (same_verb)


def refine_dist_matrix(dist_matrix, vectors_name):
    N = CR_dist_matrix.shape[0]
    for row in range(N):
        for col in range(row + 1, N):
            if is_same_verb_O_S(vectors_name[row], vectors_name[col]):
                mixed_dist_matrix[row, col] = 100000
    return (mixed_dist_matrix)


# --------------------------------------Clustering Test--------------
# --------------Example1:

vectors = np.random.normal([1, 1], size=[200, 2])
dist_matrix = cosine_distances(vectors)
final_clusters = run_clustering(vectors, 1, "simple", "maximum _cluster_members", 0)
print(final_clusters)
'''

# --------------Example 2: 
vectors = np.random.normal([1, 1], size=[200, 2])
dist_matrix = cosine_distances(vectors)
final_clusters = run_clustering(vectors, 10, "simple", "maximum_clusters_number", 0)

# --------------Example 3: 

vectors = [np.array(f) for f in [[0, 1], [0, 2], [0, 5], [11, 0], [30, 0], [34, 0], [35, 0]]]
dist_matrix = cosine_distances(vectors)
final_clusters = run_clustering(vectors, 1, "sparse_scoring", "minimum_similarity_score", 1)

# ----Example for Syntactic clustering------------
# input:  CR_vectors, SP_vectors,vectors_name

CR_vectors = [np.array(f) for f in [[0, 1], [0, 2], [0, 5], [11, 0], [30, 0], [34, 0], [35, 0]]]
SP_vectors = [np.array(f) for f in [[0, 1], [0, 2], [0, 5], [11, 10], [30, 0], [34, 0], [35, 0]]]
vectors_name = ["go_off:s", "plant:o", "go_off:o", "set_off:o", "kidnap:s", "rape:s", "injured:o"]

CR_dist_matrix = cosine_distances(CR_vectors)
SP_dist_matrix = cosine_distances(SP_vectors)

mixed_dist_matrix = mix_SP_CR_similarity(CR_dist_matrix, SP_dist_matrix)

dist_matrix = refine_dist_matrix(mixed_dist_matrix, vectors_name)

final_clusters = run_clustering(CR_vectors, 1, "sparse_scoring", "minimum_similarity_score", 1)
'''







