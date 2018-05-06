#!/usr/bin/env python

import os
import sys
import requests
from PyLyrics import *
import sqlite3
import requests
import urllib.parse

try:
    from stemming.porter2 import stem
except ImportError:
    print('You need to install the following stemming package:')
    print('http://pypi.python.org/pypi/stemming/1.0')
    sys.exit(0)


def lyrics_to_bow(lyrics):
    outputf = "output.db"

    # sanity checks
    # if not os.path.isfile(trainf):
    # print('ERROR: %s does not exist.' % trainf)
    # sys.exit(0)

    if not os.path.isfile(outputf):
        print('ERROR: %s does not exists.' % outputf)
        sys.exit(0)
    lyrics_flat = lyrics.replace('\r', '\n').replace('\n', ' ').lower()
    lyrics_flat = ' ' + lyrics_flat + ' '
    # special cases (English...)
    lyrics_flat = lyrics_flat.replace("'m ", " am ")
    lyrics_flat = lyrics_flat.replace("'re ", " are ")
    lyrics_flat = lyrics_flat.replace("'ve ", " have ")
    lyrics_flat = lyrics_flat.replace("'d ", " would ")
    lyrics_flat = lyrics_flat.replace("'ll ", " will ")
    lyrics_flat = lyrics_flat.replace(" he's ", " he is ")
    lyrics_flat = lyrics_flat.replace(" she's ", " she is ")
    lyrics_flat = lyrics_flat.replace(" it's ", " it is ")
    lyrics_flat = lyrics_flat.replace(" ain't ", " is not ")
    lyrics_flat = lyrics_flat.replace("n't ", " not ")
    lyrics_flat = lyrics_flat.replace("'s ", " ")
    # remove boring punctuation and weird signs
    punctuation = (',', "'", '"', ",", ';', ':', '.', '?', '!', '(', ')',
                   '{', '}', '/', '\\', '_', '|', '-', '@', '#', '*')
    for p in punctuation:
        lyrics_flat = lyrics_flat.replace(p, '')
    words = [x for x in lyrics_flat.split(' ') if x.strip() != '']
    # stem words
    words = [stem(x) for x in words]

    # open output SQLite file
    conn = sqlite3.connect(outputf)
    qo = "Select stem from stemmap4"
    res = conn.execute(qo)
    kw = res.fetchall()
    kli=list()
    for k in range(len(kw)):
        kli.append(kw[k][0])
    #print(words)
    #print(kli)

    bow = {}
    for w in words:
        if not w in list(bow.keys()):
            bow[w] = 1
        else:
            bow[w] += 1
    # remove special words that are wrong
    fake_words = ('>', '<', 'outro~')
    bowwords = list(bow.keys())
    for bw in bowwords:
        if bw in fake_words or bw not in kli:
            #print(bw)
            bow.pop(bw)
        elif bw.find(']') >= 0:
            bow.pop(bw)
        elif bw.find('[') >= 0:
            bow.pop(bw)

    # not big enough? remove instrumental ones among others
    if len(bow) <= 3:
        return None
    # done
    return bow


def die_with_usage():
    """ HELP MENU """

    print('This code shows how we transformed lyrics into bag-of-words.')
    print('It is mostly intended to be used as a library, but you can pass')
    print('in lyrics and we print the resulting dictionary.')
    print('')

    sys.exit(0)


if __name__ == '__main__':

    # help menu
   # if len(sys.argv) < 2:
      #  die_with_usage()



    # params (lyrics)
    lyrics= ''
    tid=input("enter mxm_tid--> ")
    print(tid)


    r = requests.get("http://api.musixmatch.com/ws/1.1/track.lyrics.get?track_id="+tid+"&apikey=53d782798f96d7c47ac1a2fd0246dbf0")
    #print(r.status_code)

    if(r.status_code!=200):
        #print("\n music language not found")
        sys.exit()
    info = requests.get(
        "http://api.musixmatch.com/ws/1.1/track.get?track_id=" + tid + "&apikey=53d782798f96d7c47ac1a2fd0246dbf0")
    #print(info.status_code)

    if (info.status_code != 200):
        #print("\n music details not found")
        sys.exit()



    inly_body=r.json()
    inly_info = info.json()
    #print(inly_body)
    #inly_ly=inly_body['message']['body']['lyrics']['lyrics_body']
    #print("\n lyrics: ", inly_ly)

    if(inly_body['message']['header']['status_code']!=200):
        print("\n music language not found")
        sys.exit()
    if (inly_info['message']['header']['status_code'] != 200):
        print("\n music details not found")
        sys.exit()


    inly_lang=inly_body['message']['body']['lyrics']['lyrics_language']
    inly_name = inly_info['message']['body']['track']['track_name']
    inly_al_name =inly_info['message']['body']['track']['album_name']
    inly_a_name = inly_info['message']['body']['track']['artist_name']
    print("\n------------------------------------------------Meta-----------------------\n")
    print("\n Music language: ", inly_lang)
    print("\n Music name: ", inly_name)
    print("\n Music album name: ", inly_al_name)
    print("\n Music artist name: ", inly_a_name)
    f={'search_query': str(inly_name)+" "+str(inly_a_name)}
    encoded=urllib.parse.urlencode(f)
    print("\n youtube---> https://www.youtube.com/results?"+str(encoded))
    print("\n")

    inly_ly=PyLyrics.getLyrics(inly_a_name, inly_name)  # Print the lyrics directly

    #inly_ly=""
    inly = [" "+inly_ly+" "]
    inly[0].replace('\r\n','')

    for word in inly[0:]:
        lyrics += ' ' + word
        #print("\n", word)
    lyrics = lyrics.strip()


    # make bag of words
    bow = lyrics_to_bow(lyrics)
    if bow is None:
        print('ERROR, maybe there was not enough words to be realistic?')
        sys.exit(0)

    # print result
    try:
        from operator import itemgetter
        print("\n--------------------------------------Matched keyword---------------------\n")
        karta=sorted(list(bow.items()), key=itemgetter(1), reverse=True)
        for h in karta:
            print(str(h[0])+"--->"+str(h[1]))
    except ImportError:
        print(bow)
    print("\n-----------------------------------Mood help----------------------------------\n")
    rmh = requests.post("https://tone-analyzer-demo.ng.bluemix.net/api/tone", data={'text': inly_ly , 'language': 'en'})
    if rmh.status_code==200:
        moodh_body = rmh.json()
        y=moodh_body['document_tone']['tones']
        for l in y:
            i=l['score'] * 100
            print(str(round(i,1))+"% ---> "+str(l['tone_name']))

    print("\n------------------------------------lyrics---------------------------------\n")
    print("\n", inly_ly)
