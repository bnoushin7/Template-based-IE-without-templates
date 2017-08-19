
from sklearn.metrics.pairwise import cosine_distances
import numpy as np
from collections import Counter
import scipy.cluster.hierarchy as sch

def Agglomerative_Clustering(distance_matrix):

    N = distance_matrix.shape[0]  # vector number

    dist = distance_matrix[np.triu_indices(N, 1)]
    clust_tree = sch.linkage(dist, method='average')

    n_clusters = N - 4
    max_count = 0
    while max_count < 4:
        n_clusters -= 1
        y = sch.fcluster(clust_tree, n_clusters, 'maxclust') #100
        print("len {}".format(len(Counter(y))))
        for i in range(1, len(Counter(y))+1):
            print("counter y is {}".format(Counter(y)[i]))
            max_count = max(max_count, Counter(y)[i])

    clusters_labels_count = Counter(y)  # final clusters labels with their sizes (having at most 40 members)

    for i in range(n_clusters):
        cluster1_vectors_index = np.where(y == i+1)
        print(cluster1_vectors_index[0])


vectors = np.random.normal([1, 0.5],
                           size=[10, 2])  # vectors of 1000  random two dimensional points from normal distribution

distance_matrix = cosine_distances(vectors)
Agglomerative_Clustering(distance_matrix)