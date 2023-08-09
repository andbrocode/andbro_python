#!/usr/bin/python
#
#  get mean amplitudes of a signal
#
# by AndBro @2022
# __________________________


''' get data of ROMY for one component from archive 

VARIABLES:
 - signal:    signal as array
 - deltaN:    samples to consider

DEPENDENCIES:
 - import numpy

OUTPUT:
 - amplitudes
 - mean
 - standard deviation
 
EXAMPLE:
>>> __get_mean_amplitude(signal, deltaN=100)

'''

def __get_mean_amplitude(signal, deltaN=100):

    from numpy import nanmean, nanstd
    
    n1, n2, amplitudes = 0, deltaN, []
    
    while n2 < len(signal):

        amplitudes.append(max(signal[n1:n2])-min(signal[n1:n2]))

        n1 += deltaN
        n2 += deltaN
        
    return amplitudes, nanmean(amplitudes), nanstd(amplitudes)

## End of File
