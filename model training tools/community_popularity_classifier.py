import pickle
from sklearn import preprocessing
import csv
import numpy as np
import scipy.stats as ss
from sklearn import preprocessing, linear_model, metrics, feature_selection, kernel_ridge
import util
from collections import defaultdict
from sklearn.model_selection import cross_val_score

def read(featuresfile, fp1, fp2):
    data = util.read_info(featuresfile, ',')
    features = data[0].keys()
    exclude_features = ['pid', 'numcmts']
    features = list(set(features).difference(set(exclude_features)))
    for datarow in data:
        for ft in features:
            datarow[ft] = float(datarow[ft])
    scores = [int(datarow['score']) for datarow in data]
    (s1, s2) = (ss.scoreatpercentile(scores, fp1), ss.scoreatpercentile(scores, fp2))
    data = [datarow for datarow in data if int(datarow['score']) >= s1 and int(datarow['score']) <= s2]
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

#ridge regression
def learn(filename, features, posts, Ztrain, trainpids, fp1, fp2):
    Yfeatures = ['score']
    Xfeatures = [ft for ft in features if ft not in Yfeatures]
    Xtrain, Xtrainscaled, Xtrainnormed, Ytrain, (mtrain, ntrain) = XYsplit(Ztrain, features, Xfeatures, Yfeatures, 'train')
    
    clf = linear_model.RidgeCV(alphas=[0.1, 0.5, 1.0, 10.0], cv=10, scoring='neg_mean_squared_error')
    clf = clf.fit(Xtrain, Ytrain)

    #scores = cross_val_score(clf, Xtrain, Ytrain, cv=10)
    #print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
    
    # save the model to disk
    pickle.dump(clf, open(filename, 'wb'))

def testbed(fn, testfile, score=True):
    with open(fn) as data:
        data.readline()
        if score:
            y = [float(line.strip().split(",")[1]) for line in data]
        else:
            y = [float(line.strip().split(",")[2]) for line in data]
    one = str(np.percentile(y, 90))
    two = str(np.percentile(y, 80))
    three = str(np.percentile(y, 50))
    four = str(np.percentile(y, 10))
    print max(y), one, two, three, four, min(y)
    test = [yy for yy in y if yy > float(two)]
    print len(test), float(len(test))/len(y)
    with open(testfile, "w") as out:
        out.write(",".join((one,two,three,four))+"\n")
    
if __name__ == "__main__":
    sub = "worldpolitics"
    ftfile = sub+"_features_selected_filt.csv"
    testbed(ftfile, sub+"_testbed_cmts.txt", False)
##    features, posts = read(ftfile, 0, 100)
##    Ztrain, trainpids = splitdata8020(features, posts)
##    learn("POPULARITY_MODEL_"+sub.upper()+".sav", features, posts, Ztrain, trainpids, 0, 100)
    
