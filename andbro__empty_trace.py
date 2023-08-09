#!/bin/python



def __empty_trace(config, seed_id):
    ''' 
    creates an empty trace with essential meta data for missing traces in stream

    config['tbeg']      starttime
    config['tend']      endtime

    ''' 

    from numpy import zeros, nan
    from obspy import Trace

    tr = Trace()

    if seed_id.split(".")[3][0] == "B":
        tr.stats.sampling_rate = 20
    elif seed_id.split(".")[3][0] == "H":
        tr.stats.sampling_rate = 200
    else:
        sys.exit()

    tr.data = zeros(int((config['tend']-config['tbeg'])*tr.stats.sampling_rate)+1) * nan
    tr.stats.network  = seed_id.split(".")[0]
    tr.stats.station  = seed_id.split(".")[1]
    tr.stats.location = seed_id.split(".")[2]
    tr.stats.channel  = seed_id.split(".")[3]

    tr.stats.starttime = config['tbeg']

    return tr
      
## END OF FILE
