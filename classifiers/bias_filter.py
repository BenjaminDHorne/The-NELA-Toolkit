import warnings
warnings.filterwarnings("ignore")

from sklearn import preprocessing
import pickle
import os
import numpy as np

DIRNAME = os.path.dirname(__file__)

def bias_fitler(featurepath):
    print "Predicting bias"
    with open(os.path.join(featurepath, "bias_features.csv")) as data:
        data.readline()
        x_test = data.readline().strip().split(",")

    X_test = []
    x_test = tuple([float(x) for x in x_test])
    x_test = np.array(x_test).reshape(1, -1)
    #X_test.append(x_test)
    #x_test = preprocessing.normalize(x_test)
    #x_test = preprocessing.scale(x_test)

    # load the model from disk
    loaded_model = pickle.load(open(os.path.join(DIRNAME, 'resources', 'BIAS_FILTER_MODEL.sav'), 'rb'))
    #print "PREDICT", loaded_model.predict(x_test)
    styles = ["Biased Writing Style", "UnBiased Writing Style"]
    result = loaded_model.predict_proba(x_test)[0]
    #print loaded_model.classes_

    # combine results with writing styles list
    result = [(styles[i], x) for i,x in enumerate(result)]

    # sort the results such that the first item in the list is the most likely
    # possibility
    #result = sorted(result, key=lambda x: x[1], reverse=True)

    return result
