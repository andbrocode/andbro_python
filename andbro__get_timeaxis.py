#!/usr/bin/python
#
# by AndBro @2021
# __________________________

def __get_timeaxis(dates=None, times=None, timestamp=None, unit='seconds', unitmode='relative', dateformat="yyyymmdd"):
    '''
    This method returns a time axis and appropriate ticks & labels according to the set mode
    
    ARGS: 
        dates:       array/list of dates (e.g. 20210901)
        times:       array/list of times (e.g. 130405)
        timestamp:   array/list of timestamps (e.g. '20210901 13:04:05)
        unit:        selected time unit: seconds, minutes, hours, days, time, date
        unitmode:    relative or absolute (default: relative )
        dateformat:  format of date passed (default: yyyymmdd)
    RETURN: 
        timeaxis, ticks, ticklabels, axistext
        
    '''
    
    from obspy import UTCDateTime
    from numpy import array, linspace, around, unique, arange
    from math import floor, ceil
    from pandas import Series
    
    ## _______________________________
    ## 
    
    def __time_to_seconds(arr):
        return array([int(str(i).rjust(6, "0")[:2])*3600+int(str(i).rjust(6, "0")[2:4])*60+int(str(i).rjust(6, "0")[-2:]) for i in arr])
    
    def __date_to_seconds(arr):
        return array([UTCDateTime(str(i)).julday * 86400 for i in arr ])
    
    def __timestamp_to_seconds(arr):
        try:
            x = UTCDateTime(str(arr[0]))
        except:
            print("Error: Not convertable to UTCDateTime! Aborting..."); return
        
        dd = array([UTCDateTime(str(i)).date for i in arr])
        tt = array([UTCDateTime(str(i)).time.strftime("%HH%MM%SS") for i in arr])
                  
        return __date_to_seconds(dates) + __time_to_seconds(times)      

    def __get_unique_dates(dates, times):
        a, b = unique(dates, return_index=True)
        
        ## trying to avoid date that starts in the mid of the day due to gap
#         ud, udx = [], []
#         for m, (d, i) in enumerate(zip(a,b)):
#             if times[i] == 0:
#                 ud.append(d)
#                 udx.append(i)         
#         return ud, udx
        return a, b 

    def __format_date(series, dateformat):
        
        if "-" in dateformat: 
            dateformat.replace("-","")
            series.str.replace("-","")
        
        if dateformat is "ddmmyy":
            tmp = series.astype(str).str.rjust(6,"0")
            oseries = "20"+tmp.str[-2:]+"-"+tmp.str[2:4]+"-"+tmp.str[:2]; del tmp
            return oseries

    def __reduce(arr):
        if len(arr) <= 5: 
            return arr 
        else: 
            return __reduce(arr[0:-1:2])    
    
    ## _______________________________
    ## run checks
                  
    if (dates is None and times is not None) or (dates is not None and times is None):
        print("ERROR: No valid arrays provide!"); return
    
    if dateformat is not "yyyymmdd":
        dates = __format_date(Series(dates), dateformat)   
        print(f' -> Formating: date <{dateformat}> -> <yyyymmdd>')
    
    if dates is not None and times is not None:
        case = 1
        
        dates, times = array(dates), array(times)
        
        date0_time0 = UTCDateTime(f'{dates[0]} {str(times[0]).rjust(6,"0")}')
        date0 = date0_time0.date.strftime("%Y-%m-%d")
        time0 = date0_time0.time.strftime("%H:%M:%S")
        


    elif timestamp is not None: 
        case = 2
        
        date0, time0 = UTCDateTime(timestamp[0]).date, UTCDateTime(timestamp[0]).time

    if unitmode not in ['relative', ' absolute']:
        print(f"ERROR: mode {unitmode} is not valid!")

    units = {'seconds': ['sec', 1],
            'minutes': ['min', 60],
            'hours': ['hours', 3600],
            'days': ['days', 86400],
            'date': ['', 86400],
            'time': ['', 1],
            }
    
    if not unit in units.keys():
        print(f"ERROR: unit {unit} is not valid!")
            
    ## _______________________________
    ## get timeaxis
        
    ## as total seconds
    if case == 1:
        timeaxis = __date_to_seconds(dates) + __time_to_seconds(times)
    elif case == 2:
        timeaxis = __timestamp_to_seconds(timestamp)
    
    ## _______________________________
    ## get ticks & lables
    numTicks = 5
    
    ticks = linspace(min(timeaxis), max(timeaxis), numTicks)
    unique_dates, unique_dates_idx = __get_unique_dates(dates, times)
    
    ## adjust if timeaxis is relative or absolute
    if unitmode is 'relative':
        lticks = linspace(min(timeaxis), max(timeaxis), numTicks) - min(timeaxis)
        text = f' Time ({units[unit][0]}) from {date0} {time0} UTC'
        
    elif unitmode is 'absolute':
        lticks = linspace(min(timeaxis), max(timeaxis), numTicks)
        text = f' Time ({units[unit][0]})'
    
    ## adjust to selected unit for timeaxis
    if unit in ['seconds', 'minutes', 'hours']:
        ticklabels = around(lticks/units[unit][1], decimals=0)
        ticklabels = [int(ll) for ll in ticklabels]
        
    elif unit in ['time']:
        ticklabels = []
        for t in lticks:
            hh = str(int(t/3600)).rjust(2,"0")
            mm = str(int(t%3600/60)).rjust(2,"0")
            ss = str(int(t%3600%60)).rjust(2,"0")
            ticklabels.append(f'{hh}:{mm}:{ss}')
    
    elif unit in ['date', 'days']:
        ticks = [ timeaxis[idx] for idx in unique_dates_idx ]
        
        if unit == 'date':
            ticklabels = [ str(dd) for dd in unique_dates ]       
            text = ""
        elif unit == 'days':
            ticks = ticks[1:]
            ticklabels = arange(1, len(ticks)+1, 1)
            text = f"Time ({units[unit][0]}) from {date0} {time0} UTC"
    else:
        print(f" -> Mode: {unit} is not a valid option!")       
        return 
    
    ## shorten list of ticklabels adaptively 
    if len(ticks) > numTicks:
#         numElems = len(unique_dates) - len(unique_dates)%numTicks
#         steps = int(np.floor(len(unique_dates)/numTicks))
#         idx = arange(0, numElems, steps).astype(int)
#         ticklabels = [ l if n in idx else '' for n, l in enumerate(ticklabels) ]
        idx = __reduce(ticks)
        ticklabels = [ ticklabels[n] if t in idx else '' for n, t in enumerate(ticks) ]
    else:
        idx = arange(0, numTicks, 1)
        ticklabels = [ l if n in idx else '' for n, l in enumerate(ticklabels) ]

    return timeaxis, ticks, ticklabels, text

## END OF FILE
