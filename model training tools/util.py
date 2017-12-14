import sys
import csv
import math
import json
import string
import pickle
import logging
import DistanceReader
import numpy as np

def read_info(fname,delim,key=None,inckey=None,incvals=None):
    if not key:
        data = list()
    else:
        data = dict()
    with open(fname,'rU') as f:
        reader = csv.DictReader(f,delimiter=delim,quoting=csv.QUOTE_NONE)
        try:
            for row in reader:
                if not key:
                    if '' in row:
                        logging.debug('skipping, blank entries in row '+str(row))
                        continue
                    data.append(row)
                else:
                    keyval = row[key]
                    if keyval == '':
                        logging.debug('skipping, key value is blank '+str(row)+' key '+str(key))
                        continue
                    if not inckey == None:
                        if not row[inckey] in incvals:
                        	continue
                    if not keyval == None:
                        data[keyval] = row
        except:
            logging.debug('Could not process row '+str(row))
    logging.debug('Read file '+fname)
    return data

def get_tokenized(text):
    text = text.lower()
    text = text.replace('u.s.', 'united_states')
    if type(text) == unicode:
        text = unicodedata.normalize('NFKD', text).encode('ascii','ignore')
    text = text.translate(string.maketrans(string.punctuation," "*len(string.punctuation)))
    return [w for w in text.split(' ') if w != '']

def get_kgrams(text, phraselist, k):
    phrases = []
    for i in range(len(text)-k+1):
        phrase = ('_').join(text[i:i+k])
        if phrase in phraselist:
            phrases.append([0, i, k, phrase])
    return phrases

def clean_text(text, counts, stopwords):
    newtext = []
    for word in text:
        if '_' in word or (word not in stopwords and word.isalpha() and word in counts):
            newtext.append(word)
    return newtext

def get_phrases(text, phrases, counts, key):
    # phrases = list of lists with [0 (replaced with count), position, length, text]
    used = [1]*len(text)
    for i in range(len(phrases)):
        p = phrases[i][3]
        if p in counts:
            phrases[i][0] = counts[p]
    phrases.sort()
    for p in phrases:
        index = p[1]
        length = p[2]
        if used[index:index+length] == [1]*length:
            used[index:index+length] = [0]*length
            text[index] = p[3]
            text[index+1:index+length] = ['']*(length-1)
    return [w for w in text if w != '']

def process_text(text, phraselist, phraselengths, stopwords, counts, key):
    phrases = []
    text = get_tokenized(text)
    if len([t for t in text if t not in counts]) > 0:
        logging.debug('Could not find in lexcounts '+' '.join([t for t in text if t not in counts]))
    text = [t for t in text if t in counts]
    for i in phraselengths:
        phrases += get_kgrams(text, phraselist, i)
    text = get_phrases(text, phrases, counts, key)
    return clean_text(text, counts, stopwords)

def get_top_k(text, counts, key, rev=False):
    freqlist = []
    for w in text:
        if w in counts:
            if not key:
                freqlist.append((float(counts[w]), w))
            else:
                freqlist.append((float(counts[w][key]), w))
    freqlist.sort(reverse=rev)
    
    k = len(freqlist)
    
    top_k_words = [freqlist[i][1] for i in range(k)]
    
    weights = [math.log(freqlist[i][0])+1 for i in range(k)]
    totalval = sum(weights)
    top_k_weights = [w/totalval for w in weights]
    
    return top_k_words,top_k_weights

def write_dict_to_csv(fname, fields, rows):
    with open(fname, 'wb') as f:
        writer = csv.DictWriter(f, delimiter=',', fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    logging.debug('Wrote file '+fname)
