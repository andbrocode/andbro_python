#!/bin/python 

def __filterStream(st, config):
    ''' 
    INPUT: 
          - st:         stream
          - config:     configurations
             - setFilter:       bool
             - filter_type:     e.g. bandpass/bp 
             - filter_corners:  [lower, upper]


    OUTPUT: stream
    '''
    
    import sys
    from numpy import nan, isnan, ones

    
    ## check for NaN in data and create masks
    masks, masks_empty = [], True

    ## apply filter according to configurations
    if config['setFilter']:
        if set(('filter_type','filter_corners')).issubset(config.keys()):     
            print(f"\n Filtering: {config['filter_type']} {config['filter_corners']}...\n")
        else:
            sys.exit(" --> missing keyswords in config! Aborting ...")

    for tr in st:
        if isnan(tr.data).any():
            mask = ones(len(tr.data))
            for i, e in enumerate(tr.data):
                if isnan(e):
                    tr.data[i] = 0
                    mask[i] = nan
            print(" --> created masks for NaN values ")
            masks.append(mask)
            masks_empty = False
        else:
            masks.append([])

        ## apply filter as specified in configurations
        if config['setFilter']:
            if config.get("filter_type") in ['bp', 'bandpass']:
                print(f" {tr.stats.station}.{tr.stats.channel}.: Applying bandpass {config.get('filter_corners')[0]} - {config.get('filter_corners')[1]} Hz")
                tr=tr.filter("bandpass", freqmin=config.get("filter_corners")[0], freqmax=config.get("filter_corners")[1], corners=4, zerophase=True)
            elif config.get("filter_type") in ['lp', 'lowpass']:
                print(f" {tr.stats.station}.{tr.stats.channel}: Applying lowpass {config.get('filter_corners')[1]} Hz")
                tr=tr.filter("lowpass", freq=config.get("filter_corners")[1], corners=4, zerophase=True)
            elif config.get("filter_type") in ['hp', 'highpass']:
                print(f" {tr.stats.station}.{tr.stats.channel}: Applying highpass {config.get('filter_corners')[0]} Hz")
                tr=tr.filter("highpass", freq=config.get("filter_corners")[0], corners=4, zerophase=True)
        
        ## re-apply mask
        if not masks_empty:
            for i, tr in enumerate(st):
                if i < len(masks):
                    if not len(masks[i]) == 0:
                        tr.data *= masks[i]

    return st
