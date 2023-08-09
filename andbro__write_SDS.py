#!/usr/bin/python
#
# description
#
# by AndBro @2022
# __________________________


'''

VARIABLES:
 - st:          stream object to write
 - config:	    configuration dictionary (keys: output_file, output_path)

DEPENDENCIES:
 - import os

OUTPUT:
 - None
 
EXAMPLE:
>>> __write_SDS(st, config)

'''

def __write_SDS(st, config):

    ## check if output_path and output_file is set in config
    if not "output_path" in config.keys():
        print(" -> missing config key: output_path")
        return

    ## check if output path exists
    if not os.path.exists(config['output_path']):
        print(f" -> {config['output_path']} does not exist!")
        return
    
    for tr in st:
        nn, ss, ll, cc = tr.stats.network, tr.stats.station, tr.stats.location, tr.stats.channel
        yy, jj = tr.stats.starttime.year, tr.stats.starttime.julday
        
        if not os.path.exists(config['output_path']+f"{yy}/"):
            os.mkdir(config['output_path']+f"{yy}/")
            print(f"creating: {config['output_path']}{yy}/")
        if not os.path.exists(config['output_path']+f"{yy}/{nn}/"):
            os.mkdir(config['output_path']+f"{yy}/{nn}/")
            print(f"creating: {config['output_path']}{yy}/{nn}/")
        if not os.path.exists(config['output_path']+f"{yy}/{nn}/{ss}/"):
            os.mkdir(config['output_path']+f"{yy}/{nn}/{ss}/")
            print(f"creating: {config['output_path']}{yy}/{nn}/{ss}/")
        if not os.path.exists(config['output_path']+f"{yy}/{nn}/{ss}/{cc}.D"):
            os.mkdir(config['output_path']+f"{yy}/{nn}/{ss}/{cc}.D")
            print(f"creating: {config['output_path']}{yy}/{nn}/{ss}/{cc}.D")

    for tr in st:
        nn, ss, ll, cc = tr.stats.network, tr.stats.station, tr.stats.location, tr.stats.channel
        yy, jj = tr.stats.starttime.year, str(tr.stats.starttime.julday).rjust(3,"0")
        
        try:
            st_tmp = st.copy()
            st_tmp.select(channel=cc).write(config['output_path']+f"{yy}/{nn}/{ss}/{cc}.D/"+f"{nn}.{ss}.{ll}.{cc}.D.{yy}.{jj}", format="MSEED")
        except:
            print(f" -> failed to write: {cc}")


## End of File
