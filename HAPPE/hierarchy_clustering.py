## clustering using pheat file
## usage: python __file__ in.newpheat out.newick out.cluster

# in.pheat format
# name ref alt  sample1 sample2 sample3 ...
# chr1A_131 A G 0 9 -9 ...

from logging import error
import pandas as pd
import numpy as np
from scipy.cluster import hierarchy
import sys
import sklearn as sk
from sklearn import cluster
import dynamicTreeCut 

sys.setrecursionlimit(100000)

def getNewick(node, newick, parentdist, leaf_names):
    if node.is_leaf():
        return "%s:%f%s" % (leaf_names[node.id], parentdist - node.dist, newick)
    else:
        if len(newick) > 0:
            newick = "):%f%s" % (parentdist - node.dist, newick)
        else:
            newick = ");"
        newick = getNewick(node.get_left(), newick, node.dist, leaf_names)
        newick = getNewick(node.get_right(), ",%s" % (newick), node.dist, leaf_names)
        newick = "(%s" % (newick)
        return newick

def get_linkage_matrix(model):
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count


    linkage_matrix = np.column_stack([model.children_, model.distances_, counts]).astype(float)
    return linkage_matrix

if __name__ == "__main__":
    # read table file
    inf = open(sys.argv[1],"r")
    header = inf.readline().strip().split()
    sample_gt_d = {}
    for sample in header[3:]:
        sample_gt_d[sample]  = []
    n_site = 0
    for line in inf:
        n_site +=1
        ls = line.strip().split()
        for index,value in enumerate( ls[3:] ):
            '''
            -9: 0/0
            0 :  0/1
            9 :  1/1
            NA: missing
            '''
            if value == "-9":
                value = -1
            if value == "0":
                value = 0.9
            if value == "9":
                value = 1
            if value == "NA":
                value = 0
            sample_gt_d[header[ index + 3] ] .append(value)

    inf.close()
    # print(sklearn.__version__)
    pd_df = pd.DataFrame(sample_gt_d)
    col_name = pd_df.columns.tolist()
    pd_df = pd_df.T

    hclustering = cluster.AgglomerativeClustering(distance_threshold=0, n_clusters=None).fit(pd_df)
    # print(len(clustering.labels_))
    Z = get_linkage_matrix(hclustering)
    tree = hierarchy.to_tree(Z, rd=False)
    newick_str = getNewick(tree, "", tree.dist, col_name )

    ouf = open(sys.argv[2],"w")
    ouf.write(newick_str)
    ouf.close()


    # pd_df.to_csv("zz.test.txt",sep="\t",index=True)
    #Langfelder P, Zhang B, Horvath S. Defining clusters from a hierarchical cluster tree: the Dynamic Tree Cut package for R[J]. Bioinformatics, 2008, 24(5): 719-720.
    #dymic cut tree
    dist_matrix = sk.metrics.pairwise.pairwise_distances(pd_df, metric='euclidean')
    clusters = dynamicTreeCut.cutreeHybrid(Z, dist_matrix,minClusterSize=1,deepSplit=4)
    
    # print(clusters["labels"])
    print("cluster min and max:",min(clusters["labels"]),max(clusters["labels"]),file=sys.stderr)

    outf = open(sys.argv[3],"w")
    outf.write("sample\tcluster\n")
    for index, sample in enumerate(col_name):
        outf.write("%s\t%d\n" % (sample,clusters["labels"][index]))
    outf.close()



    