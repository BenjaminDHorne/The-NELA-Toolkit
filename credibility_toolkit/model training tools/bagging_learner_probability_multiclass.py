from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn import preprocessing
from sklearn.model_selection import cross_val_score
import logging
import pickle
import copy
import numpy as np
from operator import itemgetter

def predefined_feature_selection(Xs, ys, feat_labs, fs_type, title=True, body=True):
    if fs_type == "all":
        X_new = []
        for x in Xs:
            i=0
            x_new =[]
            while i < len(x):
                x_new.append(x[i])
                i+=1
            X_new.append(x_new)
        features_selected = feat_labs
        return X_new, features_selected

    features_to_select = []
    if title == False and body == True:
        if fs_type == 'ACL13':
            features_to_select = ["bias_count", "assertives_count", "factives_count", "hedges_count", "implicatives_count", "report_verbs_count", "positive_op_count", "negative_op_count", "wneg_count", "wpos_count", "wneu_count", "sneg_count", "spos_count", "sneu_count"]
        elif fs_type == 'Our':
            features_to_select = ["NB_pobj","NB_psubj","vad_neg","vad_neu","vad_pos","affect","anger","friend","future","present","TTR","FKE","SMOG","stop","wordlen","WC","quotes","incl","excl","hear","percept","Exclaim","allcaps","cause","insight","cogmech","certain","tentat","discrep","quant","number","swear","funct","ppron","we","i","shehe","you","ipron","they", "death"]
        elif fs_type == 'POS':
            features_to_select = ["CC","CD","DT","EX","FW","IN","JJ","JJR","JJS","LS","MD","NN","NNS","NNP","NNPS","PDT","POS","PRP","PRP$","RB","RBR","RBS","RP","SYM","TO","UH","WP$","WRB","VB","VBD","VBG","VBN","VBP","VBZ","WDT","WP"]
        elif fs_type == 'ACL13+Our':
            features_to_select = ["bias_count", "assertives_count", "factives_count", "hedges_count", "implicatives_count", "report_verbs_count", "positive_op_count", "negative_op_count", "wneg_count", "wpos_count", "wneu_count", "sneg_count", "spos_count", "sneu_count","NB_pobj","NB_psubj","vad_neg","vad_neu","vad_pos","affect","anger","future","present","TTR","FKE","SMOG","stop","wordlen","WC","quotes","Exclaim","allcaps","cause","insight","cogmech","certain","tentat","discrep","quant","number","swear","funct","ppron","we","i","shehe","you","ipron","they", "incl","excl","hear","percept","inhib","filler", "acheive", "friend", "death"]
    if title == True and body == False:
        if fs_type == 'ACL13':
            features_to_select = ["bias_count_title", "assertives_count_title", "factives_count_title", "hedges_count_title", "implicatives_count_title", "report_verbs_count_title", "positive_op_count_title", "negative_op_count_title", "wneg_count_title", "wpos_count_title", "wneu_count_title", "sneg_count_title", "spos_count_title", "sneu_count_title"]
        elif fs_type == 'Our':
            features_to_select = ["NB_pobj_title","NB_psubj_title","vad_neg_title","vad_neu_title","vad_pos_title","affect_title","anger_title","future_title","present_title","TTR_title","FKE_title","SMOG_title","stop_title","wordlen_title","WC_title","quotes_title","Exclaim_title","allcaps_title","cause_title","insight_title","cogmech_title","certain_title","tentat_title","discrep_title","quant_title","number_title","swear_title","funct_title","ppron_title","we_title","i_title","shehe_title","you_title","ipron_title","they_title", "incl_title","excl_title","hear_title","percept_title","inhib_title","filler_title", "acheive_title", "friend_title"]
        elif fs_type == 'POS':
            features_to_select = ["CC_title","CD_title","DT_title","EX_title","FW_title","IN_title","JJ_title","JJR_title","JJS_title","LS_title","MD_title","NN_title","NNS_title","NNP_title","NNPS_title","PDT_title","POS_title","PRP_title","PRP$_title","RB_title","RBR_title","RBS_title","RP_title","SYM_title","TO_title","UH_title","WP$_title","WRB_title","VB_title","VBD_title","VBG_title","VBN_title","VBP_title","VBZ_title","WDT_title","WP_title"]
        elif fs_type == 'ACL13+Our':
            features_to_select = ["bias_count_title", "assertives_count_title", "factives_count_title", "hedges_count_title", "implicatives_count_title", "report_verbs_count_title", "positive_op_count_title", "negative_op_count_title", "wneg_count_title", "wpos_count_title", "wneu_count_title", "sneg_count_title", "spos_count_title", "sneu_count_title", "NB_pobj_title","NB_psubj_title","vad_neg_title","vad_neu_title","vad_pos_title","affect_title","anger_title","future_title","present_title","TTR_title","FKE_title","SMOG_title","stop_title","wordlen_title","WC_title","quotes_title","Exclaim_title","allcaps_title","cause_title","insight_title","cogmech_title","certain_title","tentat_title","discrep_title","quant_title","number_title","swear_title","funct_title","ppron_title","we_title","i_title","shehe_title","you_title","ipron_title","they_title", "incl_title","excl_title","hear_title","percept_title","inhib_title","filler_title", "acheive_title","friend_title"]
    if title == True and body == True:
        if fs_type == 'ACL13':
            features_to_select = ["bias_count", "assertives_count", "factives_count", "hedges_count", "implicatives_count", "report_verbs_count", "positive_op_count", "negative_op_count", "wneg_count", "wpos_count", "wneu_count", "sneg_count", "spos_count", "sneu_count"]
            title_select = [fc+"_title" for fc in features_to_select]
            features_to_select = features_to_select + title_select
        elif fs_type == 'Our':
            features_to_select = ["NB_pobj","NB_psubj","vad_neg","vad_neu","vad_pos","affect","anger","future","present","TTR","FKE","SMOG","stop","wordlen","WC","quotes","Exclaim","allcaps","cause","insight","cogmech","certain","tentat","discrep","quant","number","swear","funct","ppron","we","i","shehe","you","ipron","they", "death" "incl","excl","hear","percept","inhib","filler", "acheive", "friend"]
            title_select = [fc+"_title" for fc in features_to_select]
            features_to_select = features_to_select + title_select
        elif fs_type == 'POS':
            features_to_select = ["CC","CD","DT","EX","FW","IN","JJ","JJR","JJS","LS","MD","NN","NNS","NNP","NNPS","PDT","POS","PRP","PRP$","RB","RBR","RBS","RP","SYM","TO","UH","WP$","WRB","VB","VBD","VBG","VBN","VBP","VBZ","WDT","WP"]
            title_select = [fc+"_title" for fc in features_to_select]
            features_to_select = features_to_select + title_select
        elif fs_type == 'ACL13+Our':
            features_to_select = ["bias_count", "assertives_count", "factives_count", "hedges_count", "implicatives_count", "report_verbs_count", "positive_op_count", "negative_op_count", "wneg_count", "wpos_count", "wneu_count", "sneg_count", "spos_count", "sneu_count","NB_pobj","NB_psubj","vad_neg","vad_neu","vad_pos","affect","anger","future","present","TTR","FKE","SMOG","stop","wordlen","WC","quotes","Exclaim","allcaps","cause","insight","cogmech","certain","tentat","discrep","quant","number","swear","funct","ppron","we","i","shehe","you","ipron","they","incl","excl","hear","percept","inhib","filler", "acheive", "friend"]
            title_select = [fc+"_title" for fc in features_to_select]
            features_to_select = features_to_select + title_select
            
        inds_to_keep = [feat_labs.index(feat) for feat in features_to_select if feat in feat_labs]
        X_new = []
        for x in Xs:
            i=0
            x_new =[]
            while i < len(x):
                if i in inds_to_keep:
                    x_new.append(x[i])
                i+=1
            X_new.append(x_new)
            features_selected = features_to_select
            
    return X_new, features_selected


def create_train(fn, class1, class2, class3, feature_group_selected, title=True, body=True, oneclassvsall=False):
    X = []
    y = []
    class1data = []
    class2data = []
    class3data = []
    ys = []
    X_all = []
    with open(fn) as f:
        feat_labs = f.readline().strip().split(",")[2:]
        for i in f:
            i = i.strip().split(',')
            ix = [float(q) for q in i[2:]]
            x = tuple(ix)
            if oneclassvsall:
                if i[1] == class1:
                    ys.append(i[1])
                    X_all.append(x)
            else:
                if i[1] == class1 or i[1] == class2 or i[1] == class3:
                    ys.append(i[1])
                    X_all.append(x)
        X_new, features_selected  = predefined_feature_selection(X_all, ys, feat_labs, feature_group_selected, title, body)
        logging.info("Features Selected "+", ".join(features_selected)+"\n")
        XandY = zip(X_new, ys)
        if oneclassvsall:
            for dt in XandY:
                if dt[1] == class1:
                    class1data.append(dt[0])
                elif dt[1] != class1:
                    class2data.append(dt[0])
        else:
            for dt in XandY:
                if dt[1] == class1:
                    class1data.append(dt[0])
                elif dt[1] == class2:
                    class2data.append(dt[0])
                # if dt[1] == class3:
                #     class3data.append(dt[0])

    logging.info(" ".join(("Size of Train Classes:","class1", str(len(class1data)), "class2", str(len(class2data))))+"\n")
    
    for data in class1data:
        y.append(1.0)
        X.append(data)
    for data in class2data:
        y.append(0.0)
        X.append(data)
    # for data in class3data:
    #     y.append(2.0)
    #     X.append(data)
    return X, y, feat_labs

def create_test(fn, class1, class2, class3, feature_group_selected,  title=True, body=True, oneclassvsall=False):
    X = []
    y = []
    class1data = []
    class2data = []
    class3data = []
    ys = []
    X_all = []
    with open(fn) as f:
        feat_labs = f.readline().strip().split(",")[2:]
        for i in f:
            i = i.strip().split(',')
            ix = [float(q) for q in i[2:]]
            x = tuple(ix)
            if oneclassvsall:
                if i[1] == class1:
                    ys.append(i[1])
                    X_all.append(x)
            else:
                if i[1] == class1 or i[1] == class2 or i[1] == class3:
                    ys.append(i[1])
                    X_all.append(x)
        X_new, features_selected  = predefined_feature_selection(X_all, ys, feat_labs, feature_group_selected, title, body)
        XandY = zip(X_new, ys)
        if oneclassvsall:
            for dt in XandY:
                if dt[1] == class1:
                    class1data.append(dt[0])
                elif dt[1] != class1:
                    class2data.append(dt[0])
        else:
            for dt in XandY:
                if dt[1] == class1:
                    class1data.append(dt[0])
                elif dt[1] == class2:
                    class2data.append(dt[0])
                # if dt[1] == class3:
                #     class3data.append(dt[0])

    logging.info(" ".join(("Size of Test Classes:","class1", str(len(class1data)), "class2", str(len(class2data))))+"\n")
    
    for data in class1data:
        y.append(1.0)
        X.append(data)
    for data in class2data:
        y.append(0.0)
        X.append(data)
    # for data in class3data:
    #     y.append(2.0)
    #     X.append(data)
    return X, y, feat_labs

def test(name, clf, X_test, y_test, scale):
    logging.info("--------------\n\n\n")
    logging.info("RESULTS:")
    if scale:
        X_scaled = preprocessing.scale(X_test)
        X_test = X_scaled
    y_test_predictions = [clf.predict(xt.reshape(1, -1)) for xt in X_test]
    score = accuracy_score(y_test, y_test_predictions)
    print "ACC", score
    logging.info(name+"\n")
    logging.info("Test Accuracy: %0.4f " % (score))
##    score = precision_score(y_test, y_test_predictions, average='micro')
##    logging.info("Test Precision: %0.4f " % (score))
    score = recall_score(y_test, y_test_predictions)
    print "ROC", score
##    logging.info("Test Recall: %0.4f " % (score))
##    logging.info("ROC AUC Score: " + str(roc_auc_score(y_test, y_test_predictions)))
    logging.info("--------------\n\n\n")

def learn_params_logreg(X, y):
    X = copy.copy(X)
    y = copy.copy(y)
    scr_prms = []
    Cs = list(np.arange(0.01, 1, 0.01))
    
    for C in Cs:
            X_scaled = preprocessing.scale(X)
            clf = LogisticRegression(C=C, n_jobs=-1)
            clf.fit(X_scaled, y)
            scores = cross_val_score(clf, X_scaled, y, cv=2)
            avg_cv = float(sum(scores))/len(scores)
            scr_prms.append((avg_cv, C))
    best_C = max(scr_prms,key=itemgetter(0))[1]
    return X, y, best_C

if __name__ == "__main__":               
    trainfn = "_newsVSconspiracy_features_selected.csv"
    testfn = "_newsVSconsp_test.csv"
    path = "./"
    feature_groups = ['all']
    user_divides = ['0']
    primary_class = '1'
    class3 = '2'
    title = True
    body = True

    FORMAT = "%(asctime)s %(levelname)s %(module)s %(lineno)d %(funcName)s:: %(message)s"
    logging.basicConfig(filename=trainfn.split(".")[0]+".log", filemode='a', level=logging.DEBUG, format=FORMAT)

    for user_divide in user_divides:
        for group in feature_groups:
            class1 = primary_class
            class2 = user_divide
            logging.info("Class Divide: "+class1+" vs. "+class2+"vs. "+class3)
            logging.info("Feature Group: "+group)
            if user_divide == 'all':
                X, y, feat_labs_train = create_train(path+trainfn, class1, class2,class3, group, title, body, True)
            else:
                X, y, feat_labs_train = create_train(path+trainfn , class1, class2,class3, group, title, body, False)

            # if user_divide == 'all':
            #     X_test, y_test, feat_labs_test = create_test(path+testfn, class1, class2,class3, group, title, body, True)
            # else:
            #     X_test, y_test, feat_labs_test = create_test(path+testfn, class1, class2,class3, group, title, body, False)
            #
            #X = preprocessing.scale(X)
            print len(feat_labs_train)
            #print X.shape[1]
            
            bag_clf = RandomForestClassifier(n_estimators=300)
            bag_clf.fit(X,y)
##            bag_clf = BaggingClassifier(DecisionTreeClassifier(), n_estimators=500, max_samples=X.shape[0], bootstrap=True, n_jobs=-1)
##            bag_clf.fit(X, y)

            filename = 'newsVSconsp.sav'
            pickle.dump(bag_clf, open(filename, 'wb'))
    
            #test("Bagged Decision Trees", bag_clf, np.array(X_test), y_test, scale=False)
            
