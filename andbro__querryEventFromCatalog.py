#!/bin/python

def __querry_event_from_catalog(config):
    '''
    Get events from services as specified in the configuration 
    
    CONFIG: 
        config['tbeg']          = "2021-10-30"
        config['tend']          = "2021-11-02"
        config['min_magnitude'] = 6.0 
    
    RETURN: 
        cat:  obspy catalog object
        
    '''
    
    import sys    
    from obspy import UTCDateTime
    from obspy.clients.fdsn import Client
    
    # for catalog in ["IRIS","GFZ","BGR"]:
    for catalog in ["IRIS","ISC"]:

        try:
            ## get event from client as catalog object
            event_client = Client(catalog)
        
            cat = event_client.get_events(starttime=UTCDateTime(config.get('tbeg')), 
                                          endtime=UTCDateTime(config.get('tend')),
                                          minmagnitude=config.get('min_magnitude'))



            if not len(cat) == 0:
                print('\n -->  Using {} as source !!\n'.format(catalog))
                return cat
                break

        except:
            cat = obs.core.event.Catalog()
            print('\n !! Event not found in {} !!\n'.format(catalog))

    if len(cat) == 0:
            print("Empty catalog! EXIT!")
            sys.exit()


## END OF FILE
