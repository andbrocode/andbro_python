#!/bin/python 



def __filter_traces(st_in,f,detrend=None):

	'''
	filter the input traces with corner frequencies f, being either a float or list. 

	__filter_traces(st_in,f, detrend=None)

	st_in:   obspy stream
	f:       float or list (e.g. 0.1 ; [0.1,1.0] )
	'''

	from numpy import arange

	## extrac data object from stream
	traces = st_in[0]

	## create a time array
	timeline = arange(0, traces.stats.npts / traces.stats.sampling_rate, traces.stats.delta)

	## demean and detrend data 
	if detrend is not None:
		traces.detrend('linear')
		print('detrend applied')

	## normalizing traces 
	traces.data = traces.data/max(abs(traces.data)) 

	## actual filtering
	if type(f) is float:
		print('lowpass applied\n')
		traces.filter('lowpass',freq=f, corners=2, zerophase=True)
	elif type(f) is list:
		print('bandpass applied\n')
		traces.filter('bandpass',freqmin=f[0],freqmax=f[1], corners=2, zerophase=True)

	## overwrite the former data trace with the filtered one
	st_in[0] = traces 

	return st_in
