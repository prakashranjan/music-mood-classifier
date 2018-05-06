#!/usr/bin/env python


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
    trainf = "mxm_779k_matches.txt"

    outputf = "output.db"

    # sanity checks
    if not os.path.isfile(trainf):
        print('ERROR: %s does not exist.' % trainf)
        sys.exit(0)

    if not os.path.isfile(outputf):
        print('ERROR: %s does not exists.' % outputf)
        sys.exit(0)

    # open output SQLite file
    conn = sqlite3.connect(outputf)

    # create tables -> lymeta
    q = "CREATE TABLE lymeta (tid,"
    q += " artist_name_msd TEXT,"
    q += " title_msd TEXT,"
    q += " mxm_tid INT,"
    q += " artist_name_mxm TEXT,"
    q += " title_mxm TEXT)"
    conn.execute(q)

    # we put the msm_mxm_map data in the dataset
    f = open(trainf, 'r', encoding="utf8")
    cnt_lines = 0
    for line in f:
        if line == '' or line.strip() == '':
            continue
        if line[0] in ('#', '%'):
            continue
        lineparts = line.strip().split('<SEP>')
        tid = lineparts[0]
        a_name_msd = lineparts[1]
        title_msd = lineparts[2]
        mxm_tid = lineparts[3]
        a_name_mxm = lineparts[4]
        title_mxm = lineparts[5]

        print("\n--->tid: ",tid)
        print("\n--->a_name_msd :", a_name_msd)
        print("\n--->title_msd: ", title_msd)
        print("\n--->mxm_tid: ", mxm_tid)
        print("\n--->a_name_mxm: ", a_name_mxm)
        print("\n--->title_mxm: ", title_mxm)

        conn.execute("""INSERT INTO lymeta( tid, artist_name_msd, title_msd, mxm_tid, artist_name_mxm, title_mxm)
                         VALUES(?,?,?,?,?,? )""",(tid, a_name_msd, title_msd, mxm_tid,a_name_mxm,title_mxm))

        # verbose
        cnt_lines += 1
        if cnt_lines % 15000 == 0:
            print('Done with %d train tracks.' % cnt_lines)
            conn.commit()

    f.close()
    conn.commit()
    print( "total ? mxm map added.", cnt_lines)



    # create indices
    q = "CREATE INDEX idx_lymeta1 ON lymeta ('tid')"
    conn.execute(q)
    q = "CREATE INDEX idx_lymeta2 ON lymeta ('artist_name_msd')"
    conn.execute(q)
    q = "CREATE INDEX idx_lymeta3 ON lymeta ('title_msd')"
    conn.execute(q)
    q = "CREATE INDEX idx_lymeta4 ON lymeta ('mxm_tid')"
    conn.execute(q)
    q = "CREATE INDEX idx_lymeta5 ON lymeta ('artist_name_mxm')"
    conn.execute(q)
    q = "CREATE INDEX idx_lymeta6 ON lymeta ('title_mxm')"
    conn.execute(q)
    conn.commit()
    print('mapping Indices created.')

    # close output SQLite connection
    conn.close()