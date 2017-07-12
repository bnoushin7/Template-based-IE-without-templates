'''Created on 7/11/17
Code for doing agglomerative clustering, takes the distance (similarity) matrix as input and its output is list of lables
@author: Noushin
'''

'''

import matplotlib.pyplot as plt
'''
def agglomerative_clustering(distance_matrix):
    #import numpy as np
    from scipy.cluster import hierarchy
    import sklearn
    from sklearn.cluster import AgglomerativeClustering
    from sklearn.metrics import euclidean_distances
    import sklearn.metrics as sm

    Hclust = AgglomerativeClustering(n_clusters=5, affinity='precomputed', linkage='complete')
    y = Hclust.fit_predict(distance_matrix)
    print(y)

'''
    a = np.array([[0, 0], [1, 0], [0, 1], [1, 1], [0.5, 0], [0, 0.5],
                  [0.5, 0.5], [2, 2], [2, 3], [3, 2], [3, 3]])

    similarities = euclidean_distances(a)
    y = 0
'''




#agglomerative_clustering()