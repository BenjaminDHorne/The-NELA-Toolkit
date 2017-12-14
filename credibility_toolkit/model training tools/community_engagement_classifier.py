import pickle
from sklearn import preprocessing
import csv
import numpy as np
import scipy.stats as ss
from sklearn import preprocessing, linear_model, metrics, feature_selection, kernel_ridge
import util
from collections import defaultdict
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

def read(featuresfile, targetfeature):
    Ys = []
    Xs = []
    if targetfeature == "numcmts":
        yindex = 2
    elif targetfeature == "score":
        yindex = 1
    with open(featuresfile) as featuredata:
        header = featuredata.readline()
        for line in featuredata:
            line = line.strip().split(",")
            Ys.append(float(line[yindex]))
            Xs.append(np.array([float(x) for x in line[3:]]))
    Ys = np.array(Ys)
    Xs = np.array(Xs)
    return Xs, Ys


def learn(filename, Xs, Ys, scale=False, save=True, test=False, testfile=None):
    if scale:
        Xs = preprocessing.scale(Xs)

    #clf = linear_model.RidgeCV(alphas=[0.1, 0.5, 1.0, 10.0], cv=10, scoring='neg_mean_squared_error')
    #clf = kernel_ridge.KernelRidge(kernel='rbf')
    clf = linear_model.LassoCV()
    print Ys
    clf = clf.fit(Xs, Ys)

    #scores = cross_val_score(clf, Xtrain, Ytrain, cv=10)
    #print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
    
    # save the model to disk
    if save:
        pickle.dump(clf, open(filename, 'wb'))
    if test:
        test_xs = []
        true_ys = []
        with open(testfile) as testdata:
            testdata.readline() #remove header
            for line in testdata:
                line = line.strip().split(",")
                true_ys.append(float(line[1]))
                test_xs.append([float(l) for l in line[3:]])
        test_xs = np.array(test_xs)
        pred_ys = []
        for xvec in test_xs:
            pred_ys.append(clf.predict(xvec)[0])

        print true_ys
        print pred_ys
        #print('Coefficients: \n', clf.coef_)
        # The mean squared error
        print("Mean squared error: %.2f"
              % mean_squared_error(true_ys, pred_ys))
        # Explained variance score: 1 is perfect prediction
        print('Variance score: %.2f' % r2_score(true_ys, pred_ys))

def testbed(fn, testfile, score=True):
    with open(fn) as data:
        data.readline()
        if score:
            y = [float(line.strip().split(",")[1]) for line in data]
        else:
            y = [float(line.strip().split(",")[2]) for line in data]
    one = str(np.percentile(y, 75))
    two = str(np.percentile(y, 80))
    three = str(np.percentile(y, 50))
    four = str(np.percentile(y, 5))
    print max(y), one, two, three, four, min(y)
    test = [yy for yy in y if yy > float(two)]
    print len(test), float(len(test))/len(y)
    with open(testfile, "w") as out:
        out.write(",".join((one,two,three,four))+"\n")

if __name__ == "__main__":
    sub = "Republican"
    ftfile = "_"+sub+"_features_selected_10272017_filt.csv" #"_"+sub+"_train.csv"
    testbed(ftfile, sub+"_testbed.txt", True)
    #Xs, Ys = read(ftfile, "score")
    #learn("POPULARITY_MODEL_"+sub.upper()+"2.sav", Xs, Ys, scale=True, save=True, test=False, testfile="./_news_test.csv")
    
