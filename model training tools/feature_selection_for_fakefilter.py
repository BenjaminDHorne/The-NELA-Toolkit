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
import logging


def read(featuresfile, yindex):
    Ys = []
    Xs = []
    with open(featuresfile) as featuredata:
        header = featuredata.readline().split(",")
        Xfeatures = header[yindex+1:]
        Yfeature = header[yindex]
        for line in featuredata:
            line = line.strip().split(",")
            Ys.append(float(line[yindex]))
            Xs.append(np.array([float(x) for x in line[3:]]))
    Ys = np.array(Ys)
    Xs = np.array(Xs)
    return Xs, Ys, Xfeatures, Yfeature

#main
plot = False
output = False
print_feats = True
select_for_training = True

FORMAT = "%(asctime)s %(levelname)s %(module)s %(lineno)d %(funcName)s:: %(message)s"
logging.basicConfig(filename="featureselection.log", filemode='a', level=logging.DEBUG, format=FORMAT)

#load features
ftfile = "_newsVSconspiracy_features.csv"
output_file = "_newsVSconspiracy_features_selected.csv"
Xs, Ys, Xfeatures, Yfeature = read(ftfile, 1)

clf = ExtraTreesClassifier(n_estimators=300, random_state=0)
clf = clf.fit(Xs, Ys)
importances = clf.feature_importances_
std = np.std([tree.feature_importances_ for tree in clf.estimators_],
             axis=0)

model = SelectFromModel(clf, prefit=True)
X_new = model.transform(Xs)

indices = np.argsort(importances)[::-1]

print Xs.shape[1], X_new.shape[1]

if print_feats:
    removed =  Xs.shape[1] - X_new.shape[1]
    removed_percent =(float(removed)/Xs.shape[1])*100
    kept = X_new.shape[1]
    print ("Removed %d Features out of %d Features (%0.2f Percent Reduction)" % (int(removed), int(Xs.shape[1]), float(removed_percent)))
    print ("Kept top %d Features" % (kept))
    print("Feature ranking:")
    for f in range(Xs.shape[1]):
        print("%d. feature %d, %s (%f)" % (f + 1, indices[f], Xfeatures[int(indices[f])], importances[indices[f]]))

feature_names_selected = []
for f in range(Xs.shape[1]):
    if importances[indices[f]] >= importances[indices[X_new.shape[1]]]:
        feature_names_selected.append(Xfeatures[int(indices[f])])

if output:
    #write out new feature set.
    with open(output_file, "w") as out:
        out.write(",".join(feature_names_selected)+"\n")

if select_for_training:
    feature_names_selected.append('pid')
    feature_names_selected.append('sub')
    featuresfile = "_newsVSconspiracy_features.csv"
    outtrainfile = "_newsVSconspiracy_features_selected.csv"
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
