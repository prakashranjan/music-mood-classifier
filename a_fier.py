import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError
import urllib.parse
from sklearn.metrics import confusion_matrix




plt.style.use('ggplot') # make plots look better


#### import the data ####
#df = pd.read_csv("finaldset.csv")
df = pd.read_csv("f1combfinal2.csv")
#df = pd.read_csv("lyset31_g.csv")

#print (df.head())
print (df.describe())


#### Manual Feature selection ####
#sns.FacetGrid(df,
	#hue="mood").map(plt.scatter, "valence", "energy").add_legend()

#plt.show() # expect to see three defined clusters
# it's seen that the petal features seem to describe the species the best


#### prepare data for sklearn ####
# drop irreleveant coloums
df_feature_selected = df.drop(['f_name', 'a_name', 'title', 'lyrics', 'spot_id', 'sr_json', 'tr_json', "mood"], axis=1)
#df_feature_selected = df.drop(['mxm_tid', 'a_name', 'title', 'lyrics', 'spot_id', 'sr_json', 'tr_json', "mood"], axis=1)

# create and encode labels
labels = np.asarray(df.mood)

from sklearn import preprocessing
le = preprocessing.LabelEncoder()
le.fit(labels)

labels = le.transform(labels)

# create features using DictVectorizer, and pandas's to_dict method
df_features = df_feature_selected.to_dict( orient = 'records' )
#print ("features--> ", df_features)
from sklearn.feature_extraction import DictVectorizer
vec = DictVectorizer()
features = vec.fit_transform(df_features).toarray()


##### split up in test and training data ####
from sklearn.model_selection import train_test_split

features_train, features_test, labels_train, labels_test = train_test_split( features, labels, test_size=0.20, random_state=91)


#### Fit to random forests ####

# Random Forests Classifier
from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier( min_samples_split=4, criterion="entropy" )


# Support Vector Classifier

from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

#clf2 = SVC()



clf.fit(features_train, labels_train)
#clf2.fit(features_train, labels_train)

# find the accuracy of the model
acc_test = clf.score(features_test, labels_test)
acc_train = clf.score(features_train, labels_train)
#print ("Train Accuracy:", acc_train)
print ("Test Accuracy:", acc_test)
print("---------------------------------------------")
#acc_test2 = clf2.score(features_test, labels_test)
#acc_train2 = clf2.score(features_train, labels_train)
#print ("Train Accuracy svm:", acc_train2)
#print ("Test Accuracy svm:", acc_test2)





# compute predictions on test features
pred = clf.predict(features_test)

#### Figure out what kind of mistakes it makes ####
from sklearn.metrics import recall_score, precision_score

precision = precision_score(labels_test, pred, average="weighted")
recall = recall_score(labels_test, pred, average="weighted")

print ("Precision:", precision)
print ("Recall:", recall)

print("confusion matrix")
cm = confusion_matrix(labels_test, pred)
print(cm)
plt.matshow(cm)
plt.title('Confusion matrix of the acoustic classifier')
plt.colorbar()
plt.show()

#code for new prediction...

# predict our new music

#code for spotify get meta

username = "212ytsoaogmrrrjt3k37nzp4y"
CLIENT_ID = '7495971772344e3d9bb6e9205965630b'#set at your developer account
CLIENT_SECRET = 'ec7c23b6e4e3463d9c220dd712ba96fe' #set at your developer account
REDIRECT_URI = 'http://google.com/' #set at your developer account,
SCOPE = 'playlist-modify-public'
#erase cache
#try:
    #token = util.prompt_for_user_token(username=username, client_id=CLIENT_ID, client_secret=CLIENT_SECRET,redirect_uri=REDIRECT_URI,scope=SCOPE)
#except:
#os.remove(f".cache-{username}")
token = util.prompt_for_user_token(username=username, client_id=CLIENT_ID, client_secret=CLIENT_SECRET,redirect_uri=REDIRECT_URI, scope=SCOPE)

    #token=util.prompt_for_user_token(username=username,client_id=CLIENT_ID,client_secret=CLIENT_SECRET,redirect_uri=REDIRECT_URI)

#creating sptifyObject
#user= spoto.current_user()
#print(json.dumps(user,sort_keys=True, indent=4))
from tkinter import *
if token:
    def predict_song(aname, titlen, clf):
        # aname = input('Artist name-> ')
        # titlen = input('title-> ')
        if aname=="" or titlen=="":
            print("not music meta found---------------------------")
            res.configure(text=" No Music meta found")
            return
        spoto = spotipy.Spotify(auth=token)
        q = "artist:{} track:{}".format(aname, titlen)
        # print(q)
        try:
            track_find = spoto.search(q, limit=1, offset=0, type='track', market=None)
            track_id = track_find['tracks']['items'][0]['id']
            acou_data = spoto.audio_features(track_id)
            tempo = acou_data[0]['tempo']
            print("tempo : ", tempo)
            energy = acou_data[0]['energy']
            print("energy : ", energy)
            loudness = acou_data[0]['loudness']
            print("loudness : ", loudness)
            danceability = acou_data[0]['danceability']
            print("danceability : ", danceability)
            valence = acou_data[0]['valence']
            print("valence : ", valence)
            acousticness = acou_data[0]['acousticness']
            print("acousticness : ", acousticness)
            tr_json = acou_data[0]
            tr_json_d = json.dumps(tr_json, sort_keys=True, indent=1)

        except:
            track_id = ''
        if track_id:
            # print("\ntrack_id-->", track_id)
            sr_json = json.dumps(track_find, sort_keys=True, indent=1)
            music = [[tempo, energy, danceability, loudness, valence, acousticness]]
            class_code = clf.predict(music)
            confi = clf.predict_proba(music)
            print("\n-------------------------------------------------------------------------------------------\n")
            ha = confi[0][0] * 100
            print("happy %->", ha)
            an = confi[0][1] * 100
            print("angry %->", an)
            sa = confi[0][2] * 100
            print("sad %->", sa)
            rel = confi[0][3] * 100
            print("relax %->", rel)
            # Pie chart, where the slices will be ordered and plotted counter-clockwise:
            labels = 'Happy', 'Angry', 'Sad', 'Relax'
            sizes = [ha, an, sa, rel]
            elevate = sizes.index(max(sizes))
            explode = (0, 0, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
            explode = list(explode)
            explode[elevate] = 0.1
            explode = tuple(explode)
            fig1, ax1 = plt.subplots()
            ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                    shadow=True, startangle=90)
            ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.


            print("----------------------------------------------------------------------------------------------")
            # print(class_code)
            decoded_class = le.inverse_transform(class_code)
            # print (decoded_class)
            if decoded_class == 0:
                print("class-> happy ")
                res.configure(text="Happy")
            elif decoded_class == 1:
                print("class-> angry ")
                res.configure(text="Angry")
            elif decoded_class == 2:
                print("class-> sad ")
                res.configure(text="Sad")
            elif decoded_class == 3:
                print("class-> relax ")
                res.configure(text="Relax")
            else:
                print("failure state")
            fr = {'search_query': str(titlen) + " " + str(aname)}
            encoded = urllib.parse.urlencode(fr)
            print("\n youtube---> https://www.youtube.com/results?" + str(encoded))
            plt.show()
            print("\n")

        else:
            print("not music meta found---------------------------")
            res.configure(text="No Music meta found")
            # theta = int(input("press 1 to try next song--> "))


    def show_entry_fields():
        #print("First Name: %s\nLast Name: %s" % (e1.get(), e2.get()))
        predict_song(e1.get(), e2.get(),clf)


    master = Tk()
    Label(master, text="Artist Name").grid(row=0, pady=10)
    Label(master, text="Song Title").grid(row=1, pady=10)

    e1 = Entry(master)
    e2 = Entry(master)


    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)

    Button(master, text='Quit', command=master.quit).grid(row=3, column=0, sticky=W, pady=20)
    Button(master, text='Classify', command=show_entry_fields).grid(row=3, column=1, sticky=W, pady=20)

    Label(master, text="------ Mood Classifier Acoustic ------" ,bg="yellow", fg="black").grid(row=5, pady=10)
    res = Label(master ,fg="blue")
    res.grid(row=6 ,pady=20)
    mainloop()

else:
    print("not working token-------------")







