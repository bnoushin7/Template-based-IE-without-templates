'''
Created on 7/18/17
Sample code for  
@author: Noushin
'''
def agCluster(distances,m):
    dm = {}
    clusters = {i:[i] for i in range(len(distances))}
    clusters_map = {i:i for i in range(len(distances))}
    def check_clusters(m):
        for x in clusters:
            if len(clusters[x])<m: return False
        return True

    for i in range(len(distances)):
        for j in range(i+1,len(distances[i])):
            if distances[i][j] in dm:
                dm[distances[i][j]].append((i,j))
            else:
                dm[distances[i][j]] = [(i,j)]
    finished = False
    for distance in sorted(dm.iterkeys()):
        if finished: break
        for x,y in dm[distance]:
            if check_clusters(m) :
                finished = True
                break
            if clusters_map[x] != clusters_map[y]:
                q = clusters_map[y]
                for k in clusters[clusters_map[y]]:
                    clusters[clusters_map[x]].append(k)
                    clusters_map[k] = clusters_map[x]
                del clusters[q]

    return clusters

dists = [[0,1,6,7],
         [1,0,8,9],
         [6,8,0,2],
         [7,9,2,0]]

clusters = agCluster(dists,2)
for cl in clusters:
    print cl, " --- ", clusters[cl]