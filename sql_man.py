import os
import sys
import string
import sqlite3



outputf = "output.db"
conn = sqlite3.connect(outputf)
#qo = "Select acousticness, spot_id from lyset31 where acousticness like '%e%'"
res = conn.execute(qo)
kw = res.fetchall()
j=0
for k in range(len(kw)):
    acou=kw[k][0]
    acou_p="{:.8f}".format(float(acou))
    spot_id=kw[k][1]
    print("acou--> " , acou_p)
    #conn.execute(""" UPDATE lyset31 set acousticness= ? where spot_id= ? """, (acou_p,spot_id))
    #conn.commit()

#conn.commit()
print("k---- ", k+1)