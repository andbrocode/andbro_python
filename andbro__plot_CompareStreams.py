#!/usr/bin/python
#
# compare traces of two streams

def __plotCompareStreams(st1, st2):
    """
    compare traces of two streams

    dependencies: 
    - import matplotlib.pyplot as plt
    
    example:
    	>>> __plotCompareStreams(st1, st2)
    """
    import matplotlib.pyplot as plt
    
    ## get the earliest starttime of the two streams
    tstart = min(st1[0].stats.starttime, st2[0].stats.starttime)

    ## find out about the number of rows to adjust the figure subplots
    if st1.count() is not st2.count():
        print("streams do not have the same amount of traces!")

    else: 
        rows = st1.count()

    ## create figure and axes objects 
    fig,  axes = plt.subplots(int(rows), 1, figsize=(15,10))


    if int(rows) == 1: 
        i = 0
        sta = st1[i].id.split(".")[1]
        cha = st1[i].id.split(".")[3]
        
        axes.plot(st1[i].times("matplotlib"), st1[i].data, label=f'{sta}.{cha}', color="red")
        axes.plot(st2[i].times("matplotlib"), st2[i].data, label=f'{sta}.{cha}', color="black")

        #axes.plot(st1[i].times("matplotlib")[0], 0, "*g-", linewidth=4, markersize=12)

        axes.legend()
        axes.set_ylabel("velocity (mm/s)")

        axes.set_xlabel(f"Time (s) from {tstart.date} {tstart.time} UTC ")

        plt.show();

    elif int(rows) > 1:

        for i, ax in enumerate(axes):
            ax.plot(st1[i].times("matplotlib"), st1[i].data, label=f'{sta}.{st1[i].id.split(".")[3]}', color="red")
            ax.plot(st2[i].times("matplotlib"), st2[i].data, label=f'{sta}.{st2[i].id.split(".")[3]}', color="black")

            #ax.plot(st1[i].times("matplotlib")[0], 0, "*g-", linewidth=4, markersize=12)

            ax.legend()
            ax.set_ylabel("velocity (mm/s)")

        ax.set_xlabel(f"Time (s) from {tstart.date} {tstart.time} UTC ")

        plt.show();
        
## END OF FILE
