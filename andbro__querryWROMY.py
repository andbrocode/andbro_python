#!/bin/python3
#
# @2022 AndBro


def __read_wromy_data(config):
    '''
    reads data from T1 to T2
    '''

    from pandas import date_range
    from tqdm.notebook import tqdm_notebook

    df = pd.DataFrame()
    
    for n, date in enumerate(tqdm_notebook(date_range(config['tbeg'].date, config['tend'].date))):    
        doy = str(date.timetuple().tm_yday).rjust(3,"0")
        
        path = f"{config['pathToData']}{date.year}/BW/WROMY/{config['channel']}.D/"

        if not Path(path).exists():
            __reply(f"Path: {path}, does not exists!")
            return

    
        fileName = f"BW.WROMY.{config['channel']}.D.{date.year}.{doy}"

#         print(f'   reading {fileName} ...')

        try:
            df0 = pd.read_csv(path+fileName)
            
            ## replace error indicating values (-9999, 999.9) with NaN values
            df0.replace(to_replace=-9999, value=nan, inplace=True)
            df0.replace(to_replace=999.9, value=nan, inplace=True)
              
#             ## change time from in to 6 character string
            df0.iloc[:,2] = [str(ttt).rjust(6,"0") for ttt in df0.iloc[:,2]]
          
            if n == 1:
                df = df0
            else: 
                df = pd.concat([df,df0])
        except:
            __reply(f"File: {fileName}, does not exists!")
       
    
    df.reset_index(inplace=True, drop=True)

    ## add columns with total seconds
    if 'Seconds' in df.columns:
        totalSeconds = df.Seconds + (df.Date - df.Date.iloc[0]) * 86400
        df['totalSeconds'] = totalSeconds
    

    __reply("Done \n")
    
    return df 

## END OF FILE
