#!/usr/bin/python
#
# make a plot of traces within a stream and their spectra 
#
# by AndBro @2022
# __________________________

def __makeplotStreamSpectra(st, config):

    from scipy import fftpack
    import matplotlib.pyplot as plt

#    plt.style.use('default')


    fig, axes = plt.subplots(5,2,figsize=(15,10), sharex='col')

    plt.subplots_adjust(hspace=0.3)

    ## _______________________________________________

    st.sort(keys=['channel'], reverse=True)
    
    for i, tr in enumerate(st):


        comp_fft = abs(fftpack.fft(tr.data))
        ff       = fftpack.fftfreq(comp_fft.size, d=1/tr.stats.sampling_rate)
        comp_fft = fftpack.fftshift(comp_fft)


        ## _________________________________________________________________
        axes[i,0].plot(
                    tr.times()/60,
                    tr.data,
                    color='black',
                    label='{} {}'.format(tr.stats.station, tr.stats.channel),
                    lw=1.0,
                    )


        ## _________________________________________________________________
        axes[i,1].plot(
                    ff[1:len(ff)//2],
                    abs(fftpack.fft(tr.data)[1:len(ff)//2]),
                    color='black',
                    lw=1.0,
                    )


        
        axes[i,0].set_ylabel(r'$\Omega$ (rad/s)')    
        axes[i,1].set_ylabel('ASD (rad/s/Hz)')        
#         axes[i,0].legend(loc='upper left',bbox_to_anchor=(0.8, 1.10), framealpha=1.0)
        axes[i,0].annotate('{} {}'.format(tr.stats.station, tr.stats.channel), 
                           xy=(0.4,0.928+i*-0.181),
                           xycoords='figure fraction', 
                           )
        axes[i,0].ticklabel_format(axis='y', style='sci', scilimits=(0,0))
        axes[i,1].ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    
        if config['set_filter']:
            if config['filter_type'] == "bandpass":
                axes[i,1].annotate('{}-{} Hz'.format(config['lower_corner_frequency'], config['upper_corner_frequency']), xy=(0.88,0.90+i*-0.18), xycoords='figure fraction')
            elif config['filter_type'] == "lowpass":
                axes[i,1].annotate('<{} Hz'.format(config['upper_corner_frequency']), xy=(0.88,0.90+i*-0.18), xycoords='figure fraction')
            elif config['filter_type'] == "highpass":
                axes[i,1].annotate('>{} Hz'.format(config['lower_corner_frequency']), xy=(0.88,0.90+i*-0.18), xycoords='figure fraction')

        if config['upper_corner_frequency'] is not None:
            
            axes[i,1].set_xlim(0, 1.5*config['upper_corner_frequency'])
#         axes[i,1].set_yscale('logit')

        if i == len(st)-1:
            axes[i,0].set_xlabel('Time (min)  from {} {} UTC'.format(tr.stats.starttime.date, str(tr.stats.starttime.time)[0:8]))
            axes[i,1].set_xlabel('Frequency (Hz)')
    
    
    ## save figure if specified in configurations
    if config['save_figs']:
        __savefig(fig, outpath=config['outpath_figs'], outname=f"TraceSpectrum_{config['tbeg'].date}"+".png", mode="png");

    return fig

## End of File
