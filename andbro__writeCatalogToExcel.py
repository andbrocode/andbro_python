#!/usr/bin/python3

def __write_events_to_excel(cat, file, user_params=None):
    '''
    Write earthquake events from catalog to excel sheet

    RETURN:
        df:  Dataframe with events as printed to file

    EXAMPLE:
        df = __write_events_of_catalog(cat, "~/Documents/ROMY/ROMY_EventBase.xls")
    '''

    import pandas as pd

    df = pd.read_excel(file)

    for i, event in enumerate(cat):

        ## add row of None values at the end
        row = len(df)
        df.loc[row] = None

        ## assgin event values
        df.loc[row, 'EVENT ID'] = str(cat[i].resource_id).split("=")[1]
        df.loc[row, 'DATETIME'] = cat[i].origins[0].time
        df.loc[row, 'MAGNITUDE'] = cat[i].magnitudes[0].mag
        df.loc[row, 'MAGNITUDE TYPE'] = cat[i].magnitudes[0].magnitude_type
        df.loc[row, 'LONGITUDE'] = cat[i].origins[0].longitude
        df.loc[row, 'LATITUDE'] = cat[i].origins[0].latitude
        df.loc[row, 'DEPTH'] = cat[i].origins[0].depth
#         df.loc[row,'CATALOG'] =
        df.loc[row, 'FLINN_ENGDAHL'] = cat[i].event_descriptions[0].text

        if user_params is None:
            df.loc[row, 'RLAS']   = None
            df.loc[row, 'ROMY Z'] = None
            df.loc[row, 'ROMY U'] = None
            df.loc[row, 'ROMY V'] = None
            df.loc[row, 'ROMY W'] = None
            print(" --> No specification for ROMY channels provided!")
        else:
            df.loc[row, 'RLAS']   = user_params.get('RLAS')
            df.loc[row, 'ROMY Z'] = user_params.get('ROMY_Z')
            df.loc[row, 'ROMY U'] = user_params.get('ROMY_U')
            df.loc[row, 'ROMY V'] = user_params.get('ROMY_V')
            df.loc[row, 'ROMY W'] = user_params.get('ROMY_W')


        print(f" --> Added event: {df.iloc[row,0]} to {file}\n")

    ## sort for Datetime
    df.sort_values(by='DATETIME', ascending=True)

    ## write dataframe to
    df.to_excel(file, index=False)


    ## check for dublicates
    if len(df[df.duplicated('EVENT ID')])>0:
        df_dup = df[df.duplicated('EVENT ID')]
        print(f"\n --> Dublicates found: {df_dup['EVENT ID']}")

    return df


## END OF FILE
