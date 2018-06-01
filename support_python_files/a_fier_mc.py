import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('ggplot') # make plots look better


#### import the data ####
#df = pd.read_csv("finaldset.csv")
df = pd.read_csv("lyset31_mc_a.csv")

#print (df.head())
#print (df.describe())


#### Manual Feature selection ####
sns.FacetGrid(df,
	hue="pri_mood").map(plt.scatter, "valence", "acousticness").add_legend()

plt.show() # expect to see three defined clusters
# it's seen that the petal features seem to describe the species the best


#### prepare data for sklearn ####
# drop irreleveant coloums
#df_feature_selected = df.drop(['f_name', 'a_name', 'title', 'lyrics', 'spot_id', 'sr_json', 'tr_json', "mood","pri_mood"], axis=1)
df_feature_selected = df.drop(['mxm_tid', 'a_name', 'title', 'lyrics', 'spot_id', 'sr_json', 'tr_json',"tempo","valence" ,"mood", "pri_mood"], axis=1)

# create and encode labels
labels = np.asarray(df.pri_mood)

from sklearn import preprocessing
le = preprocessing.LabelEncoder()
le.fit(labels)

labels = le.transform(labels)
print("labels->", labels)
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

clf2 = SVC()


clf.fit(features_train, labels_train)
clf2.fit(features_train, labels_train)

# find the accuracy of the model
acc_test = clf.score(features_test, labels_test)
acc_train = clf.score(features_train, labels_train)
print ("Train Accuracy:", acc_train)
print ("Test Accuracy:", acc_test)
print("---------------------------------------------")
acc_test2 = clf2.score(features_test, labels_test)
acc_train2 = clf2.score(features_train, labels_train)
print ("Train Accuracy svm:", acc_train2)
print ("Test Accuracy svm:", acc_test2)





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

precision = precision_score(labels_test, pred, average="weighted")
recall = recall_score(labels_test, pred, average="weighted")

print ("Precision:", precision)
print ("Recall:", recall)