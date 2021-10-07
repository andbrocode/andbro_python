#!/usr/bin/env python
# coding: utf-8


def __makeplot_compare2traces(st1, st2, ylabel=None):
    ''' 
    plot two traces and their difference 

    VARIABLES:
        
        st1:    traces or stream or array 
        st2:    traces or stream or array 
        ylabel: str for label on y-axis 


    DEPENDENCIES:
    
        import matplotlib.pyplot as plt
	from numpy import arange
	
    OUTPUT:
        
        fig: figure object 
        
    EXAMPLE:
    
        >>> fig = __makeplot_compare2traces(st1, st2, ylabel=None)

    '''

    import matplotlib.pyplot as plt
    from numpy import arange
	
    if str(type(st1)) == "<class 'obspy.core.stream.Stream'>":
        tr1 = st1[0].data
        tr2 = st2[0].data
        timeline = arange(0, st1[0].stats.npts*st1[0].stats.delta, st1[0].stats.delta)
        l1, l2 = f"{st1[0].stats.station}.{st1[0].stats.channel}", f"{st2[0].stats.station}.{st2[0].stats.channel}"
        t0 = f"{st1[0].stats.starttime.date} {str(st1[0].stats.starttime.time)[:9]} UTC"
        
    elif str(type(st1)) == "<class 'obspy.core.trace.Trace'>":
        tr1 = st1.data
        tr2 = st2.data
        timeline = arange(0, st1.stats.npts*st1.stats.delta, st1.stats.delta)
        l1, l2 = f"{st1.stats.station}.{st1.stats.channel}", f"{st2.stats.station}.{st2.stats.channel}"
        t0 = f"{st1.stats.starttime.date} {str(st1.stats.starttime.time)[:9]} UTC"

    else:
        timeline = arange(0, len(st1), 1)
        l1, l2 = "trace1", "trace2"
        t0 = []
        
    ## _______________________
    ## Plotting
        
    fig, ax = plt.subplots(3, 1, figsize=(17,5), sharex=True)

    font = 12
        
    ax[0].plot(timeline, tr1, label=l1)
    ax[0].legend(loc="upper right")
    
    ax[1].plot(timeline, tr2, label=l2)
    ax[1].legend(loc="upper right")
    
    ax[2].plot(timeline, tr1-tr2, label=f"{l1}-{l1}")
    ax[2].legend(loc="upper right")

    ax[0].tick_params(axis='both', labelsize=font-1)
    ax[1].tick_params(axis='both', labelsize=font-1)
    ax[2].tick_params(axis='both', labelsize=font-1)
    
    ax[2].set_xlabel(f"Time from {t0} (s)", fontsize=font)
    
    if ylabel is None:
        ax[0].set_ylabel(f"rot. rate \n (rad/s)", fontsize=font)
        ax[1].set_ylabel(f"rot. rate \n (rad/s)", fontsize=font)
        ax[2].set_ylabel(f"rot. rate \n (rad/s)", fontsize=font)
    else:
        ax[0].set_ylabel(ylabel, fontsize=font)
        ax[1].set_ylabel(ylabel, fontsize=font)
        ax[2].set_ylabel(ylabel, fontsize=font)        
    plt.show();
    
    return fig 
