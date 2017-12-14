import nltk
from nltk import tokenize
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from readability import Readability
import collections
from nltk.stem.porter import *
from nltk import word_tokenize
import string
import pickle

DIRNAME = os.path.dirname(__file__)

def ttr(text):
    words = text.split()
    dif_words = len(set(words))
    tot_words = len(words)
    if tot_words == 0:
        return 0
    return (float(dif_words)/tot_words)

def POS_features(fn, text, outpath):
    fname = os.path.join(outpath, fn.split(".")[0]+"_tagged.txt")

    pos_tags = ["CC","CD","DT","EX","FW","IN","JJ","JJR","JJS","LS","MD","NN","NNS","NNP","NNPS","PDT","POS","PRP","PRP$","RB","RBR","RBS","RP","SYM","TO","UH","WP$","WRB","VB","VBD","VBG","VBN","VBP","VBZ","WDT","WP"]
    sents = tokenize.sent_tokenize(text)
    counts_norm = []
    allwords = []
    sents = tokenize.sent_tokenize(text)

    with open(fname, "w") as out:
        for sent in sents:
            words = sent.strip(".").split()
            tags = nltk.pos_tag(words)
            strtags = ["/".join((wt[0],wt[1])) for wt in tags]
            out.write(" ".join(strtags)+" ")

    with open(fname, "r") as fl:
        line = fl.readline() #each file is one line

    wordandtag = line.strip().split()
    try:
        tags = [wt.split("/")[1] for wt in wordandtag]
    except:
        print wordandtag
    counts = collections.Counter(tags)

    for pt in pos_tags:
        try:
           counts_norm.append(float(counts[pt])/len(tags))
        except:
            counts_norm.append(0)

    return counts_norm

def vadersent(text):
    analyzer = SentimentIntensityAnalyzer()
    vs = analyzer.polarity_scores(text)
    return vs['neg'], vs['neu'], vs['pos']

def readability(text):
    rd = Readability(text)
    fkg_score = rd.FleschKincaidGradeLevel()
    SMOG = rd.SMOGIndex()
    return fkg_score, SMOG

def wordlen_and_stop(text):
    with open("./resources/stopwords.txt") as data:
        stopwords = [w.strip() for w in data]
    set(stopwords)
    words = word_tokenize(text)
    WC = len(words)
    stopwords_in_text = [s for s in words if s in stopwords]
    percent_sws = float(len(stopwords_in_text))/len(words)
    lengths = [len(w) for w in words if w not in stopwords]
    if len(lengths) == 0:
        word_len_avg = 3
    else:
        word_len_avg = float(sum(lengths))/len(lengths)
    return percent_sws, word_len_avg, WC

def stuff_LIWC_leftout(pid, text):
    puncs = set(string.punctuation)
    tokens = word_tokenize(text)
    quotes = tokens.count("\"")+tokens.count('``')+tokens.count("''")
    Exclaim = tokens.count("!")
    AllPunc = 0
    for p in puncs:
        AllPunc+=tokens.count(p)
    words_upper = 0
    for w in tokens:
        if w.isupper():
            words_upper+=1
    try:
        allcaps = float(words_upper)/len(tokens)
    except:
        print pid
    return (float(quotes)/len(tokens))*100, (float(Exclaim)/len(tokens))*100, (float(AllPunc)/len(tokens))*100, allcaps

def subjectivity(text):
    loaded_model = pickle.load(open(os.path.join(DIRNAME, 'resources', 'NB_Subj_Model.sav'), 'rb'))
    count_vect = pickle.load(open(os.path.join(DIRNAME, 'resources', 'count_vect.sav'), 'rb'))
    tfidf_transformer = pickle.load(open(os.path.join(DIRNAME, 'resources', 'tfidf_transformer.sav'), 'rb'))
    X_new_counts = count_vect.transform([text])
    X_new_tfidf = tfidf_transformer.transform(X_new_counts)
    result = loaded_model.predict_proba(X_new_tfidf)
    prob_obj = result[0][0]
    prob_subj = result[0][1]
    return prob_obj, prob_subj

def load_LIWC_dictionaries(filepath="./resources/"):
    cat_dict = {}
    stem_dict = {}
    counts_dict = {}
    with open(os.path.join(filepath, "LIWC2007_English100131.dic")) as raw:
        raw.readline()
        for line in raw:
            if line.strip() == "%":
                break
            line = line.strip().split()
            cat_dict[line[0]] = line[1]
            counts_dict[line[0]] = 0
        for line in raw:
            line = line.strip().split()
            stem_dict[line[0]] = [l.replace("*","") for l in line[1:]]
    return cat_dict, stem_dict, counts_dict

def LIWC(text, cat_dict, stem_dict, counts_dict):
    for key in counts_dict:
        counts_dict[key] = 0
    tokens = word_tokenize(text)
    WC = len(tokens)
    stemmer = PorterStemmer()
    stemed_tokens = [stemmer.stem(t) for t in tokens]
    
    #count and percentage
    for stem in stem_dict:
        count = stemed_tokens.count(stem.replace("*", ""))
        if count > 0:
            for cat in stem_dict[stem]:
                counts_dict[cat]+=count
    counts_norm = [float(counts_dict[cat])/WC*100 for cat in counts_dict]
    cats = [cat_dict[cat] for cat in cat_dict]
    return counts_norm, cats

def fix(text): # this is just my frustating attempt to fix unicode junk
    text = text.replace("\r", "").replace('\n', "").replace("\ufffd'", "")
    text = text.decode("ascii", "ignore")
    return text

def whatsbeendon(filename):
    pids = []
    try:
        with open(filename) as data:
            pids = [line.strip().split(",")[0] for line in data]
        return set(pids)
    except:
        return set(pids)
            
#main
done = whatsbeendon("all_features_training_worldnews.csv")
outpath = "./"
cat_dict, stem_dict, counts_dict = load_LIWC_dictionaries()
liwc_cats = [cat_dict[cat] for cat in cat_dict]
pos_tags = ["CC","CD","DT","EX","FW","IN","JJ","JJR","JJS","LS","MD","NN","NNS","NNP","NNPS","PDT","POS","PRP","PRP$","RB","RBR","RBS","RP","SYM","TO","UH","WP$","WRB","VB","VBD","VBG","VBN","VBP","VBZ","WDT","WP"]
pos_tags_titles = [t+"_title" for t in pos_tags]
liwc_cats_title = [t+"_title" for t in liwc_cats]

if len(done) == 0:
    with open(os.path.join(outpath, "all_features_training_worldnews.csv"), "a") as out:
        seq = ("pid,TTR,vad_neg,vad_neu,vad_pos,FKE,SMOG,stop,wordlen,WC,NB_pobj,NB_psubj,quotes,Exclaim,AllPunc,allcaps",",".join(pos_tags),",".join(liwc_cats), "TTR_title,vad_neg_title,vad_neu_title,vad_pos_title,FKE_title,SMOG_title,stop_title,wordlen_title,WC_title,NB_pobj_title,NB_psubj_title,quotes_title,Exclaim_title,AllPunc_title,allcaps_title",",".join(pos_tags_titles),",".join(liwc_cats_title))
        out.write(",".join(seq)+"\n")

path = "D:\\RPI Research\\Credibility Toolkit\\Scraping Folder\\worldnews_articles_2012+2013\\"
title_path = "D:\\RPI Research\\Credibility Toolkit\\Scraping Folder\\worldnews_titles_2012+2013\\"
for fn in os.listdir(path):
    pid = fn.split(".")[0]
    if pid in done:
        continue
    else:
        print "working on", pid
    try:
        with open(path+fn) as textdata:
            text_content = [line.strip() for line in textdata]
            text = " ".join(text_content)
            text = fix(text)
        with open(title_path+fn) as titledata:
            text_content = [line.strip() for line in titledata]
            title_text = " ".join(text_content)
            title_text = fix(title_text)
    except:
        continue
   
    if len(text) == 0:
        raise ValueError("No Text")
    
    toks = word_tokenize(title_text)
    if len(toks) == 0:
        continue
    
    pos_features_path = "./temp/"
    #body
    quotes, Exclaim, AllPunc, allcaps = stuff_LIWC_leftout(pid, text)
    lex_div = ttr(text)
    counts_norm = POS_features("input", text, pos_features_path)
    counts_norm = [str(c) for c in counts_norm]
    counts_norm_liwc, liwc_cats = LIWC(text, cat_dict, stem_dict, counts_dict)
    counts_norm_liwc = [str(c) for c in counts_norm_liwc]
    vadneg, vadneu, vadpos = vadersent(text)
    fke, SMOG = readability(text)
    stop, wordlen, WC = wordlen_and_stop(text)
    NB_pobj, NB_psubj = subjectivity(text)

    #title
    quotes_titles, Exclaim_titles, AllPunc_titles, allcaps_titles = stuff_LIWC_leftout(pid, title_text)
    lex_div_title = ttr(title_text)
    counts_norm_title = POS_features("input_title", title_text, pos_features_path)
    counts_norm_title = [str(c) for c in counts_norm]
    counts_norm_liwc_title, liwc_cats_title2 = LIWC(title_text, cat_dict, stem_dict, counts_dict)
    counts_norm_liwc_title = [str(c) for c in counts_norm_liwc_title]
    vadneg_title, vadneu_title, vadpos_title = vadersent(title_text)
    fke_title, SMOG_title = readability(title_text)
    stop_title, wordlen_title, WC_title = wordlen_and_stop(title_text)
    NB_pobj_title, NB_psubj_title = subjectivity(title_text)

    
    with open(os.path.join(outpath, "all_features_training_worldnews.csv"), "a") as out:
        seq = (str(pid),str(lex_div),str(vadneg),str(vadneu),str(vadpos),str(fke),str(SMOG),str(stop),str(wordlen),str(WC),str(NB_pobj),str(NB_psubj),str(quotes),str(Exclaim),str(AllPunc),str(allcaps), ",".join(counts_norm), ",".join(counts_norm_liwc),str(lex_div_title),str(vadneg_title),str(vadneu_title),str(vadpos_title),str(fke_title),str(SMOG_title),str(stop_title),str(wordlen_title),str(WC_title),str(NB_pobj_title),str(NB_psubj_title),str(quotes_titles),str(Exclaim_titles),str(AllPunc_titles),str(allcaps_titles), ",".join(counts_norm_title), ",".join(counts_norm_liwc_title))
        feat_str = ",".join(seq)
        out.write(feat_str + "\n")
    
    

