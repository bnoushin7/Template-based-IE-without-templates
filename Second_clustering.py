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


def clusters_distance(clusters, cluster1, cluster2):
    distance = 0

    for clus1_member in clusters[cluster1]:
        for clus2_member in clusters[cluster2]:
            distance += dist_matrix[clus1_member, clus2_member]

    distance /= len(clusters[cluster1]) * len(clusters[cluster2])
    distance = 1 - score(clusters, cluster1, cluster2)


    return(distance)


def find_closest_clusters(clusters):
    closest = dict()
    min_distance = np.inf

    for clus1 in range(len(clusters)):
        for clus2 in range(clus1 + 1, len(clusters)):
            distance = clusters_distance(clusters, clus1, clus2)

            if distance < min_distance:
                min_distance = distance
                merge_candid1 = clus1
                merge_candid2 = clus2

    closest[1] = merge_candid1
    closest[2] = merge_candid2
    return (closest)


def stop_condition(clusters, minimum_score):

    stop = False

    if (len(clusters) == 1):
        return (True)

    next_closest_clusters = find_closest_clusters(clusters)
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


def run_clustering(vectors, minimum_score):
    clusters = initialize(vectors)

    while not stop_condition(clusters, minimum_score):
        closest_pair = find_closest_clusters(clusters)
        cluster1 = closest_pair[1]
        cluster2 = closest_pair[2]

        clusters = merge_clusters(clusters, cluster1, cluster2)
    return (clusters)


vectors = [[0, 1], [0, 2], [0, 5], [11, 0], [30, 0], [34, 0], [35, 0]]
dist_matrix = cosine_distances(vectors)
final_clusters = run_clustering(vectors, 1)

print final_clusters