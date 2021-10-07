#!/usr/bin/python3


def __get_mseed(seed_id, starttime, endtime, repository='online', raw=None, restitute=None):
	"""

	dependencies: 
	- import os, sys
	- from obspy import UTCDateTime
	- from andbro__get_data_archive import __get_data_archive
	- from andbro__querrySeismoData import __querrySeismoData

	>>> __get_mseed(seed_id, starttime, endtime, repository='online', raw=None, restitute=None)
	"""

	import os, sys
	from obspy import UTCDateTime
	from andbro__get_data_archive import __get_data_archive
	from andbro__querrySeismoData import __querrySeismoData


	starttime  = UTCDateTime(starttime)
	endtime    = UTCDateTime(endtime)
	path = os.getcwd()

	if repository == 'online':
		st, inv = __querrySeismoData(seed_id, starttime, endtime, True, None)
		print("Data retrieved using: __querrySeismoData")
		
	elif repository == 'archive':
		st, inv = __get_data_archive(seed_id, starttime, endtime, raw)
		print("Data retrieved using: __get_data_archive") 
		
	else:
		print("Define argument 'repository' as either: online or archive") 
		sys.exit()
		
	if restitute:
		#        pre_filt = [0.001, 0.005, 45, 50]
		pre_filter = [0.001, 0.005, 45, 50]
 
		out="VEL"  # "DISP" "ACC"

		st.remove_response(
		    inventory=inv, 
		    pre_filt=pre_filter,
		    output=out,
		)
		print(f"response function removed! output = {out}")

	st.write(f'{seed_id.split(".")[1]}_{seed_id.split(".")[3]}_{starttime.date}.mseed', format='MSEED') 
	print(f'stored data to:  {path}/{seed_id.split(".")[1]}_{seed_id.split(".")[3]}_{starttime.date}.mseed')

	if inv:
		inv.write(f'{seed_id.split(".")[1]}_{seed_id.split(".")[3]}.xml', format="STATIONXML") 
		print(f'stored inventory to:  {path}/{seed_id.split(".")[1]}_{seed_id.split(".")[3]}.xml')
		
# END OF FILE
