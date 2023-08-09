#!/bin/python3

def __load_wromy_stream(path_to_sds, seed_id, tbeg, tend):
    
    '''
    
    reads WROMY data from tbeg to tend
    
    >>> __load_wromy_stream(path_to_sds, seed_id, tbeg, tend)
    
    '''

    from os.path import exists
    from pandas import date_range, read_csv, concat, DataFrame
    from tqdm.notebook import tqdm_notebook
    from obspy import Stream, UTCDateTime
    from numpy import nan, inf
    
    def __add_trace(seed_id, ch, tbeg, dat):

        from obspy import Trace, UTCDateTime
        from numpy import array
        from numpy.ma import masked_invalid

        net, sta, loc, cha = seed_id.split(".")

        tr = Trace()
        tr.stats.network = net
        tr.stats.station = 'WROMY'
        tr.stats.location = cha
        tr.stats.channel = str(ch)
        tr.stats.sampling_rate = 1.0
        tr.stats.starttime = UTCDateTime(tbeg)
        tr.data = masked_invalid(array(dat))

        return tr
    
    
    t1 = tbeg
    t2 = tend + 86410
    
    net, sta, loc, cha = seed_id.split(".")
    
    df = DataFrame()
    
    for n, date in enumerate(tqdm_notebook(date_range(t1.date, t2.date))):    
        doy = str(date.timetuple().tm_yday).rjust(3,"0")
        
#        path = f"/import/freenas-ffb-01-data/romy_archive/{date.year}/{net}/{sta}/{cha}.D/"
        path = f"{path_to_sds}{date.year}/{net}/{sta}/{cha}.D/"
        
        if not exists(path):
            print(f"Path: {path}, does not exists!")
            return

    
        fileName = f"BW.WROMY.{cha}.D.{date.year}.{doy}"

#         print(f'   reading {fileName} ...')

        try:
            df0 = read_csv(path+fileName)
            
            ## replace error indicating values (-9999, 999.9) with NaN values
            df0.replace(to_replace=-9999, value=nan, inplace=True)
            df0.replace(to_replace=999.9, value=nan, inplace=True)
            df0.replace(to_replace=inf, value=nan, inplace=True)
              
#             ## change time from in to 6 character string
            df0.iloc[:,2] = [str(ttt).rjust(6,"0") for ttt in df0.iloc[:,2]]
          
            if n == 1:
                df = df0
            else: 
                df = concat([df,df0])
        except:
            print(f"File: {fileName}, does not exists!")
       

    
    df.reset_index(inplace=True, drop=True)
    
    df_starttime = UTCDateTime(f"{df['Date'][0]} {df['Time (UTC)'][0]}")
    
    
    ## add columns with total seconds
    if 'Seconds' in df.columns:
        totalSeconds = df.Seconds + (df.Date - df.Date.iloc[0]) * 86400
        df['totalSeconds'] = totalSeconds
    
    st0 = Stream()
    st0 += __add_trace(seed_id, "LAT", df_starttime, df['Temperature (°C)'])
    st0 += __add_trace(seed_id, "LAP", df_starttime, df['Pressure (hPa)'])
    st0 += __add_trace(seed_id, "LAH", df_starttime, df['rel. Humidity (%)'])
        
        
    st0.trim(tbeg, tend)
    
    if len(st0) > 3:
        print(" -> split, interpolate, merge ...")
        st0.split().merge(fill_value="interpolate")

    
    print(f"Specified end: {tend} \nTrace end:     {st0.select(channel='LAT')[0].stats.endtime}")
    
    return st0

## END OF FILE
