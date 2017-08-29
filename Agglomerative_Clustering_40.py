
import numpy as np
from collections import Counter
import scipy.cluster.hierarchy as sch
import distance_matrix_calculation
import conll_full_parser
import sys

def main():
    if len(sys.argv) > 1 :
        address = sys.argv[1]
    else:
        address = None

    (word_sent_dict, cntr) = conll_full_parser.parse_full_conll("dev-muc3-0001-0100.conll", "dict")
    ola = distance_matrix_calculation.Distance_Calc(word_sent_dict, cntr)
    real_distance = ola.calculate_distance()
    clustering(real_distance)

def clustering(distance_matrix):
    N = distance_matrix.shape[0]  # vector number

    # distance_matrix = cosine_distances(vectors)  # distance matrix calcualtion based on cosine similarity


    dist = distance_matrix[np.triu_indices(N, 1)]


    clust_tree = sch.linkage(dist, method='average')

    n_clusters = N - 40
    max_count = 0
    while max_count < 40:
        n_clusters -= 1
        y = sch.fcluster(clust_tree, n_clusters, 'maxclust')  # 100
        for i in range(1, len(Counter(y) ) +1):
            max_count = max(max_count, Counter(y)[i])



    clusters_labels_count = Counter(y)  # final clusters labels with their sizes (having at most 40 members)


    for i in range(n_clusters):
        cluster1_vectors_index = np.where(y == i+ 1)
        print(cluster1_vectors_index[0])
        '''
        
        for j in (cluster1_vectors_index[0]):
            print(vectors[j])
            print(vectors[cluster1_vectors_index][j])
        '''


if __name__ == "__main__":
    main()











