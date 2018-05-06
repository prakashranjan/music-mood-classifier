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
    trainf = "mxm_reverse_mapping.txt"

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

    # create tables -> stemmap
    q = "CREATE TABLE stemmap (stem TEXT,"
    q += " word TEXT)"
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
        stem = lineparts[0]
        wordo = lineparts[1]

        print("\n--->stem: ",stem)
        print("\n--->word :", wordo)

        conn.execute("""INSERT INTO stemmap( stem, word)
                         VALUES(?,?)""",(stem, wordo))

        # verbose
        cnt_lines += 1
        if cnt_lines % 150 == 0:
            print('Done with %d words.' % cnt_lines)
            conn.commit()

    f.close()
    conn.commit()
    print( 'total %d stem map words added.', cnt_lines)



    # create indices
    q = "CREATE INDEX idx_stemmap1 ON stemmap ('stem')"
    conn.execute(q)
    q = "CREATE INDEX idx_stemmap2 ON stemmap ('word')"
    conn.execute(q)

    conn.commit()
    print('stem mapping Indices created.')

    # close output SQLite connection
    conn.close()