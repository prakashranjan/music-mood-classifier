import os
import sys
import string
from mp3_tagger import MP3File, VERSION_1, VERSION_2, VERSION_BOTH
import sqlite3

count = 0
directory="dataset_audio/Angry_all"
outputf = "output.db"
conn = sqlite3.connect(outputf)
for filename in os.listdir(directory):
    if filename.endswith(".mp3"):
        #print(filename)
        path_to_mp3=directory+"/"+filename
        mp3 = MP3File(path_to_mp3)
        try:
            tags = mp3.get_tags()
            song=tags['ID3TagV1']['song']
            song=song.strip()
            artist=tags['ID3TagV1']['artist']
            artist=artist.strip()
        except:
            tags=""
        if tags:
            if song=="UUUUUUUUUUUUUUUUUUUUUUUUUUUUUU" or artist=="UUUUUUUUUUUUUUUUUUUUUUUUUUUUUU" or song=="" or artist=="" or song=="ЄЄЄЄЄЄЄЄЄЄЄЄЄЄЄЄЄЄЄЄЄЄЄЄЄЄЄЄЄЄ" or artist=="ЄЄЄЄЄЄЄЄЄЄЄЄЄЄЄЄЄЄЄЄЄЄЄЄЄЄЄЄЄЄ" :
                #print("empty-tags--> ", filename)
                print("----")
            else:
                print("song--> ", song)
                print("artist--> ", artist)
                file_id="angry_all/"+filename
                conn.execute("""INSERT INTO angry_all(f_name, a_name, title) VALUES( ?, ?, ? ) """, (file_id, artist, song))
                conn.commit()
                count=count+1
        else:
            #print("no-tags-->" , filename)
            print("------")
        print("------------------------------------------------------\n")
conn.commit()
print("done--> ", count)