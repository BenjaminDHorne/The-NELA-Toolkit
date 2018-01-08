import warnings
warnings.filterwarnings("ignore")

from sklearn import preprocessing
import pickle
import os
import numpy as np

DIRNAME = os.path.dirname(__file__)

def community_fitler(featurepath):
    print "Predicting community interests"
    styles = ["Probability r/conspiracy interested", "Probability r/esist interested", "Probability r/new_right interested"]
    models_to_load = ["newsVSconsp", "newsVSesist", "newsVSnewright"]
    all_results = []
    for model in models_to_load:
        with open(os.path.join(featurepath, model+"_features.csv")) as data:
            data.readline()
            x_test = data.readline().strip().split(",")

        x_test = tuple([float(x) for x in x_test])
        x_test = np.array(x_test).reshape(1, -1)

        # load the model from disk
        loaded_model = pickle.load(open(os.path.join(DIRNAME, 'resources', model+'.sav'), 'rb'))

        result = loaded_model.predict_proba(x_test)[0][0]
        #print loaded_model.classes_
        all_results.append(result)

    # combine results with writing styles list
    all_results = [(styles[i], x) for i,x in enumerate(all_results)]

    # sort the results such that the first item in the list is the most likely possibility
    #result = sorted(result, key=lambda x: x[1], reverse=True)

    return all_results
