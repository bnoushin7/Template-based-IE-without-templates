'''Created on 7/11/17
Code for doing agglomerative clustering, takes the distance (similarity) matrix as input and its output is list of lables
@author: Noushin
'''

'''

'''

#def agglomerative_clustering(distance_matrix):
def agglomerative_clustering():
    import numpy as np
    from scipy.cluster import hierarchy
    import sklearn
    from sklearn.cluster import AgglomerativeClustering
    from sklearn.metrics import euclidean_distances
    import sklearn.metrics as sm



    a = np.array([[0, 0], [1, 0], [0, 1], [1, 1], [0.5, 0], [0, 0.5],
                  [0.5, 0.5], [2, 2], [2, 3], [3, 2], [3, 3]])

   # similarities = euclidean_distances(a)
   # distance_matrix = euclidean_distances(a)

    distance_matrix = [[0, 1, 2, 3],
     [1, 0, 4, 5],
     [2, 4, 0, 7],
     [3, 5, 7, 0]]

    Hclust = AgglomerativeClustering(n_clusters=2, affinity='precomputed', linkage='complete')
    y = Hclust.fit_predict(distance_matrix)
    #z = y.children_
    print(y)


agglomerative_clustering()