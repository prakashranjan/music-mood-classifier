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


plt.style.use('ggplot') # make plots look better


#### import the data ####
df = pd.read_csv("finaldset.csv")
#df = pd.read_csv("lyset31_g.csv")

#print (df.head())
print (df.describe())


#### Manual Feature selection ####
sns.FacetGrid(df,
	hue="mood").map(plt.scatter, "valence", "energy").add_legend()

plt.show() # expect to see three defined clusters
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

features_train, features_test, labels_train, labels_test = train_test_split( features, labels, test_size=0.20, random_state=42)


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
print ("Train Accuracy:", acc_train)
print ("Test Accuracy:", acc_test)
print("---------------------------------------------")
#acc_test2 = clf2.score(features_test, labels_test)
#acc_train2 = clf2.score(features_train, labels_train)
#print ("Train Accuracy svm:", acc_train2)
#print ("Test Accuracy svm:", acc_test2)





# compute predictions on test features
pred = clf.predict(features_test)
'''
# predict our new unique iris flower
flower = [[5.2,0.9]]
class_code = clf.predict(flower) # [1]

decoded_class = le.inverse_transform(class_code)
print (decoded_class) # ['Iris-versicolor']

'''
#### Figure out what kind of mistakes it makes ####
from sklearn.metrics import recall_score, precision_score

#precision = precision_score(labels_test, pred, average="weighted")
#recall = recall_score(labels_test, pred, average="weighted")

#print ("Precision:", precision)
#print ("Recall:", recall)

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

if token:
    aname = input('Artist name-> ')
    titlen = input('title-> ')
    spoto = spotipy.Spotify(auth=token)
    q = "artist:{} track:{}".format(aname, titlen)
    #print(q)
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
        track_id=''
    if track_id:
        #print("\ntrack_id-->", track_id)
        sr_json=json.dumps(track_find, sort_keys=True, indent=1)
        music = [[tempo, energy, danceability, loudness, valence, acousticness]]
        class_code = clf.predict(music)
        # print(class_code)
        decoded_class = le.inverse_transform(class_code)
        # print (decoded_class)
        if decoded_class == 0:
            print("class-> happy ")
        elif decoded_class == 1:
            print("class-> angry ")
        elif decoded_class == 2:
            print("class-> sad ")
        elif decoded_class == 3:
            print("class-> relax ")
        else:
            print("failure state")
    else:
        print("not music meta found---------------------------")



else:
    print("not working token-------------")








