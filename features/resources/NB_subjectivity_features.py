from nltk.corpus import subjectivity
from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob
import random
import os
import pickle


def build_NBclassifier():
    '''
    The Subjectivity Dataset contains 5000 subjective and 5000 objective processed sentences.
    gets 91% accuracy on 1000 sentence test set.
    '''
    random.seed(1)
    subjective_sents = subjectivity.sents(categories='subj')
    objective_sents = subjectivity.sents(categories='obj')

    sents = []
    for sent in subjective_sents:
        sents.append((sent, 'subj'))
    for sent in objective_sents:
        sents.append((sent, 'obj'))

    random.shuffle(sents)
    train = sents
    cl = NaiveBayesClassifier(train)
    # save the model to disk
    filename = 'NB_Subj_Model.sav'
    pickle.dump(cl, open(filename, 'wb'))
    

#main

cl = build_NBclassifier()

##with open(outfile, "a") as out:
##    out.write("pid,NB_SubCat,NB_pobj,NB_psubj\n")
##for fn in os.listdir(files):
##    pid = fn.split(".")[0]
##    print "processing", pid
##    with open(files+fn) as article:
##        lines = [fix(line.strip()) for line in article]
##        text = " ".join(lines)
##        blob = TextBlob(text, classifier=cl)
##        prob_dist = cl.prob_classify(text)
##        if blob.classify() == 'obj':
##            sub_cat = 1
##        else:
##            sub_cat = 0
##        with open(outfile, "a") as out:
##            out.write(",".join((pid, str(sub_cat),str(prob_dist.prob("obj")),str(prob_dist.prob("subj"))))+"\n")
##
##
