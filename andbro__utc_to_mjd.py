#!/usr/bin/python
#
#  convert utc datetime to mjd number
#
# by AndBro @2023
# __________________________


def __utc_to_mjd(datetime):

    '''
    VARIABLES:
     - datetime         date time as obspy.UTCDateTime or as str or list

    DEPENDENCIES:
    -   from obspy import UTCDateTime
    -   from astropy.time import Time

    OUTPUT:
     - mjd              float or list of floats
     
    EXAMPLE:
    >>> __utc_to_mjd("2023-02-06 00:00")

    '''
    
    from obspy import UTCDateTime
    from astropy.time import Time

    if str(type(datetime)) == "<class 'list'>":
        mjd = [Time(str(UTCDateTime(dt)), format='isot', scale='utc').mjd for dt in datetime]
    else:
        mjd = Time(str(UTCDateTime(datetime)), format='isot', scale='utc').mjd
     
    return mjd


## End of File
