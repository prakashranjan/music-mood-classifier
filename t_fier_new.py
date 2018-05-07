import pandas as pd
import re
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, chi2
from PyLyrics import *
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix
from sklearn.linear_model import LogisticRegression


#data = pd.read_csv("finaldset.csv")
#data = pd.read_csv("lyset31_g.csv")
data = pd.read_csv("f1comb.csv")

stemmer = SnowballStemmer('english')
words = stopwords.words("english")

data['cleaned'] = data['lyrics'].apply(lambda x: " ".join([stemmer.stem(i) for i in re.sub("[^a-zA-Z]", " ", x).split() if i not in words]).lower())

X_train, X_test, y_train, y_test = train_test_split(data['cleaned'], data.mood, test_size=0.2 ,random_state=21)

pipeline = Pipeline([('vect', TfidfVectorizer(ngram_range=(1, 2), stop_words="english", sublinear_tf=True)),
                     ('chi',  SelectKBest(chi2, k=10000)),
                     ('clf', LogisticRegression())])
#LinearSVC(C=1.0, penalty='l1', max_iter=3000, dual=False)
#MultinomialNB

model = pipeline.fit(X_train, y_train)

vectorizer = model.named_steps['vect']
chi = model.named_steps['chi']
clf = model.named_steps['clf']

feature_names = vectorizer.get_feature_names()
feature_names = [feature_names[i] for i in chi.get_support(indices=True)]
feature_names = np.asarray(feature_names)

target_names = ['0', '1', '2', '3']
print("top 20 keywords per mood:")
for i, label in enumerate(target_names):
    top10 = np.argsort(clf.coef_[i])[-20:]
    print("%s: %s" % (label, " ".join(feature_names[top10])))

print("accuracy score: " + str(model.score(X_test, y_test)))
print("accuracy score: " + str(model.score(X_train, y_train)))
print("----------------------------------------------------------------------------")

aname = input('Artist name-> ')
titlen = input('title-> ')
if aname and titlen:
    try:
        inly_ly = PyLyrics.getLyrics(aname, titlen)
    except:
        inly_ly = ''

    if inly_ly:
        inly = inly_ly.replace('\n', ' ')
        # print(inly)
        decoded_class=model.predict([inly])
        #print(decoded_class)
        print("\n--------------------------------------------------------------------------------------------\n")
        if str(decoded_class) == "[0]":
            print("class-> happy ")
        elif str(decoded_class) == "[1]":
            print("class-> angry ")
        elif str(decoded_class) == "[2]":
            print("class-> sad ")
        elif str(decoded_class) == "[3]":
            print("class-> relax ")
        else:
            print("failure state")
    else:
        print("incorrect data or no lyrics found")
else:
    print("blank data")