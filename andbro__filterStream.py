#!/bin/python 

def __filterStream(st, config):
    ''' 
    INPUT: 
          - st:         stream
          - config:     configurations
             - set_filter:               bool
             - filter_type:              e.g. bandpass/bp 
             - upper_corner_frequency:   float
             - lower_corner_frequency:   float

    OUTPUT: stream
    '''
    
    import sys
    from numpy import nan, isnan, ones
    from numpy.ma import is_masked

    ## apply filter according to configurations
    if config['set_filter']:
        if set(('filter_type', 'set_filter')).issubset(config.keys()):     
            print(f"\n Applying {config['filter_type']}...\n")
        else:
            sys.exit(" --> missing keyswords in config! No filter is set! Aborting ...")
    
    ## check for NaN in data and create masks
    masks, masks_empty = [], True

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

        
        ## apply the filter defined in the configurations
        if config['filter_type'] == 'bandpass':
            tr = tr.filter(
                            config['filter_type'], 
                            freqmin=config['lower_corner_frequency'], 
                            freqmax=config['upper_corner_frequency'],
                            corners=4,
                            zerophase=True,
                            );
        elif config['filter_type'] == 'lowpass':
            rt = tr.filter(
                            config['filter_type'], 
                            freq=config['upper_corner_frequency'],
                            corners=4,
                            zerophase=True,
                            );
        elif config.filter_type == 'highpass':
            tr = tr.filter(
                            config['filter_type'], 
                            freq=config['lower_corner_frequency'], 
                            corners=4,
                            zerophase=True,
                            );

        ## re-apply mask
        if not masks_empty:
            for i, tr in enumerate(st):
                if i < len(masks):
                    if not len(masks[i]) == 0:
                        tr.data *= masks[i]

    return st

## END OF FILE
