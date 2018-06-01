import os
import sys
import string
import sqlite3



outputf = "output.db"
conn = sqlite3.connect(outputf)
qo = "Select mxm_tid from lyset31"
res = conn.execute(qo)
kw = res.fetchall()
j=0
for k in range(len(kw)):
    mxm_tid=kw[k][0]
    print("mxm--> " , mxm_tid)
    #conn.execute(""" UPDATE lyset31 set mood= (select mood from lyset31_lab where mxm_tid= ? ) where mxm_tid= ? """, (mxm_tid,mxm_tid))
    conn.commit()

conn.commit()
print("k---- ", k+1)