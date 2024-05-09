import argparse
import pandas as pd
import numpy as np
from nltk.cluster.util import cosine_distance
import string
import math
import operator
import nltk
from nltk.tokenize import SpaceTokenizer
import re
stopwords=pd.read_csv('./StopwordsHindi.csv')
stopwords=list(stopwords['stopwords'])
stopwords.extend(['में','के','है','से'])

def remove_redundant_sentences(sentences):
    cleaned=[]
    for s in sentences:
        if s in cleaned or s.strip()=='':
            continue
        else:
            cleaned.append(s)
    return cleaned

def clean_corpus(corpus):
    corpus=corpus.replace('।','.')
    corpus=corpus.replace('\xa0','')
    corpus=corpus.replace('\n','')
    corpus=corpus.replace('\r','')
    return corpus

def get_clean_sentences(doc):
    type(doc)
    cleaned_doc=clean_corpus(doc)
    sentences=cleaned_doc.split('.')
    sentences=remove_redundant_sentences(sentences)
    return sentences



patternEnglish = re.compile(r'[[A-Z]|[a-z]]*')
patternNumeric = re.compile(r'.*[0-9]+')
patternBraces=re.compile(r'\[(.*?)\]|\{(.*?)\}|\((.*?)\)')
patternUrl=re.compile(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))")


def titlewordsScore(sentence,heading_titlewords):
    titlewords_sent=SpaceTokenizer().tokenize(sentence)
    titlewords_count=len(heading_titlewords)
    titlewords_sent=[word for word in titlewords_sent if word in heading_titlewords]
    s1_score=len(titlewords_sent)/titlewords_count
    return (s1_score)

def get_len_all_sentences(sentences):
    len_of_all_sent=[len(SpaceTokenizer().tokenize(sentence)) for sentence in sentences]
    max_length=np.max(len_of_all_sent)
    return max_length, len_of_all_sent


def searchEnglishWords(sentence):
    words=SpaceTokenizer().tokenize(sentence.strip())
    words=list(filter(None,words))
    english_words=[word for word in words if patternEnglish.match(word) !=None]
    return len(english_words)/len(words)



def positionScore(total_len):
    mid=(total_len/2)
    positions=(np.arange(total_len,mid,-1)/total_len).tolist()
    if(total_len%2==0):
        positions.extend((np.arange(mid+1,total_len+1,1)/total_len).tolist())
    else:
        positions.extend(np.arange(mid,total_len+1,1).tolist())
    return positions


def numericScore(sentence):
    words=SpaceTokenizer().tokenize(sentence)
    numbers=[1 for word in words if re.match(patternNumeric,word)]
    return np.sum(numbers)/len(words)

def bracesScore(sentence):
    t=re.findall(patternBraces,sentence)
    words=SpaceTokenizer().tokenize(sentence)
    insideTerms=()
    for term in t:
        insideTerms+=term
    insideTerms=[term for term in insideTerms if term !='']
    return (len(words)-len(insideTerms))/len(words)



def url_email_score(sentence):
    words=SpaceTokenizer().tokenize(sentence.strip())
    words=list(filter(None, words))
    urls=[word for word in words if patternUrl.match(word)!=None]
    return len(urls)/len(words)


def generate_summary_rule_based(clean_sentences,compression_ratio):
    score_table=pd.DataFrame(clean_sentences)
    score_table.columns=['sentence']

    headlinetokens=SpaceTokenizer().tokenize(str(clean_sentences))
    heading_titlewords=[ word for word in  headlinetokens if word!= '' and word not in stopwords]
    score_table['S1']=[titlewordsScore(sentence,heading_titlewords) for sentence in clean_sentences]
    max_length,len_of_all_sent=get_len_all_sentences(clean_sentences)
    score_table['S2']=[x/max_length for x in len_of_all_sent]
    score_table['S3']=[searchEnglishWords(sentence) for sentence in clean_sentences]
    score_table['S4']=[numericScore(sentence) for sentence in clean_sentences]
    score_table['S5']=[bracesScore(sentence) for sentence in clean_sentences]
    score_table['S7']=[url_email_score(sentence) for sentence in clean_sentences]
    #score_table['S8']=positionScore(len(clean_sentences))
    score_table['Total']=score_table['S1']+score_table['S2']+score_table['S3']+score_table['S4']+score_table['S5']+score_table['S7']
    summary_sent_count=round(compression_ratio*len(clean_sentences))
    summary_sent=list(score_table.sort_values('Total',ascending=False).iloc[0:summary_sent_count]['sentence'])
    summary=""
    for sentence in summary_sent:
        summary+=sentence.strip()+"| "
    return summary

def generateSummary(sample):
    clean_sentences=get_clean_sentences(sample)
    summary_rule_based=generate_summary_rule_based(clean_sentences,0.4)
    return summary_rule_based