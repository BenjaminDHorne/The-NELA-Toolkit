from sklearn import svm
import numpy as np
import copy
from sklearn.model_selection import cross_val_score
from sklearn import preprocessing
import pickle
from operator import itemgetter

def learn_params_svm(X, y):
    X = copy.copy(X)
    y = copy.copy(y)
    scr_prms = []
    Cs = list(np.arange(0.05, 1, 0.05))
    #X_normalized = preprocessing.normalize(X)
    #X_scaled = preprocessing.scale(X_normalized)
    for C in Cs:
        clf = svm.LinearSVC(C=C)
        clf.fit(X, y)
        scores = cross_val_score(clf, X, y, cv=10)
        avg_cv = float(sum(scores))/len(scores)
        scr_prms.append((avg_cv, C))
        
    best_C = max(scr_prms,key=itemgetter(0))[1]
    return best_C


if __name__ == "__main__":
    X = []
    y = []
    with open('./fake_features_fortraining.csv') as f:
        f.readline()
        for i in f:
            i = i.strip().split(',')
            x = tuple(i[2:])
            x = tuple([float(e) for e in x])
            X.append(x)
            if i[1] == "Real":
                y.append(1.0)
            elif i[1] == "Fake":
                y.append(0.0)
            elif i[1] == "Satire":
                y.append(2.0)
    best_C=learn_params_svm(X, y)
    #X_normalized = preprocessing.normalize(X)
    #X_scaled = preprocessing.scale(X_normalized)
    clf = svm.LinearSVC(C=best_C, multi_class='ovr')
    clf.fit(X, y)

    # save the model to disk
    filename = 'FAKE_FILTER_MODEL.sav'
    pickle.dump(clf, open(filename, 'wb'))
    
