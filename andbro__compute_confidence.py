#!/usr/bin/python
#
# compute 95% confidence interval from array
#
# by AndBro @2023
# __________________________


def __compute_confidence(arr):

	'''

	VARIABLES:
	 - seed_id:    code of seismic stations (e.g. "BW.ROMY..BJU")
	 - tstart:	    begin of time period
	 - tdelta:     temporal length of period

	DEPENDENCIES:
	 - import obspy

	OUTPUT:
	 - test
	 
	EXAMPLE:
	>>> __get_stream_data_archive('BW.ROMY.10.BJZ', '2020-07-17 02:50', 3600, raw=False)

	'''

	from numpy import zeros, nanpercentile, shape

	percentiles_lower = zeros(shape(arr)[1])
	percentiles_upper = zeros(shape(arr)[1])

	for kk in range(shape(arr)[1]):
	out = nanpercentile(arr[:, kk],  [5, 95])
	percentiles_upper[kk] = out[1]
	percentiles_lower[kk] = out[0]

	return percentiles_lower, percentiles_upper


## End of File
