#!/usr/bin/python
#
# description
#
# by AndBro @2022
# __________________________



def __convert_to_stream(arr, starttime="1970-01-01 00:00:00", sampling_rate=1, seed="XX.Test..ccc"):
    
	'''

	VARIABLES:
	- arr:			data as numpy array 
	- seed:    		seed code of the data (e.g. "BW.ROMY..BJU")
	- startime:		startdate and time of the trace
	- sampling_rate:	sampling period (in seconds)

	DEPENDENCIES:
    	- from obspy import Stream, Trace, UTCDateTime
    	- from numpy import array

	OUTPUT:
	 - stream
	 
	EXAMPLE:
	>>> __convert_to_stream(etides.tiltN, starttime="2022-04-24 00:00", sampling_rate=600, seed="BW.etide..LHN")

	'''    

	from obspy import Stream, Trace, UTCDateTime
	from numpy import array

	## initalize
	st = Stream()
	tr = Trace()

	## set array data to trace
	tr.data = array(arr)

	## set starttime and sampling rate
	tr.stats.starttime = UTCDateTime(starttime)
	tr.stats.sampling_rate = sampling_rate

	## meta data
	tr.stats.network = seed.split(".")[0]
	tr.stats.station = seed.split(".")[1]
	tr.stats.location = seed.split(".")[2]    
	tr.stats.channel = seed.split(".")[3]

	st += tr

	return st

## End of File
