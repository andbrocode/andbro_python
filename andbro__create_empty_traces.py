#!/bin/python

from numpy import isnan, ones, nan, empty

def __create_empty_traces(st, config):
    ''' 
    creates empty traces with essential meta data for missing traces in stream

    from numpy import isnan, ones, nan, empty

    ''' 

    missing = [i for i, tr in enumerate(st) if tr.stats.npts == 0]
    full  = [i for i, tr in enumerate(st) if tr.stats.npts > 0]

    if len(full) == 0:
        print("All traces are empty! Aborting..."); return

    if len(missing) != 0:
        for k in missing:
            dummy_data = empty(st[full[0]].stats.npts)
            dummy_data[:] = nan
            st[k].data = dummy_data
            st[k].stats.sampling_rate = st[full[0]].stats.sampling_rate
            st[k].stats.starttime = st[full[0]].stats.starttime
            if config.seeds:
                st[k].stats.network, st[k].stats.station, st[k].stats.location, st[k].stats.channel = config.seeds[k].split(".")

      
## END OF FILE
