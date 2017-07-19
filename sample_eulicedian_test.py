import numpy as np
#from scipy.cluster import hierarchy
#import matplotlib.pyplot as plt
#import sklearn
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import euclidean_distances
#import sklearn.metrics as sm

a = np.array([[0,   0  ], [1,   0  ], [0,   1  ], [1,   1  ], [0.5, 0  ], [0,   0.5],
              [0.5, 0.5], [2,   2  ], [2,   3  ], [3,   2  ],[3,   3  ]])

similarities = euclidean_distances(a)
y=0

Hclust = AgglomerativeClustering(n_clusters = 5, affinity = 'precomputed', linkage = 'complete')
y = Hclust.fit_predict(similarities)
print(y)

