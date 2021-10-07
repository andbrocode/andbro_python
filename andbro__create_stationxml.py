#!/usr/bin/env python
# coding: utf-8

# ## Create an STATION XML file for a seismometer




import re
from obspy import UTCDateTime, read_inventory
from obspy.clients.nrl import NRL
from obspy.io.xseed import Parser
from obspy.core.inventory import Inventory, Network, Station, Channel, Site
from obspy.clients.fdsn import Client as FDSNClient



## _____________________________

# could be replaced with a local download of NRL
nrl = NRL()


print(nrl.sensors)

manufacturer = input("\nChoose manufacturer: ");print("\n_______________________________")



print(nrl.sensors[manufacturer])

sensor = input("\nChoose sensor: ");print("\n_______________________________")



print(nrl.sensors[manufacturer][sensor])

sensitivity = input("\nChoose sensitivity: ");print("\n_______________________________")



print(nrl.sensors[manufacturer][sensor][sensitivity])

generation = input("\nChoose generation: ");print("\n_______________________________")



print(nrl.sensors[manufacturer][sensor][sensitivity][generation])


## _____________________________

print(nrl.dataloggers)

datalogger = input("\nChoose datalogger: ");print("\n_______________________________")



print(nrl.dataloggers[datalogger])

model = input("\nChoose datalogger model: ");print("\n_______________________________")


print(nrl.dataloggers[datalogger][model])

gain = input("\nChoose datalogger gain: ");print("\n_______________________________")


print(nrl.dataloggers[datalogger][model][gain])

sampling_rate = input("\nChoose datalogger sampling rate: ");print("\n_______________________________")


print(nrl.dataloggers[datalogger][model][gain][sampling_rate])


## _____________________________


response = nrl.get_response(
    datalogger_keys=[datalogger, model, gain, sampling_rate],
    sensor_keys=[manufacturer, sensor, sensitivity, generation]
    )


response.plot(0.001);

## _____________________________



net = input("\nEnter network: ");print("\n_______________________________")

sta = input("\nEnter station name: ");print("\n_______________________________")

site_name = input("\nEnter site name: ");print("\n_______________________________")

outpath = input("\nEnter path of output file: ");print("\n_______________________________")

location = input("\nSpecify location (y/n)? ")

if location == "y" or location == "yes":
    lat = input("Enter latitude: ")
    lon = input("Enter longitude: ")
    ele = input("Enter elevation: ")
    
else:
    lat, lon, ele = 0.0, 0.0, 0.0

outfile = f"{net}-{sta}.xml"


## _____________________________


channel1 = Channel(code='HHZ', 
                   location_code='', 
                   latitude=lat, 
                   longitude=lon,
                   elevation=ele, 
                   depth=0,
#                    azimuth=0,
#                    dip=-90,
                   sample_rate=sampling_rate,
                   response=response,
                  )

channel2 = Channel(code='HHN', 
                   location_code='', 
                   latitude=lat, 
                   longitude=lon,
                   elevation=ele, 
                   depth=0,
#                    azimuth=0,
#                    dip=0,
                   sample_rate=sampling_rate,
                   response=response,
                  )

channel3 = Channel(code='HHE', 
                   location_code='', 
                   latitude=lat, 
                   longitude=lon,
                   elevation=ele, 
                   depth=0,
#                    azimuth=90,
#                    dip=0,
                   sample_rate=sampling_rate,
                   response=response,
                  )



site = Site(name=site_name)


station = Station(code=sta, 
                  latitude=lat, 
                  longitude=lon,
                  elevation=ele,
                  channels=[channel1,channel2,channel3],
                  site=site,
                 )

network = Network(code=net,
                  stations=[station],
                 )


inv = Inventory(networks=[network], 
                source='LMU',
               )

## _____________________________
## actual writing to file

if outpath[-1] == "/":
    outpath = outfile[:-1]

inv.write(f"{outpath}/{outfile}", 
          format='STATIONXML',
         )

## _____________________________
## brief test if file is callable

try:
    read_inventory(f"{outpath}/{outfile}")
    print("\n DONE")
except:
    print("\n Something went wrong! File: {outpath}/{outfile} could not be loaded!")




