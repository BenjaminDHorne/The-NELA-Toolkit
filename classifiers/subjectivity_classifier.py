import warnings
warnings.filterwarnings("ignore")

import pickle
import os
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

DIRNAME = os.path.dirname(__file__)

def subjectivity(title, text):
    print "Computing subjectivity"
    try:
        loaded_model = pickle.load(open(os.path.join(DIRNAME, 'resources', 'NB_Subj_Model.sav'), 'rb'))
        count_vect = pickle.load(open(os.path.join(DIRNAME, 'resources', 'count_vect.sav'), 'rb'))
        tfidf_transformer = pickle.load(open(os.path.join(DIRNAME, 'resources', 'tfidf_transformer.sav'), 'rb'))
    except:
        return -1., -1. 
    
    X_new_counts = count_vect.transform([title])
    X_new_tfidf = tfidf_transformer.transform(X_new_counts)
    result = loaded_model.predict_proba(X_new_tfidf)
    prob_obj_title = result[0][0]

    X_new_counts = count_vect.transform([text])
    X_new_tfidf = tfidf_transformer.transform(X_new_counts)
    result = loaded_model.predict_proba(X_new_tfidf)
    prob_obj = result[0][0]

    return prob_obj_title, prob_obj
