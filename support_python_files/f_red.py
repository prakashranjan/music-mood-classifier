#!/usr/bin/env python


import os
import sys
import sqlite3
import nltk
from nltk import wordpunct_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.corpus import words
from nltk import pos_tag
from nltk.tokenize import word_tokenize
#nltk.download()


def encode_string(s):
    """
    Simple utility function to make sure a string is proper
    to be used in a SQLite query
    (different than posgtresql, no N to specify unicode)
    EXAMPLE:
      That's my boy! -> 'That''s my boy!'
    """
    return "'" + s.replace("'", "''") + "'"


def die_with_usage():
    """ HELP MENU """
    print('mxm_dataset_to_db.py')
    print('   by T. Bertin-Mahieux (2011) Columbia University')
    print('      tb2332@columbia.edu')
    print('This code puts the musiXmatch dataset into an SQLite database.')
    print('')
    print('USAGE:')
    print('  ./lymeta_cr.py <matchmap_file.txt> <output.db>')
    print('PARAMS:')
    print('      <train>  - mXm dataset matchmap text  file')
    print('  <output.db>  - SQLite database to create')
    sys.exit(0)


if __name__ == '__main__':

    # help menu
    #if len(sys.argv) < 3:
       # die_with_usage()

    # params
    stop_words = set(stopwords.words('english'))
    outputf = "output.db"
    # open output SQLite file
    conn = sqlite3.connect(outputf)

    # create tables -> stemmap
    q = "Select stem,word from stemmap3 "
    res=conn.execute(q)
    tmpwords = res.fetchall()
    #assert len(tmpwords) == len(topwords), 'Number of words issue.'
    j=0
    m=0
    h=0
    o=0
    a=0
    manywords = words.words()
    for k in range(len(tmpwords)):
        tempo= tmpwords[k][0]
        tempot=tempo
        tempo=tempo.capitalize()
        tempo2= tmpwords[k][1]
        tempo2t=tempo2
        tempo2=tempo2.capitalize()
        t1= word_tokenize(str(tempo))
        t2 = word_tokenize(str(tempo2))
        token_pos=pos_tag(t1)
        token_pos2 = pos_tag(t2)
        x1=token_pos
        x2=token_pos2
        #print(x2[0][1])
        if x2[0][1]=="VB" or x2[0][1]=="VBD" or x2[0][1]=="VBG" or x2[0][1]=="VBN" or x2[0][1]=="VBP" or x2[0][1]=="VBZ":
            h=h+1
            #print("verb word- %d > %s:%s" % (k + 1, tempo, tempo2))
            #dtemres3 = 'update stemmap set pos="VB" where stem="' + tempot + '" AND pos IS NULL'
            #conn.execute(dtemres3)
            #if (h % 50 == 0):
                #conn.commit()
                #print("verb complete->", h)
        elif x2[0][1]=="JJ" or x2[0][1]=="JJR" or x2[0][1]=="JJS":
            o = o + 1
            #print("adjective word- %d > %s:%s" % (k + 1, tempo, tempo2))
            #dtemres2 = 'update stemmap set pos="JJ" where stem="' + tempot + '" AND pos IS NULL'
            #conn.execute(dtemres2)
            #if(o%50==0):
                #conn.commit()
                #print("adjective complete->", o)
        else:
            a = a + 1
            #dtemres = 'delete from stemmap2 where stem="' + tempo + '"'
            #conn.execute(dtemres)


        if tempot not in manywords and tempo2t not in manywords:
            print("non eng-word- %d > %s:%s" % (k+1, tempo,tempo2))
            dtem = 'delete from stemmap3 where stem="'+tempot+'"'
            conn.execute(dtem)
            j=j+1
        elif tempo in stop_words or tempo2 in stop_words or tempot in stop_words or tempo2t in stop_words:
            print("stopword- %d > %s:%s" % (k + 1, tempo,tempo2))
            dtemst = 'delete from stemmap3 where stem="'+tempot+'"'
            conn.execute(dtemst)
            m = m + 1

        #assert tmpwords[k][0] == k + 1, 'ROWID issue.'
        #assert tmpwords[k][0].encode('utf-8') == topwords[k], 'ROWID issue.'
    conn.commit()
    print("%d words deleted." % (j))
    print("%d stopwords deleted." % (m))
    print("%d verb all words deleted." % (h))
    print("%d adjective all words deleted." % (o))
    print("%d rest of all words deleted." % (a))
    print("%d total words' table filled, checked." % (k+1))










    print('feature reduction done.')

    # close output SQLite connection
    conn.close()