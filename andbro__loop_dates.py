#!/usr/bin/python
#
# loop over a date range with certain time interval and time overlap
#
# by AndBro @2023
# __________________________


def __loop_dates(dat1, date2):

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
	>>> __loop_dates(dat1, date2)

	'''

	from pandas import date_range

	config['time_interval'] = 3600 ## in seconds
	config['time_overlap'] = 600 ## seconds

	date1, date2 = "2022-10-01", "2022-10-10"


	for date in date_range(date1, date2):
	    date = obs.UTCDateTime(obs.UTCDateTime(date).date)

	    hh = 0
	    while hh <= 86400: 
		
		tbeg = date - config['time_overlap']
		tend = date + config['time_overlap'] + hh
		
		print(tbeg, tend)
		## DO STUFF
		
		hh += config['time_interval']
		       


## End of File
