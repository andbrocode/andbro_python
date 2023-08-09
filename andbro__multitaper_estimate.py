#!/usr/bin/python
#
# description
#
# by AndBro @2022
# __________________________


'''

>>> __multitaper_estimate(data, fs, n_windows=4, one_sided=True)

VARIABLES:
 - data:       array with data
 - fs:         sampling rate
 - n_windows:  amount of taper windows
 - one_sided:  one_sided spectrum or not

DEPENDENCIES:
 from spectrum import dpss, pmtm
 from numpy import zeros, arange, linspace

OUTPUT:
 - frequencies
 - estimate
 
'''

def __multitaper_estimate(data, fs, n_windows=4, one_sided=True):

    from spectrum import dpss, pmtm
    from numpy import zeros, arange, linspace
    
    
    NN = len(data)
    
    ## Option 1
    #[tapers, eigen] = dpss(NN, 2.5, n_windows)
    # spectra, weights, eigenvalues = pmtm(data, e=tapers, v=eigen, show=True)

    ## Option 2
    # res = pmtm(data, NW=2.5, show=False)
    spectra, weights, eigenvalues = pmtm(data, NW=2.5, k=n_windows, show=False)

    ## average spectra
    estimate = zeros(len(spectra[0]))
    for m in range(n_windows):
        estimate += (abs(spectra[m])**2)
    estimate /= n_windows
    
    l = len(estimate)
    frequencies = linspace(-0.5*fs, 0.5*fs, l)
    
    if one_sided:
        return  frequencies[int(l/2):], estimate[:int(l/2)]
    else:
        return frequencies, estimate


## End of File
