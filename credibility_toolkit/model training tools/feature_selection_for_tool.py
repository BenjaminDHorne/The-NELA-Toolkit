# feature select for each community model
#output list as json
#store json files with tool, load in to do quikc feature selection

from sklearn.ensemble import ExtraTreesClassifier
from sklearn.datasets import load_iris
from sklearn.feature_selection import SelectFromModel
import json
import util
from collections import defaultdict
import numpy as np
from sklearn import preprocessing


def read(featuresfile):
    data = util.read_info(featuresfile, ',')
    features = data[0].keys()
    exclude_features = ['pid', 'numcmts']
    features = list(set(features).difference(set(exclude_features)))
    for datarow in data:
        for ft in features:
            datarow[ft] = float(datarow[ft])
    pdata= defaultdict(list)
    for datarow in data:
        pdata[datarow['pid']] = [datarow[d] for d in datarow if d in features] #double check this
    return features, pdata

def splitdata8020(features, posts):
    permuted = np.random.permutation(range(len(posts.keys())))
    pids = np.array(posts.keys())
    trainids = permuted
    trainpids = pids[trainids]
    trainrows = [posts[pid] for pid in trainpids]
    train = np.double(np.array(trainrows))
    return train, trainpids

def XYsplit(Z, features, Xfeatures, Yfeatures, name):
    m = len(Z)
    X = np.zeros((m, len(Xfeatures)))
    Y = np.zeros((m, len(Yfeatures)))
    j = 0
    for ft in features:
        if ft in Xfeatures:
            i = Xfeatures.index(ft)
            X[:, i] = Z[:, j]
        elif ft in Yfeatures:
            i = Yfeatures.index(ft)
            Y[:, i] = Z[:, j]
        j = j + 1
    (m, n) = np.shape(X)
    Xscaled = preprocessing.scale(X)
    Xnormed = preprocessing.normalize(X)
    return X, Xscaled, Xnormed, Y, (m, n)

#main
plot = False
output = False
print_feats = False
select_for_training = True

#load features
sub = "conspiracy"
ftfile = "__%s_features_training_filt.csv" % (sub)
output_file = "features_selected_%s.csv" % (sub)
features, posts = read(ftfile)
Ztrain, trainpids = splitdata8020(features, posts)
Yfeatures = ['score']
Xfeatures = [ft for ft in features if ft not in Yfeatures]
X, Xscaled, Xtrainnormed, Y, (mtrain, ntrain) = XYsplit(Ztrain, features, Xfeatures, Yfeatures, 'train')
Y = np.array([int(y) for y in Y])

clf = ExtraTreesClassifier(n_estimators=250, random_state=0)
clf = clf.fit(Xscaled, Y)
importances = clf.feature_importances_
std = np.std([tree.feature_importances_ for tree in clf.estimators_],
             axis=0)

model = SelectFromModel(clf, prefit=True)
X_new = model.transform(Xscaled)       

indices = np.argsort(importances)[::-1]

if print_feats:
    removed =  Xscaled.shape[1] - X_new.shape[1]
    removed_percent =(float(removed)/Xscaled.shape[1])*100
    kept = X_new.shape[1]
    print ("Removed %d Features out of %d Features (%0.2f Percent Reduction)" % (int(removed), int(Xscaled.shape[1]), float(removed_percent)))
    print ("Kept top %d Features" % (kept))
    print("Feature ranking:")
    for f in range(Xscaled.shape[1]):
        print("%d. feature %d, %s (%f)" % (f + 1, indices[f], Xfeatures[int(indices[f])], importances[indices[f]]))

feature_names_selected = []
for f in range(Xscaled.shape[1]):
    if importances[indices[f]] >= importances[indices[X_new.shape[1]]]:
        feature_names_selected.append(Xfeatures[int(indices[f])])

if output:
    #write out new feature set.
    with open(output_file, "w") as out:
        out.write(",".join(feature_names_selected)+"\n")

if select_for_training:
    feature_names_selected.append('pid')
    feature_names_selected.append('score')
    feature_names_selected.append('numcmts')
    featuresfile = "__%s_features_training_filt.csv" % (sub)
    outtrainfile = sub+"_features_selected_filt.csv"
    with open(featuresfile) as allfeats:
        feat_names = allfeats.readline().strip().split(",")
        feats_to_keep = [f for f in feat_names if f in feature_names_selected]
        ind_to_keep = [feat_names.index(fk) for fk in feats_to_keep]
        with open(outtrainfile, "a") as out:
                out.write(",".join(feats_to_keep)+"\n")
        for line in allfeats:
            line_to_keep = []
            line = line.strip().split(",")
            for i in xrange(len(line)):
                if i in ind_to_keep:
                    line_to_keep.append(line[i])
            with open(outtrainfile, "a") as out:
                out.write(",".join(line_to_keep)+"\n")

if plot:
    # Plot the feature importances of the forest
    plt.figure()
    plt.title("Feature importances")
    plt.bar(range(X.shape[1]), importances[indices],
           color="r", yerr=std[indices], align="center")
    plt.xticks(range(X.shape[1]), indices)
    plt.xlim([-1, X.shape[1]])
    plt.show()
