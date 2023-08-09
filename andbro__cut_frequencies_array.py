#!/usr/bin/python
#
# description
#
# by AndBro @2022
# __________________________


'''

VARIABLES:
 - arr:     array
 - freqs:   frequencies
 - fmin:    minimum frequency
 - fmax:    maximum frequency

DEPENDENCIES:
 - None
 
OUTPUT:
 - array
 - frequencies
 
EXAMPLE:
>>> __cut_frequencies_array(arr, freqs, fmin, fmax)

'''

def __cut_frequencies_array(arr, freqs, fmin, fmax):

    ind = []
    for i, f in enumerate(freqs):
        if f >= fmin and f <= fmax:
            ind.append(i)

    ff = freqs[ind[0]:ind[-1]]
    pp = arr[:,ind[0]:ind[-1]]
    
    return pp, ff 

## End of File
