import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

plt.style.use('ggplot')
print("running")
df = pd.read_csv("dset01.csv")
#df = pd.read_csv("Iris.csv")
print (df.head())
print (df.describe())



#df.plot.scatter(x="SepalLengthCm", y="SepalWidthCm")
df.plot.scatter(x="not", y="old")
plt.show()

#sns.FacetGrid(df,
    #hue="").map(plt.scatter, "S", "S").add_legend()
sns.FacetGrid(df,
    hue="moodlabel").map(plt.scatter, "not", "old").add_legend()

plt.show()


df_feature_selected = df.drop(["moodlabel"], axis=1)

labels = np.asarray(df.moodlabel)
#labels = np.asarray(df.moods)
le = LabelEncoder()
le.fit(labels)

# apply encoding to labels
labels = le.transform(labels)
print(df.sample(5))
#df_selected = df.drop(['', '', "", ""], axis=1)

df_features = df_feature_selected.to_dict(orient='records')


vec = DictVectorizer()
features = vec.fit_transform(df_features).toarray()

features_train, features_test, labels_train, labels_test = train_test_split(
    features, labels,
    test_size=0.20, random_state=42)

# import


# initialize
clf = RandomForestClassifier()

# train the classifier using the training data
clf.fit(features_train, labels_train)
# compute accuracy using test data
acc_test = clf.score(features_test, labels_test)

print ("Test Accuracy:", acc_test)
# Test Accuracy: 0.98

# compute accuracy using training data
acc_train = clf.score(features_train, labels_train)

print ("Train Accuracy:", acc_train)
# Train Accuracy: 0.98
'''
#keywords = [["good","fast"]]
class_code = clf.predict(keywords)
# [1]


decoded_class = le.inverse_transform(class_code)
print (decoded_class)'''

