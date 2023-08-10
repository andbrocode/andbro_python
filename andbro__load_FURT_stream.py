#!/bin/python3

def __load_furt_stream(config, show_raw=False, path_to_archive = '/bay200/gif_online/FURT/WETTER/'):
    
    '''
    Load a selection of data of FURT weather station for certain times and return an obspy stream
    
    
    PARAMETERS:
        - config:    configuration dictionary
        - show_raw:  bool (True/False) -> shows raw data FURT head


    RETURN:
        - stream
        
    '''
    
    from pathlib import Path
    from obspy import UTCDateTime
    from tqdm.notebook import tqdm_notebook
    from numpy import arange
    from obspy import Stream
    from pandas import concat, to_datetime, read_csv, DataFrame
    
    def __add_trace(cha, tbeg, dat, dt=1):

        from obspy import Trace, UTCDateTime
        from numpy import array

        tr = Trace()
        tr.stats.station = 'FURT'
        tr.stats.network = 'BW'
        tr.stats.channel = str(cha)
        tr.stats.sampling_rate = 1/dt
        tr.stats.starttime = UTCDateTime(tbeg)
        tr.data = array(dat)

        return tr
    
    
    def __resample(df, freq='1S'):

        ## make column with datetime
        df['datetime'] = df['date'].astype(str).str.rjust(6,"0")+" "+df['time'].astype(str).str.rjust(6,"0")

        ## drop datetime duplicates
        df = df[df.duplicated("datetime", keep="first") != True]

        ## convert to pandas datetime object
        df['datetime'] = to_datetime(df['datetime'], format="%d%m%y %H%M%S", errors="coerce")

        ## set datetime column as index
        df.set_index('datetime', inplace=True)

        ## remove duplicates
        df = df[~df.index.duplicated()]

        ## resample
        df = df.asfreq(freq=freq)

        return df 
    

    
    config['tbeg'] = UTCDateTime(config['tbeg'])
    config['tend'] = UTCDateTime(config['tend'])
    
    output_text = []
    
    new_delta = 10
    
    if not Path(path_to_archive).exists():
        output_text.append(f"  -> Path: {path_to_archive}, does not exists!")
#         print(f"  -> Path: {path_to_archive}, does not exists!")
        return    
    
    
    ## list of parameters requried in configurations
    params = ['tbeg', 'tend']
    for param in params:
        if not param in config.keys():
            output_text.append(f"ERROR: {param} not in config but required!")
#             print(f"ERROR: {param} not in config but required!")
            return
    
    
    ## declare empyt dataframe
    df = DataFrame()
    
    for i, date in enumerate(arange(config['tbeg'].date, (config['tend']+86410).date)):
        
        date = UTCDateTime(str(date)).date
        filename = f'FURT.WSX.D.{str(date.day).rjust(2,"0")}{str(date.month).rjust(2,"0")}{str(date.year).rjust(2,"0")[-2:]}.0000'
        
#         print(f'   reading {filename} ...')

        try:
            if show_raw:
                df0 = read_csv(path_to_archive+filename)            
                print(df0.columns.tolist())
                return
            else:
                df0 = read_csv(path_to_archive+filename, usecols=[0,1,10,12,13,14], names=['date', 'time', 'T', 'H', 'P','Rc'])            
            
            ## substitute strings with floats
            df0['T']  = df0['T'].str.split("=", expand=True)[1].str.split("C", expand=True)[0].astype(float)
            df0['P']  = df0['P'].str.split("=", expand=True)[1].str.split("H", expand=True)[0].astype(float)
            df0['H']  = df0['H'].str.split("=", expand=True)[1].str.split("P", expand=True)[0].astype(float)
            df0['Rc'] = df0['Rc'].str.split("=", expand=True)[1].str.split("M", expand=True)[0].astype(float)
           
            
            ## replace error indicating values (-9999, 999.9) with NaN values
#             df0.replace(to_replace=-9999, value=nan, inplace=True)
#             df0.replace(to_replace=999.9, value=nan, inplace=True)
            
            
            if df.empty:
                df = df0
            else: 
                df = concat([df, df0])
        except:
            output_text.append(f"  -> File: {filename}, does not exists!")
#             print(f"  -> File: {filename}, does not exists!")
   
    ## reset the index for the joined frame
    df.reset_index(inplace=True, drop=True)

    
    ## resample dataframe and avoid data gaps
    df = __resample(df, freq=f'{new_delta}S')

    
    for text in output_text:
        print(text)    

    df_starttime = UTCDateTime(df.index[0])
    
    ## create stream and attach traces
    st0 = Stream()
    st0 += __add_trace("LAT", df_starttime, df['T'], dt=new_delta)
    st0 += __add_trace("LAP", df_starttime, df['P'], dt=new_delta)
    st0 += __add_trace("LAH", df_starttime, df['H'], dt=new_delta)
    st0 += __add_trace("LAR", df_starttime, df['Rc'], dt=new_delta)
        
    ## trim to specfied time period
    st0.trim(config['tbeg'], config['tend'])
        
    print(f"Specified end: {config['tend']} \nTrace end:     {st0.select(channel='LAT')[0].stats.endtime}")
    
    return st0

## END OF FILE
