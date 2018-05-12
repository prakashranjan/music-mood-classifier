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
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import urllib.parse


def wcloud(word_string):
    # Convert all the required text into a single string here
    # and store them in word_string

    # you can specify fonts, stopwords, background color and other options
    wordcloud = WordCloud(
        stopwords=STOPWORDS,
        background_color='white',
        width=1200,
        height=1000
    ).generate(word_string)

    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()

#data = pd.read_csv("finaldset.csv")
#data = pd.read_csv("lyset31_g.csv")
data = pd.read_csv("f1combfinal2.csv")

#print("0-> ", len(data[data.mood==0]))
#print("1-> ", len(data[data.mood==1]))
#print("2-> ", len(data[data.mood == 2]))
#print("3-> ", len(data[data.mood == 3]))

stemmer = SnowballStemmer('english')
words = stopwords.words("english")

data['cleaned'] = data['lyrics'].apply(lambda x: " ".join([stemmer.stem(i) for i in re.sub("[^a-zA-Z]", " ", x).split() if i not in words]).lower())

X_train, X_test, y_train, y_test = train_test_split(data['cleaned'], data.mood, test_size=0.2 ,random_state=99)

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
#print("top 50 keywords per mood:")
for i, label in enumerate(target_names):
    top10 = np.argsort(clf.coef_[i])[-50:]
    #print("%s: %s" % (label, " ".join(feature_names[top10])))
    print("%s----> "  % (label))
    wcloud(str(" ".join(feature_names[top10])))
pred=model.predict(X_test)
print("Testing accuracy score: " + str(model.score(X_test, y_test)))
#print("traing accuracy score: " + str(model.score(X_train, y_train)))
print("-----------------------------------------------------")
print("confusion matrix")
cm = confusion_matrix(y_test, pred)
print(cm)
plt.matshow(cm)
plt.title('Confusion matrix of the classifier')
plt.colorbar()
plt.show()
print("----------------------------------------------------------------------------")
from tkinter import *
def predict_song(aname, titlen, model):
    #aname = input('Artist name-> ')
    #titlen = input('title-> ')
    if aname and titlen:
        try:
            inly_ly = PyLyrics.getLyrics(aname, titlen)
        except:
            inly_ly = ''

        if inly_ly:
            #print(inly_ly)
            inly = inly_ly.replace('\n', ' ')
            # print(inly)
            decoded_class=model.predict([inly])
            confi=model.predict_proba([inly])
            print("\n-------------------------------------------------------------------------------------------\n")
            ha=confi[0][0]*100
            print("happy %->", ha)
            an=confi[0][1]*100
            print("angry %->", an)
            sa=confi[0][2]*100
            print("sad %->", sa)
            rel=confi[0][3]*100
            print("relax %->", rel)
            # Pie chart, where the slices will be ordered and plotted counter-clockwise:
            labels = 'Happy', 'Angry', 'Sad', 'Relax'
            sizes = [ha, an, sa, rel]
            elevate=sizes.index(max(sizes))
            explode = (0, 0, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
            explode=list(explode)
            explode[elevate]=0.1
            explode=tuple(explode)
            fig1, ax1 = plt.subplots()
            ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                    shadow=True, startangle=90)
            ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            plt.show()

            #print(decoded_class)
            print("\n--------------------------------------------------------------------------------------------\n")
            if str(decoded_class) == "[0]":
                print("class-> happy ")
                res.configure(text="Happy")
            elif str(decoded_class) == "[1]":
                print("class-> angry ")
                res.configure(text="Angry")
            elif str(decoded_class) == "[2]":
                print("class-> sad ")
                res.configure(text="Sad")
            elif str(decoded_class) == "[3]":
                print("class-> relax ")
                res.configure(text="Relax")
            else:
                print("failure state")
                res.configure(text="Failure state")
            fr = {'search_query': str(titlen) + " " + str(aname)}
            encoded = urllib.parse.urlencode(fr)
            print("\n youtube---> https://www.youtube.com/results?" + str(encoded))
            print("\n")
        else:
            print("incorrect data or no lyrics found")
            res.configure(text=" No Music meta found")
    else:
        print("blank data")
        res.configure(text=" Empty ")
    #theta=int(input("press 1 to try next song--> "))
def show_entry_fields():
    #print("First Name: %s\nLast Name: %s" % (e1.get(), e2.get()))
    predict_song(e1.get(), e2.get(),model)


master = Tk()
Label(master, text="Artist Name").grid(row=0, pady=10)
Label(master, text="Song Title").grid(row=1, pady=10)

e1 = Entry(master)
e2 = Entry(master)


e1.grid(row=0, column=1)
e2.grid(row=1, column=1)

Button(master, text='Quit', command=master.quit).grid(row=3, column=0, sticky=W, pady=20)
Button(master, text='Classify', command=show_entry_fields).grid(row=3, column=1, sticky=W, pady=20)

Label(master, text="------ Mood Classifier Lyrical ------" ,bg="yellow", fg="black").grid(row=5, pady=10)
res = Label(master ,fg="blue")
res.grid(row=6 ,pady=20)
mainloop()


print("program over--------------------------------------------------------------")