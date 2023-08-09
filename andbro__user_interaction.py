#!/usr/bin/python
#
# interact with user to querry information
#
# by AndBro @2022
# __________________________

def __getFilterInfo(config):

    from obspy import UTCDateTime


    config['seed_id'] = ["BW.ROMY.10.BJZ","BW.ROMY..BJU","BW.ROMY..BJV","BW.ROMY..BJW", "BW.RLAS..BJZ"]
    config['repos'] = "george"
    config['datapath'] = None


    ## ask user to specify event information
    config['name']  = input("\nEnter a name:  ") or None
    config['name']  = f'ROMY_{str(obs.UTCDateTime.now())[:10]}_{config.get("name")}'


    ## ask for event information
    config['event_time'] =  UTCDateTime(input("\nEnter Time of Event  in UTC (e.g. 2022-02-08 17:30):  ")) or None
    config['event_duration'] =  input("\nEnter Duration of Event (in minutes):  ") or None
    config['event_magnitude'] =  input("\nEnter Magnitude of Event (e.g. 6.5):  ") or None


    ## ask for filter parameters
    config['set_filter'] = input("\nSet Filter (yes/[no])?  ") or None
    if config['set_filter'] is not None and config['set_filter'] in ['y','yes','Y', 'Yes']:
        config['set_filter'] = True
    else:
        config['set_filter'] = False

    if config['set_filter']:
        config['filter_type'] = input("\nEnter filter type (bp, lp, hp): ")
        if config['filter_type'].lower() in ['bp', 'bandpass']:
            config['filter_type'] = 'bandpass'
            config['lower_corner_frequency'] = float(input("\nEnter lower corner frequency (in Hz): ")) or None
            config['upper_corner_frequency'] = float(input("Enter upper corner frequency (in Hz): ")) or None
        elif config['filter_type'].lower() in ['hp', 'highpass']:
            config['filter_type'] = 'highpass'
            config['lower_corner_frequency'] = float(input("\nEnter lower corner frequency (in Hz): ")) or None
            config['upper_corner_frequency'] = None
        elif config['filter_type'].lower() in ['lp', 'lowpass']:
            config['filter_type'] = 'lowpass'
            config['lower_corner_frequency'] = None
            config['upper_corner_frequency'] = float(input("\nEnter upper corner frequency (in Hz): ")) or None
        else:
            config['set_filter'] = False
            print("\n -> wrong filter parameters were provided! No Filter is set!")

    print("\n_____________________________________________________\n")
    return config


## End of File
