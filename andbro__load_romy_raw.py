#!/usr/bin/python
#
# description
#
# by AndBro @2023
# __________________________

def __load_romy_raw(seed, starttime, endtime):

    '''

    VARIABLES:
     - seed_id      code of seismic stations (e.g. "BW.DROMY..FJU")
     - starttime    start date (str / UTCDateTime object)
     - endtime      end date (str / UTCDateTime object)
     
    DEPENDENCIES:
     - import obspy
     - import io
     - from pandas import date_range

    OUTPUT:
     - st           stream object
     
    EXAMPLE:
    >>> __load_romy_raw("BW.DROMY..FJZ", starttime, endtime)

    '''

    import obspy
    import io
    from pandas import date_range
    
    tbeg = obspy.UTCDateTime(starttime)
    tend = obspy.UTCDateTime(endtime)

    net, sta, loc, cha = seed.split(".")
    
    reclen = 512
    chunksize = 100000 * reclen # Around 50 MB
    
    st0 = obspy.Stream()
        
    for dt in date_range(tbeg.date, tend.date):
    
        doy = UTCDateTime(dt).julday
        year = UTCDateTime(dt).year
    
        path = f"/import/freenas-ffb-01-data/romy_archive/{year}/{net}/{sta}/{cha}.D/"

        with io.open(path+f"{net}.{sta}.{loc}.{cha}.D.{year}.{doy}", "rb") as fh:
            while True:
                with io.BytesIO() as buf:
                    c = fh.read(chunksize);
                    if not c:
                        break
                    buf.write(c);
                    buf.seek(0, 0);
                    st = obspy.read(buf);
        st0 += st
    
    st0.merge()
    
    return st0 




## End of File
