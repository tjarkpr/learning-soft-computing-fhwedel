import sys
import os
import json
import joblib
import string
import numpy as np
import pandas as pd
import nltk

old_stdout = sys.stdout
old_stderr = sys.stderr
sys.stdout = open(os.devnull, 'w')
sys.stderr = open(os.devnull, 'w')

nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)

from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from nltk.tokenize import TweetTokenizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.kernel_ridge import KernelRidge
from sklearn.metrics import f1_score, make_scorer
from sklearn.model_selection import GridSearchCV

CURRENT_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
VOCABULARY_NAME = 'vocabulary.csv'
VOCABULARY_PATH = CURRENT_DIR + '/data/' + VOCABULARY_NAME
MODEL_NAME = 'best-model.pkl'
MODEL_PATH = CURRENT_DIR + '/data/' + MODEL_NAME
NGRAM_RANGE = (1,2)

vocabulary = pd.read_csv(VOCABULARY_PATH, header=None)
lemmatizer = WordNetLemmatizer()
tokenizer = TweetTokenizer()

def score(y_true, y_pred):
    y_pred = np.rint(y_pred)
    return f1_score(y_true, y_pred, average='micro')

def lemmatize_words(comment):
    word_list = pos_tag(tokenizer.tokenize(comment))
    lemmatize_words = []
    for word, tag in word_list:
        wtag = tag[0].lower()
        if wtag in ['a', 'r', 'n', 'v', 's']:
            word = lemmatizer.lemmatize(word, wtag)
        lemmatize_words.append(word)
    return ' '.join(lemmatize_words)

def remove_punctuation(text):
    if type(text) != str or len(text) == 0:
        return np.nan
    
    clean_text = ""
    for char in text:
        if char not in string.punctuation:
            clean_text += char
    return clean_text

def generate_features(sentence):
    sentence = lemmatize_words(sentence)
    sentence = remove_punctuation(sentence)
    count_vectorizer = CountVectorizer(lowercase=True, analyzer='word', stop_words='english', ngram_range=NGRAM_RANGE, vocabulary=vocabulary.iloc[:, 0].values.astype('U'))
    bag_of_words = count_vectorizer.fit_transform([sentence]) 

    return np.array(bag_of_words.todense())

if __name__ == '__main__':
    SENTENCE = sys.argv[1]
    if SENTENCE != None and SENTENCE != '':
        model = joblib.load(MODEL_PATH)
        features = generate_features(SENTENCE)
        prediction = model.predict(features)
        prediction_rounded = np.rint(prediction)
        if (prediction_rounded[0] == 0):
            prediction = 1 - prediction
        result_json = '{"input": "' + SENTENCE + '", "result" : ' + str(prediction_rounded[0]) + ', "probability" : ' + str(prediction) + '}'
    else:
        result_json = '{"input": "", "result" : 0.0, "probability" : 1}'
    
    parsed = json.loads(result_json)
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    print(json.dumps(parsed))
