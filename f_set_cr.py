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
    qo = "Select stem from stemmap4"
    res = conn.execute(qo)
    tmpwords = res.fetchall()
    # assert len(tmpwords) == len(topwords), 'Number of words issue.'
    j = 0
    m = 0

    for k in range(len(tmpwords)):
        tempo = tmpwords[k][0]
        # create tables -> f_set01
        q = "ALTER TABLE dsetlow3 ADD COLUMN ["+tempo+"] INT"
        print("0")
        conn.execute(q)
        j=j+1
    conn.commit()

    print( "total words found.", (k+1))
    print("total fields added.",  (j))
    conn.close()