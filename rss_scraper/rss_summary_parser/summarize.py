import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from collections import Counter
from heapq import nlargest
import time
import logging

nlp = spacy.load("en_core_web_sm")

def word_frequency(text:str):
    doc = nlp(text)
    keyword = []
    stopwords = list(STOP_WORDS)
    pos_tag = ['PROPN', 'ADJ', 'NOUN', 'VERB']
    for token in doc:
        if(token.text in stopwords or token.text in punctuation):
            continue
        if(token.pos_ in pos_tag):
            keyword.append(token.text)
    word_freq = Counter(keyword)
    return word_freq


def summarize(text:str, number_of_sentences:int=5):
    text = text.replace("\n","")
    doc = nlp(text)
    word_freq = word_frequency(text)
    sent_strength={}
    for sent in doc.sents:
        for word in sent:
            if word.text in word_freq.keys():
                if sent in sent_strength.keys():
                    sent_strength[sent]+=word_freq[word.text]
                else:
                    sent_strength[sent]=word_freq[word.text]
    summarized_sentences = nlargest(number_of_sentences, sent_strength, key=sent_strength.get)
    final_sentences = [w.text for w in summarized_sentences]
    summary = ' '.join(final_sentences)
    return summary