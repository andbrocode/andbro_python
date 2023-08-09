#!/usr/bin/python
#
# make plot as helicorder (with mlti times)
#
# by AndBro @2023
# __________________________


def __makeplot_helicorder(config, traces, times, time_stamps=None, mlti_bins=None):

    from numpy import linspace, shape, nanmax, nanmedian, array

    N = shape(traces)[0]
    
    ## extract colors from colormap
    cols = plt.cm.jet_r(linspace(0, 1, N+1))

    ## ____________________________________________

    fig, ax = plt.subplots(1,1, figsize=(15,10))

    plt.subplots_adjust(wspace=0.15)

    font = 14
    
    timeaxis = linspace(0, 60, len(traces[0]))

    for m, (tr, t_axis) in enumerate(zip(traces, times)):
        
        norm_tr_max = nanmax(abs(tr))
        
        ax.plot(t_axis/60, (tr - nanmedian(tr))/norm_tr_max + N-1-m, color=cols[m], alpha=0.4, zorder=3)

        if mlti_bins:
            for mlti in mlti_bins[m]:

                ax.plot([mlti/60, mlti/60], [-.8+N-2-m, .8+N-2-m], color='k', zorder=1, alpha=0.3)
                
    
    if time_stamps:
        ax.set_yticks(linspace(0, len(time_stamps), len(time_stamps)+1))
        ax.set_yticklabels([str(int(tt)).rjust(2,"0")+":00" for tt in array(time_stamps)])
    else:
        ax.set_yticks(linspace(0,N-1,N))
        labelsy = [str(int(tt)).rjust(2,"0")+":00" for tt in linspace(0,N-1,N)]
        ax.set_yticklabels(labelsy[::-1])
        
    ax.set_ylim(-1, N)

    ax.tick_params(axis='both', labelsize=font-2)

    ax.set_xlabel("Time (min)", fontsize=font)
    
    ax.set_title(f"{config['seed']}  {str(config['tbeg'])[:-8]} - {str(config['tend'])[:-8]}", fontsize=font)
    
    plt.show();
    return fig


## End of File
