#!/usr/bin/python
#
# querry data and create stream
#
# by AndBro @2022
# __________________________

def __getStream(config, restitute=True):
    """
    
    CONFIG:     config['seeds'] list of seed names
                config['tbeg'] startime as UTCDateTime
                config['tend'] endtime as UTCDateTime
                config['repository'] data repository to call [e.g. george, archive, jane,online]


    st = __getStream(config, restitute=True)

    """

    from andbro__querrySeismoData import __querrySeismoData
    from andbro__empty_trace import __empty_trace
    from obspy import Stream
    
    st = Stream()


    for seed in config['seeds']:
        
        net, sta, loc, cha = seed.split(".")
        
        print(f"loading {seed}...")
        
        try:
            st0, inv0 = __querrySeismoData(  
                                            seed_id=seed,
                                            starttime=config.get("tbeg"),
                                            endtime=config.get("tend"),
                                            repository=config.get("repository"),
                                            path=None,
                                            restitute=False,
                                            detail=None,
                                            fill_value=None,
                                            )
            if restitute:
                if cha[-2] == "J":
                    print(" -> removing sensitivity...")
                    st0.remove_sensitivity(inv0)
                elif cha[-2] == "H":
                    print(" -> removing response...")
                    st0.remove_response(inventory=inv0, output="VEL", zero_mean=True)

            if len(st0) == 1:
                st += st0
            elif len(st0) > 1:
                print(" -> merging stream...")
                st += st0.merge()

        except:
            print(f" -> failed to load {seed}!")
            print(f" -> substituted {seed} with NaN values! ")
            st_empty = Stream()
            st_empty.append(__empty_trace(config, seed))
            st += st_empty
    
    print("\ncompleted loading")
    print(" -> trimming stream...")
    st.trim(config['tbeg'], config['tend'])
            
    return st

## End of File
