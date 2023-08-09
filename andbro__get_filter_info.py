#!/usr/bin/python
#
# ask user for details for filtering
#
# by AndBro @2022
# __________________________

def __getFilterInfo(config):

    from obspy import UTCDateTime


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
