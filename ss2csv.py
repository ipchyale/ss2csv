import pandas as pd
import numpy as np
import sys
import os

def file2table(f):
    with open(f,'r') as colorfile:
        l = colorfile.readlines()

    hunt = False
    collist = []
    for item in l:
        if hunt==True:
            if 'END_DATA_FORMAT' in item:
                break
            else:
                collist.append(item)

        if 'BEGIN_DATA_FORMAT' in item:
            hunt = True

    cols = collist[0].split('\t')
    cols = [item.rstrip('\n') for item in cols]

    hunt = False
    vallists = []
    for item in l:
        if hunt==True:
            if item=='END_DATA\n':
                vallists.append(vallist)
                hunt = False
            else:
                vallist.append(item)

        if item=='BEGIN_DATA\n':
            hunt = True
            vallist = []

    rowlist = []
    for i,vallist in enumerate(vallists):
            l = [item.rstrip('\n').split('\t') for item in vallist]
            l = [item for sublist in l for item in sublist]

            n = len([item for item in l if item!=''])
            if n==78:
                rowlist.append([item for item in l if item!=''])
            else:
                print('bad row',n)

    sf = pd.DataFrame(rowlist,columns=cols)

    return sf,lens

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
