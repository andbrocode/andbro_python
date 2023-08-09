#!/usr/bin/python
#
# read mseed data from SDS type filesystem  
#
# by AndBro @2023
# __________________________


def __read_sds(path_to_archive, seed, tbeg, tend, data_format="MSEED"):

    '''
    VARIABLES:
     - path_to_archive
     - seed
     - tbeg, tend
     - data_format

    DEPENDENCIES:
     - from obspy.core import UTCDateTime
     - from obspy.clients.filesystem.sds import Client

    OUTPUT:
     - stream
     
    EXAMPLE:
    >>> st = __read_sds(path_to_archive, seed, tbeg, tend, data_format="MSEED")

    '''    
	
    from obspy.core import UTCDateTime
    from obspy.clients.filesystem.sds import Client
    
    tbeg, tend = UTCDateTime(tbeg), UTCDateTime(tend)
    
    ## separate seed id
    net, sta, loc, cha = seed.split(".")
    
    ## define SDS client
    client = Client(path_to_archive, sds_type='D', format=data_format)
        
    ## read waveforms
    st = client.get_waveforms(net, sta, loc, cha, tbeg, tend, merge=-1)

    return st


## End of File
