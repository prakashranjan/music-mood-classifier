import os
import sys
import sqlite3



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
    #trainf = "mxm_779k_matches.txt"

    outputf = "output.db"

    # sanity checks
    #if not os.path.isfile(trainf):
        #print('ERROR: %s does not exist.' % trainf)
        #sys.exit(0)

    if not os.path.isfile(outputf):
        print('ERROR: %s does not exists.' % outputf)
        sys.exit(0)

    # open output SQLite file
    conn = sqlite3.connect(outputf)
    qo = "Select stem from stemmap4 order by stem"
    res = conn.execute(qo)
    tmpwords = res.fetchall()
    qo2 = "Select mxm_tid from dsetlow3"
    res2 = conn.execute(qo2)
    mxid = res2.fetchall()
    # assert len(tmpwords) == len(topwords), 'Number of words issue.'
    j = 0
    m = 0


    for k in range(len(mxid)):
        mx = mxid[k][0]
        ylo=0
        for l in range(len(tmpwords)):
            tempo=tmpwords[l][0]

            res3 = conn.execute("""Select [count] from lyrics where mxm_tid= ? and word= ? """, (mx,tempo))
            coun = res3.fetchall()
            if len(coun)==0:
                ylo=ylo+1
                conn.execute("update dsetlow3 set ["+tempo+"]=0 where mxm_tid= "+str(mx))
            else:
                cn=coun[0][0]
                print("--->",str(cn))
                #print("--->",str(mx))
                #cn=7
                conn.execute("update dsetlow3 set ["+tempo+"] = "+str(cn)+" where mxm_tid= "+str(mx))
                #print("update fsetlow set ["+tempo+"] = "+str(cn)+" where mxm_tid= "+str(mx))

        print("---"+str(ylo))
        if(ylo==599):
            print(mx)
            conn.execute("delete from dsetlow3 where mxm_tid= " + str(mx))


        conn.commit()
        print(" %d rows complete." % (k + 1))




    conn.commit()

    print( "total rows complete:" , k+1)

    conn.close()