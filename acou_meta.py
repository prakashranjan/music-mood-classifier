#spotify api
#get metadata of songs


import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError
import sqlite3

outputf = "output.db"
conn = sqlite3.connect(outputf)

username = "212ytsoaogmrrrjt3k37nzp4y"
CLIENT_ID = '7495971772344e3d9bb6e9205965630b'#set at your developer account
CLIENT_SECRET = 'ec7c23b6e4e3463d9c220dd712ba96fe' #set at your developer account
REDIRECT_URI = 'http://google.com/' #set at your developer account,
SCOPE = 'playlist-modify-public'
#erase cache
try:
    token = util.prompt_for_user_token(username=username, client_id=CLIENT_ID, client_secret=CLIENT_SECRET,redirect_uri=REDIRECT_URI,scope=SCOPE)
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username=username, client_id=CLIENT_ID, client_secret=CLIENT_SECRET,redirect_uri=REDIRECT_URI, scope=SCOPE)

    #token=util.prompt_for_user_token(username=username,client_id=CLIENT_ID,client_secret=CLIENT_SECRET,redirect_uri=REDIRECT_URI)

#creating sptifyObject
#user= spoto.current_user()
#print(json.dumps(user,sort_keys=True, indent=4))
if token:
    spoto = spotipy.Spotify(auth=token)
    qo = "Select spot_id from lyset21 limit 56 offset 199"
    res = conn.execute(qo)
    kw = res.fetchall()
    j=0
    tracks=list()
    for k in range(len(kw)):
        spot_id=kw[k][0]
        tracks.append(spot_id)


    print("tracks--> ",tracks)

    try:
        acou_data = spoto.audio_features(tracks)

    except:
        acou_data=''
    if acou_data:
        sr_json=json.dumps(acou_data, sort_keys=True, indent=1)
        print(sr_json)
        for m in range(len(tracks)):
            try:
                tempo = acou_data[m]['tempo']
                #print("tempo : ", tempo)
                energy = acou_data[m]['energy']
                #print("energy : ", energy)
                loudness = acou_data[m]['loudness']
                #print("loudness : ", loudness)
                danceability = acou_data[m]['danceability']
                #print("danceability : ", danceability)
                valence = acou_data[m]['valence']
                #print("valence : ", valence)
                acousticness = acou_data[m]['acousticness']
                #print("acousticness : ", acousticness)
                tr_json=acou_data[m]
                tr_json_d=json.dumps(tr_json, sort_keys=True, indent=1)
            except:
                tempo=''
            if tempo:
                song_id = acou_data[m]['id']
                print("spot_id: ",song_id)
                #conn.execute(""" UPDATE lyset21 set  tempo = ?, energy = ?, danceability = ?, loudness = ?, valence = ?, acousticness = ?, tr_json = ? where spot_id= ? """,(tempo, energy, danceability, loudness, valence, acousticness, tr_json_d, song_id))
                print("run update query ", m)
                conn.commit()
                j=j+1

            print("\n--------------------------------------------------\n")



        #conn.commit()



    conn.commit()
    print("all-->", k + 1)
    print("done-->", j)
    print("failed-->", (k + 1) - j)

else:
    print("not working token-------------")








'''
track_meta=spoto.audio_features(track_id)
print("\n--------------------------------------------------\n")
print(json.dumps(track_meta,sort_keys=True, indent=4))

print("\n--------------------------------------------------\n")
tempo=track_meta[0]['tempo']
print("tempo : ", tempo)
energy=track_meta[0]['energy']
print("energy : ", energy)
loudness=track_meta[0]['loudness']
print("loudness : ", loudness)
danceability=track_meta[0]['danceability']
print("danceability : ", danceability)
valence=track_meta[0]['valence']
print("valence : ", valence)
acousticness=track_meta[0]['acousticness']
print("acousticness : ", acousticness)'''
