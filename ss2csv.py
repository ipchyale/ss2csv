import pandas as pd
import numpy as np
import sys
import os

try:
    infile = sys.argv[1]

    try:
        outfile = sys.argv[2]
    except:
        outfile = os.path.splitext(infile)[0] + ".csv"

    sf = file2table(infile)

    assert len(sf['SPECTRAL_NM']) == len(sf['SPECTRAL_VAL'])
    newcols = ['nm' + item for item in sf['SPECTRAL_NM'].iloc[0]]
    tmp = sf['SPECTRAL_VAL']
    tmp.columns = newcols
    sf[newcols] = tmp
    trunccols = [item for item in sf.columns if item not in ['SPECTRAL_NM','SPECTRAL_VAL']]
    sf = sf[trunccols]

    sf.to_csv(outfile,index=False)

except:
    pass

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
    sf = pd.DataFrame(columns=cols)

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

    for i,vallist in enumerate(vallists):
            l = [item.rstrip('\n').split('\t') for item in vallist]
            l = [item for sublist in l for item in sublist]

            try:
                sf.loc[i] = [item for item in l if item!='']
            except:
                print('bad row')

    return sf
