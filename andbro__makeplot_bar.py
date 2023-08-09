#!/usr/bin/python
#
# plot a nice bar plot with customized xticks
#
# by AndBro @2022
# __________________________


def __makeplot_bar(config):
    
    '''
    Config: 
        - xdata         data on x-axis
        - ydata         data on y-axis
        - xth           nth xtick that is shown
        - ylabel        label for y-axis
        - title         title of plot
        
    '''
    
    import matplotlib.pyplot as plt    

    # Creating histogram
    fig, ax = plt.subplots(1, 1, figsize =(12, 5), tight_layout = True)

    NN = len(config['xdata'])

    # Remove axes splines
    for s in ['top', 'bottom', 'left', 'right']:
        ax.spines[s].set_visible(False)

    # Remove x, y ticks
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')

    # Add padding between axes and labels
    ax.xaxis.set_tick_params(pad = 5)
    ax.yaxis.set_tick_params(pad = 10)

    # Add x, y gridlines
    ax.grid(b = True, color ='grey', linestyle ='-.', linewidth = 0.5, alpha = 0.6, zorder=0)


    # Creating histogram
    bars = range(0, NN)
    ax.bar(bars, config['ydata'], width=0.8, align='center', alpha=0.9)


    # Set ticks
    datelabel = config['xdata'][::config['xth']]
    dateticks = bars[::config['xth']]

    ax.set_xticklabels(datelabel)
    ax.set_xticks(dateticks)


    # Adding extra features   
    plt.ylabel(config['ylabel'])
    plt.title(config['title'])
              
    # Show plot
    plt.show();

    return fig

## End of File
