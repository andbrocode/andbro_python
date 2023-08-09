#!/usr/bin/python3

def __showClients():
    '''
    show clients availble for obspy
    '''

    from obspy.clients.fdsn.header import URL_MAPPINGS
    
    names = []
    for key in sorted(URL_MAPPINGS.keys()):

        names.append("{0:<11} {1}".format(key,  URL_MAPPINGS[key]))
    return names

## END OF FILE
