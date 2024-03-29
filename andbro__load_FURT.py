#!/bin/python3

def __load_furt(config, show_raw=False, path_to_archive = '/bay200/gif_online/FURT/WETTER/'):
    '''
    Load a selection of data of FURT weather station for time period
    
    
    PARAMETERS:
        - config:            configuration dictionary
        - show_raw:          bool (True/False) -> shows raw data FURT head
        - path_to_archive:   path to FURT data

    RETURN:
        - dataframe
        
    '''
    
    from pathlib import Path
    from obspy import UTCDateTime
    from tqdm.notebook import tqdm_notebook
    
    config['tbeg'] = UTCDateTime(config['tbeg'])
    config['tend'] = UTCDateTime(config['tend'])
    
    output_text = []

        
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
    df = pd.DataFrame()
    
    for i, date in enumerate(tqdm_notebook(np.arange(config['tbeg'].date, (config['tend']+86400).date))):
        
        date = UTCDateTime(str(date)).date
        filename = f'FURT.WSX.D.{str(date.day).rjust(2,"0")}{str(date.month).rjust(2,"0")}{str(date.year).rjust(2,"0")[-2:]}.0000'
        
#         print(f'   reading {filename} ...')

        try:
            if show_raw:
                df0 = pd.read_csv(path_to_archive+filename)            
                print(df0.columns.tolist())
                return
            else:
                df0 = pd.read_csv(path_to_archive+filename, usecols=[0,1,10,12,13,14], names=['date', 'time', 'T', 'H', 'P','Rc'])            
            
            ## substitute strings with floats
            df0['T']  = df0['T'].str.split("=", expand=True)[1].str.split("C", expand=True)[0].astype(float)
            df0['P']  = df0['P'].str.split("=", expand=True)[1].str.split("H", expand=True)[0].astype(float)
            df0['H']  = df0['H'].str.split("=", expand=True)[1].str.split("P", expand=True)[0].astype(float)
            df0['Rc'] = df0['Rc'].str.split("=", expand=True)[1].str.split("M", expand=True)[0].astype(float)
           
            
            ## replace error indicating values (-9999, 999.9) with NaN values
            df0.replace(to_replace=-9999, value=nan, inplace=True)
            df0.replace(to_replace=999.9, value=nan, inplace=True)
            
            
            if df.empty:
                df = df0
            else: 
                df = pd.concat([df, df0])
        except:
            output_text.append(f"  -> File: {filename}, does not exists!")
#             print(f"  -> File: {filename}, does not exists!")
   
    df.reset_index(inplace=True, drop=True)
        
    for text in output_text:
        print(text)
        
    return df

## END OF FILE
