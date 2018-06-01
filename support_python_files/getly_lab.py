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
    outputf = "output.db"
    conn = sqlite3.connect(outputf)
    qo = "Select a_name, title, f_name from relax_all where lyrics is null "
    res = conn.execute(qo)
    kw = res.fetchall()
    j=0
    for k in range(len(kw)):
        aname=kw[k][0]
        titlen=kw[k][1]
        mxid=kw[k][2]

        try:
            inly_ly=PyLyrics.getLyrics(aname, titlen)
        except:
            inly_ly=''

        if inly_ly:
            inly = inly_ly
            inly = inly.replace('\n', ' ')
            # print(inly)

            #conn.execute(""" UPDATE relax_all set lyrics = ? where f_name= ? """, (inly, mxid))
            print("ok--", mxid)
            j = j + 1
            conn.commit()


        else:
            print("---------------non lyrics-----", mxid)


    print("all done success-->", k + 1)
    print("success-->", j)
    print("failed-->", (k + 1)-j)
    conn.commit()