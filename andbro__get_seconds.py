#!/bin/python 

def __get_seconds(timestamp, mode="of_day"):
    
    '''
    get seconds of a DateTime 
    
    VARIABLES:
        
        mode:    reference: 'of_day', 'of year', 'total'

    DEPENDENCIES:
    
        from obspy import UTCDateTime

    OUTPUT:
    
        float: seconds 

    '''
    
    from obspy import UTCDateTime
    
    timestamp = UTCDateTime(timestamp)
    
    time_seconds = timestamp.hour*3600 + timestamp.minute*60 + timestamp.second + timestamp.microsecond*1e-6
    date_seconds = timestamp.julday * 86400 + time_seconds
    
    if mode == "of_day":
        return time_seconds
    
    elif mode == "of_year":
        return date_seconds
       
       
