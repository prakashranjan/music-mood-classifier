import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import sys
import requests
from PyLyrics import *
import requests
import urllib.parse

#https://github.com/shreyans29/thesemicolon/blob/master/Text%20Analytics%20tfidf.ipynb
if __name__ == '__main__':

    df=pd.read_csv("finaldset.csv")

    df.head()

    #print(len(df))
    '''
    print("0-> ", len(df[df.mood==0]))
    print("1-> ", len(df[df.mood==1]))
    print("2-> ", len(df[df.mood == 2]))
    print("3-> ", len(df[df.mood == 3]))
    '''
    #df.loc[df["Status"]=='ham',"Status",]=1

    #df.loc[df["Status"]=='spam',"Status",]=0

    #df.head()

    df_x=df["lyrics"]
    df_y=df["mood"]

    cv = TfidfVectorizer(min_df=1,stop_words='english')

    x_train, x_test, y_train, y_test = train_test_split(df_x, df_y, test_size=0.20, random_state=22)

    #print(x_train.head())

    cv = TfidfVectorizer(min_df=1,stop_words='english')
    '''
    x_traincv = cv.fit_transform(["Hi How are you How are you doing","Hi what's up","Wow that's awesome"])

    x_traincv.toarray()

    cv.get_feature_names()
    '''
    cv1 = TfidfVectorizer(min_df=1,stop_words='english')

    x_traincv = cv1.fit_transform(x_train)

    a=x_traincv.toarray()

    print(a[0])
    print(cv1.get_feature_names())
    cv1.inverse_transform(a[0])

    print(x_train.iloc[1])
    print("x-test--------------",x_test)
    x_testcv=cv1.transform(x_test)

    x_testcv.toarray()

    mnb = MultinomialNB()

    y_train=y_train.astype('int')

    #print(y_train)

    mnb.fit(x_traincv,y_train)

    #testmessage=x_test.iloc[0]

    #print(testmessage)
    print("---input format---", x_testcv)

    predictions=mnb.predict(x_testcv)

    #print(predictions)

    a=np.array(y_test)

    #print(a)

    count=0

    for i in range (len(predictions)):
        if predictions[i]==a[i]:
            count=count+1

    out=len(predictions)
    accuracy=(count/out)*100
    print("accuracy-> ", accuracy)

    #get percentage'''







    n_testcv = cv1.fit_transform(["Hi How are you How are you doing"])

    n_testcv.toarray()
    print(n_testcv)
    predict_val = mnb.predict(n_testcv)
    print(predict_val)

