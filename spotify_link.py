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
    spoto = spotipy.Spotify(auth=token)
    #qo = "Select a_name, title, f_name from relax_all"
    qo = "Select a_name, title, mxm_tid from lyset21"
    res = conn.execute(qo)
    kw = res.fetchall()
    j=0
    for k in range(len(kw)):
        aname=kw[k][0]
        titlen=kw[k][1]
        f_name=kw[k][2]
        q = "artist:{} track:{}".format(aname, titlen)
        print(q)

        try:
            track_find = spoto.search(q, limit=1, offset=0, type='track', market=None)
            track_id = track_find['tracks']['items'][0]['id']
        except:
            track_id=''
        if track_id:
            print("\ntrack_id-->", track_id)
            sr_json=json.dumps(track_find, sort_keys=True, indent=1)
            #conn.execute(""" UPDATE relax_all set spot_id = ?, sr_json = ? where f_name= ? """, (track_id, sr_json, f_name))
            #conn.execute(""" UPDATE lyset21 set spot_id = ?, sr_json = ? where mxm_tid= ? """,(track_id, sr_json, f_name))
            j=j+1
            conn.commit()
        print("\n--------------------------------------------\n")

    conn.commit()
    print("all-->", k + 1)
    print("success-->", j)
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
