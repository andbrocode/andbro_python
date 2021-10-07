#!/bin/python

def __get_data_george(component,resolution,beg,duration):

	''' 
	get data of ROMY for one component from server george (http://george) via fdsn service 

	__get_stream_data_george(component,resolution,beg,duration)

	component:  U, V, W, Z, F1, F2
	resolution: B (=20Hz) or H (=200Hz)
	beg:	    begin of time period
	duration:   temporal length of period
	
	dependencies: 
		- import obspy
		
	>>> __get_data_george('Z', 'B', '2020-07-17 02:50', 3600)

	'''

	from obspy.clients.fdsn import Client

	cha = '{}J{}'.format(resolution,component)
	end = beg + duration

	waveform_client = Client(base_url='http://george', timeout=200)


	if component == 'Z':
		st = waveform_client.get_waveforms(location='10', channel=cha, network='BW', station='ROMY', starttime=beg, endtime=end, attach_response=True)
		return st

	elif component in ['U', 'V', 'W']:
		st = waveform_client.get_waveforms(location='', channel=cha, network='BW', station='ROMY', starttime=beg, endtime=end, attach_response=True)
		return st

	elif component in {'F1', 'F2'}:
		cha=f"{component}V"
		st = waveform_client.get_waveforms(location="", channel=cha, network='BW', station='ROMY', starttime=beg, endtime=end, attach_response=True)
		return st

	else:
		print('This component is unkown! Enter Z , U , V, W or F1, F2 !!!')


