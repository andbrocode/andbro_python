#!/bin/python

import obspy
import sys

def __get_data_archive(seed_id='BW.ROMY..BJU', beg='2020-07-17 00:00', end='2020-07-17 02:00', raw=None):

	''' get data of ROMY for one component from archive 

	seed_id:    code of network, sta, location and channel
	beg:	    begin of time period
	end:        end of time period

	dependency: - obspy

	>>> __get_data_archive(seed_id='BW.ROMY..BJU', beg='2020-07-17 00:00', end='2020-07-17 02:00', raw=None)

	'''

	from obspy import UTCDateTime, read_inventory
	
	# process input 
	net, sta, loc, cha = seed_id.split(".")

	beg = UTCDateTime(beg)
	end = UTCDateTime(end)
	
	## defining parameters
	year = beg.year
	doy  = beg.julday
	
	if doy < 10:
		doy = f"00{doy}"
	elif doy >= 10 and doy < 100:
		doy = f"0{doy}"

	## set sta accordingly
	if raw is True or sta == "DROMY": 
		sta = 'DROMY'
		loc = ''


	from obspy.clients.fdsn import Client, RoutingClient


	try:
		inv = read_inventory()
	except:
		print("no inventory read")
		inv = []
	
#	inv = RoutingClient("eida-routing").get_stations(network=seed_id[0], station=seed_id[1], starttime=beg, endtime=end, level= "response")
	
	print(inv)

	## define local data path
	path = f"/import/freenas-ffb-01-data/romy_archive/{year}/BW/{sta}/"
	


	if cha[2] == 'Z' and loc == "" and not cha[0] == "B":
		name = f'{cha}.D/{net}.{sta}.10.{cha}.D.{year}.{doy}'

		st = obspy.read(path+name, starttime=beg, endtime=end)

	elif cha[2] in {'Z','U','V','W'}:
		name = f'{cha}.D/BW.{sta}.{loc}.{cha}.D.{year}.{doy}'

		st = obspy.read(path+name, starttime=beg, endtime=end)

	elif cha in {'F1V', 'F2V'}:
		#path = '/bay200/mseed_online/archive/2020/BW'
		name = f'{cha}.D/BW.{sta}.{loc}.{cha}.D.{year}.{doy}'

		print(path+name)
		
		st = obspy.read(path+name, starttime=beg, endtime=end)       

	else: 
		print("No correct setting found! Abort!")
		sys.exit()

	return st, inv
	
## END OF FILE
