#!/usr/bin/python
#
# by AndBro @2021
# __________________________

def __get_timeaxis(dates=None, times=None, utcdatetime=None, timestamp=None, unit=None, unitmode='relative', dateformat="yyyymmdd",streamstats=None):
    '''
    This method returns a time axis and appropriate ticks & labels according to the set mode

    ARGS:
        dates:       array/list of dates (e.g. 20210901)
        times:       array/list of times (e.g. 130405)
        utcdatetime: array/list of UTCDateTimes
        timestamp:   array/list of timestamps (e.g. '20210901 13:04:05)
        unit:        selected time unit: seconds, minutes, hours, days, time, date
        unitmode:    relative or absolute (default: relative )
        dateformat:  format of date passed (default: yyyymmdd)

    RETURN:
        timeaxis, ticks, ticklabels, axistext


    EXAMPLE:
        timeaxis, ticks, ticklabels, text = __get_timeaxis(
                                                 utcdatetime=tr.times(type="utcdatetime"),
                                                 unit="time",
                                                 unitmode="absolute",
                                                 dateformat="yyyymmdd",
                                                  )
    '''

    from obspy import UTCDateTime
    from numpy import array, linspace, around, unique, arange, zeros, append
    from math import floor, ceil
    from pandas import Series


    reference_date = UTCDateTime(1970,1,1)

    ## _______________________________
    ##

    def __time_to_seconds(arr):
        return array([int(str(i).rjust(6, "0")[:2])*3600+int(str(i).rjust(6, "0")[2:4])*60+int(str(i).rjust(6, "0")[-2:]) for i in arr])

    def __date_to_seconds(arr):
        new_array = zeros(len(arr))
        start  = UTCDateTime(str(arr[0])).julday*86400
        for n, i in enumerate(arr):
            new_array[n] = UTCDateTime(str(i)).julday * 86400 - start
        new_array += UTCDateTime(str(arr[0])) - reference_date
        return new_array

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
        return a, b

    def __format_date(series, dateformat):

        if "-" in dateformat:
            dateformat.replace("-","")
            series.str.replace("-","")

        if dateformat is "ddmmyy":
            tmp = series.astype(str).str.rjust(6,"0")
            oseries = "20"+tmp.str[-2:]+"-"+tmp.str[2:4]+"-"+tmp.str[:2]; del tmp
            return oseries
        else:
            print("format not specified")


    def __reduce(arr):
        if len(arr) <= 5:
            return arr
        else:
            return __reduce(arr[0:-1:2])

    ## _______________________________
    ## preprocessing

    print("\n -> generate time axis")

    if (dates is None and times is not None) or (dates is not None and times is None):
        print("ERROR: No valid arrays provide! Provide dates and times array!"); return

    if dateformat is not "yyyymmdd":
        dates = __format_date(Series(dates), dateformat)
        print(f'  -> Formating: date <{dateformat}> -> <yyyymmdd>')

    if dates is not None and times is not None:
        case = 1

        dates, times = array(dates), array(times)

        date0_time0 = UTCDateTime(f'{dates[0]} {str(times[0]).rjust(6,"0")}')
        date0 = date0_time0.date.strftime("%Y-%m-%d")
        time0 = date0_time0.time.strftime("%H:%M:%S")

    elif timestamp is not None:
        case = 2

        date0, time0 = UTCDateTime(timestamp[0]).date, UTCDateTime(timestamp[0]).time

    elif utcdatetime is not None:
        case = 3

        date0, time0 = utcdatetime[0].date, utcdatetime[0].time
        dates, times = [], []
        #N = len(utcdatetime)
        #dates, times = zeros(N), zeros(N)

        for i, dt in enumerate(utcdatetime):
            #dates[i] = int(str(dt.date).replace("-",""))
            #times[i] = str(dt.time).split(".")[0].replace(":","")
            dates.append(int(str(dt.date).replace("-","")))
            times.append(str(dt.time).split(".")[0].replace(":",""))
        #dates = list(dates)
        #times = list(times)
    elif streamstats is not None:
        case = 4
        time_offset = streamstats.starttime.time.hour*3600+streamstats.starttime.time.minute*60+streamstats.starttime.time.second+streamstats.starttime.time.microsecond*1e-6
        times = arange(0, streamstats.npts*streamstats.delta, streamstats.delta) + time_offset
        timeaxis = times + (UTCDateTime(streamstats.starttime.date) - reference_date)
    else:
        print(dates, times)
        print(" -> no case matches!")
        return

    if unitmode not in ['relative', 'absolute']:
        print(f"ERROR: mode {unitmode} is not valid!")

    units = {'seconds': ['sec', 1],
            'minutes': ['min', 60],
            'hours': ['hours', 3600],
            'days': ['days', 86400],
            'date': ['', 86400],
            'time': ['UTC', 1],
            }

    if not unit in units.keys() and unit is not None:
        print(f"ERROR: unit {unit} is not valid!")

    ## _______________________________
    ## get timeaxis

    ## as total seconds
    if case == 1 or case == 3:
        timeaxis = __date_to_seconds(dates) + __time_to_seconds(times)
    elif case == 2:
        timeaxis = __timestamp_to_seconds(timestamp)
#    elif case == 4:
#        pass

    ## adjust timeaxis to relative time scale
    if unitmode == 'relative':
        timeaxis -= min(timeaxis)


    ## ___________________________________
    ## adjust timeaxis to selected unit

    if unit is not None:
        if unit == 'minutes':
            timeaxis /= 60
        elif unit == 'hours':
            timeaxis /= 3600
        elif unit == 'days':
            timeaxis /= 86400
    else:
        print("Timeaxis unit is selected automatically!")
        if max(timeaxis) > 2*86400:
            timeaxis, unit = timeaxis/86400, "days"
        elif max(timeaxis) > 2*3600:
            timeaxis, unit = timeaxis/3600, "hours"
        elif max(timeaxis) > 5*60:
            timeaxis, unit = timeaxis/60, "minutes"
        else:
            unit = "seconds"

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
        text = f"Time ({units[unit][0]}) on {date0}"

    elif unit in ['time']:
        ticklabels = []
        for t in lticks:
            hh = str(int(t/3600-utcdatetime[0].julday*24)).rjust(2,"0")
            mm = str(int(t%3600/60)).rjust(2,"0")
            ss = str(int(t%3600%60)).rjust(2,"0")
            ticklabels.append(f'{hh}:{mm}:{ss}')
            text = f"Time from {date0} {time0.split('.')[0]} ({units[unit][0]}) "

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
        idx = __reduce(ticks)
        ticklabels = [ ticklabels[n] if t in idx else '' for n, t in enumerate(ticks) ]
    else:
        idx = arange(0, numTicks, 1)
        ticklabels = [ l if n in idx else '' for n, l in enumerate(ticklabels) ]

    if unit == 'date':
        ticklabels = list(map(lambda x: x.replace('-', ''), ticklabels))
        ticklabels = [f'{s[0:4]}-{s[4:6]}-{s[6:8]}' if len(s) > 0 else s for s in ticklabels ]



    return timeaxis, ticks, ticklabels, text

## END OF FILE
