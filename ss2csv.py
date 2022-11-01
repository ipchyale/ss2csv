import pandas as pd
import numpy as np
import sys
import os

def file2table(f):
    with open(f,'r') as colorfile:
        l = colorfile.readlines()

    # all column strings are identical, so we just grab the first
    for i,item in enumerate(l):
        if 'BEGIN_DATA_FORMAT' in item:
            colstring = l[i+1]
            break

    cols = [item.rstrip('\n') for item in colstring.split('\t')]
    cols = [item for item in cols if item!='']
    ncols = len(cols)

    # we hunt for data between the 'BEGIN' and 'END' flags
    hunt = False
    vallists = []
    for item in l:
        if hunt==True:
            if 'END_DATA\n' in item:
                vallists.append(vallist)
                hunt = False
            else:
                vallist.append(item)

        if 'BEGIN_DATA\n' in item:
            hunt = True
            vallist = []

    """
    Sometimes, data from consecutive measurements will not be separated by
    the usual 'BEGIN_DATA' and 'END_DATA' flags. In such cases, the 'hunt' above
    will generate some data rows that are actually multiple rows stitched
    together. So, we look for those rows, and unstitch them.
    """

    rowlist = []
    for vallist in vallists:
        l = [item.rstrip('\n').split('\t') for item in vallist]
        l = [item for sublist in l for item in sublist] # flatten list of lists
        l = [item for item in l if item!='']
        n = len(l)

        if n == ncols: # the usual case
            rowlist.append(l)
        elif n % ncols == 0: # the stitched-together case
            for row in [l[i:i+ncols] for i in range(0,n,ncols)]:
                rowlist.append(row)
        else:
            print(os.path.basename(f),"row length {} not a multiple of ncols".format(n))

    sf = pd.DataFrame(rowlist,columns=cols)

    return sf

def cleancols(sf):
    assert len(sf['SPECTRAL_NM'].columns) == len(sf['SPECTRAL_VAL'].columns)

    # creates list ['nm380','nm390',...]
    newcols = ['nm' + item for item in sf['SPECTRAL_NM'].iloc[0]]

    # dataframe with all the spectral values and new column names from list above
    tmp = sf['SPECTRAL_VAL']
    tmp.columns = newcols

    # set new columns in sf using tmp
    sf[newcols] = tmp

    # removes the old columns
    trunccols = [item for item in sf.columns if item not in ['SPECTRAL_NM','SPECTRAL_VAL']]
    sf = sf[trunccols]

    return sf

def main():
    infile = sys.argv[1]

    try:
        outfile = sys.argv[2]
    except:
        outfile = os.path.splitext(infile)[0] + ".csv"

    sf = file2table(infile)
    sf = cleancols(sf)
    sf.to_csv(outfile,index=False)

if __name__ == "__main__":
    main()
