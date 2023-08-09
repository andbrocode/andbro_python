#!/usr/bin/python
#
# enable logging via print in python script
#
# by AndBro @2022
# __________________________


''' redirect print commands to log-file

VARIABLES:
	logpath:    path to log-file
	logname:    name of log-file


DEPENDENCIES:
	import obspy

OUTPUT:

EXAMPLE:
>>> __get_stream_data_archive('BW.ROMY.10.BJZ', '2020-07-17 02:50', 3600, raw=False)

'''

def __logging_setup(logpath, logfile):

#	import logging, sys

#	logging.basicConfig(filename=f'{logpath}{logfile}', level=logging.DEBUG)
#	logger = logging.getLogger()
#	sys.stderr.write = logger.error
#	sys.stdout.write = logger.info


    import logging
    
    logging.basicConfig(filename=f'{logpath}{logfile}', filemode='w', format='%(asctime)s, %(levelname)s, %(message)s')


## End of File
