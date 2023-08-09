#!/usr/bin/python
#
# description
#
# by AndBro @2022
# __________________________


'''

VARIABLES:
 - df:    dataframe object
 - fmin:  minimum frequency
 - fmax:  maximum frequency
 
DEPENDENCIES:
 - None

OUTPUT:
 - dataframe
 
EXAMPLE:
>>> df = __cut_frequencies_dataframe(df, fmin, fmax)

'''

def __cut_frequencies_dataframe(df, fmin, fmax):

    ind = []
    for i,f in enumerate(df_psd['frequencies']):
        if f >= fmin and f <= fmax:
            ind.append(i)

    df0 = df.iloc[ind[0]:ind[-1],:]

    return df0

## End of File
