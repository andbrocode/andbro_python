#!/usr/bin/env python
# coding: utf-8



def __makeplot_traces_spectrogram(st1, st2, f_upper, spec_param=None, ylabel=None):
    ''' 
    plot two traces with the correspsonding spectrogram

    VARIABLES:
        
        st1:    traces or stream or array 
        st2:    traces or stream or array 
        ylabel: tuple (label1, label2) for label on y-axis 


    DEPENDENCIES:
    
        import matplotlib.pyplot as plt
        from numpy import arange, where
        from scipy.signal import spectrogram

    OUTPUT:
        
        fig: figure object 
        
    EXAMPLE:
    
        >>> fig = __makeplot_traces_spectrogram(st1, st2, ylabel=None)

    '''

    import matplotlib.pyplot as plt
    
    from scipy.signal import spectrogram
    from numpy import arange, where

    if spec_param is None:
        nfft, nseg, overlap = 512, 64, 32
    else:
        nfft, nseg, overlap = spec_param

        
    if str(type(st1)) == "<class 'obspy.core.stream.Stream'>":
        tr1 = st1[0].data
        tr2 = st2[0].data
        
        dt = st2[0].stats.delta
        
        timeline = arange(0, st1[0].stats.npts*st1[0].stats.delta, st1[0].stats.delta)
        
        l1, l2 = f"{st1[0].stats.station}.{st1[0].stats.channel}", f"{st2[0].stats.station}.{st2[0].stats.channel}"
        
        t0 = f"{st1[0].stats.starttime.date} {str(st1[0].stats.starttime.time)[:9]} UTC"
        
        freqs1, times1, Sxx1 = spectrogram( st1[0].data, 
                                            fs=1/st1[0].stats.delta,
                                            nfft=nfft,
                                            nperseg=nseg,
                                            noverlap=overlap,
                                            scaling="density",
                                          )
        
        freqs2, times2, Sxx2 = spectrogram( st2[0].data, 
                                            fs=1/st2[0].stats.delta,
                                            nfft=nfft,
                                            nperseg=nseg,
                                            noverlap=overlap,
                                            scaling="density",
                                          )
    elif str(type(st1)) == "<class 'obspy.core.trace.Trace'>":
        tr1 = st1.data
        tr2 = st2.data
        
        dt = st2.stats.delta
        
        timeline = arange(0, st1.stats.npts*st1.stats.delta, st1.stats.delta)
        
        l1, l2 = f"{st1.stats.station}.{st1.stats.channel}", f"{st2.stats.station}.{st2.stats.channel}"
        
        t0 = f"{st1.stats.starttime.date} {str(st1.stats.starttime.time)[:9]} UTC"
        
        
        freqs1, times1, Sxx1 = spectrogram( st1.data, 
                                            fs=1/st1[0].stats.delta,
                                            nfft=nfft,
                                            nperseg=nseg,
                                            noverlap=overlap,
                                            scaling="density",
                                          )
        
        freqs2, times2, Sxx2 = spectrogram( st2.data, 
                                            fs=1/st2[0].stats.delta,
                                            nfft=nfft,
                                            nperseg=nseg,
                                            noverlap=overlap,
                                            scaling="density",
                                          )
    else:
        timeline = arange(0, len(st1), 1)
        l1, l2 = "trace1", "trace2"
        t0 = []

        
    idx1 = len(where(freqs1<=2*f_upper)[0])
    idx2 = len(where(freqs2<=2*f_upper)[0])
    
    ## _______________________
    ## Plotting
        
    fig, ax = plt.subplots(4, 1, figsize=(17,10), sharex=True)

    font = 12
        
    ax[0].plot(timeline, tr1, label=l1)
    ax[0].legend(loc="upper right")
    
    im1 = ax[1].imshow(Sxx1[:][:idx1], aspect='auto', cmap='viridis', origin='lower', extent=[min(times1),max(times1),min(freqs1), freqs1[idx1]])

    cbaxes1 = fig.add_axes([0.92, 0.52, 0.01, 0.16]) 
    cb1 = plt.colorbar(im1 ,cax=cbaxes1, orientation='vertical',label="power (dB)")
    
    
    ax[2].plot(timeline, tr2, label=l2)
    ax[2].legend(loc="upper right")

    im2 = ax[3].imshow(Sxx2[:][:idx2], aspect='auto', cmap='viridis', origin='lower', extent=[min(times2),max(times2),min(freqs2), freqs2[idx2]])
    
    cbaxes2 = fig.add_axes([0.92, 0.12, 0.01, 0.16]) 
    cb2 = plt.colorbar(im2 ,cax=cbaxes2, orientation='vertical',label="power (dB)")
    
    ax[0].tick_params(axis='both', labelsize=font-1)
    ax[1].tick_params(axis='both', labelsize=font-1)
    ax[2].tick_params(axis='both', labelsize=font-1)
    
    ax[3].set_xlabel(f"Time from {t0} (s)", fontsize=font)
    
    if ylabel is None:
        ax[0].set_ylabel(f"rot. rate \n (rad/s)", fontsize=font)
        ax[1].set_ylabel(f"rot. rate \n (rad$^2$/s$^2$ Hz)", fontsize=font)
        ax[2].set_ylabel(f"rot. rate \n (rad/s)", fontsize=font)
        ax[3].set_ylabel(f"rot. rate \n (rad$^2$/s$^2$ Hz)", fontsize=font)

    else:
        ax[0].set_ylabel(ylabel[1], fontsize=font)
        ax[1].set_ylabel(ylabel[1], fontsize=font)
        ax[2].set_ylabel(ylabel[0], fontsize=font) 
        ax[3].set_ylabel(ylabel[1], fontsize=font)        

    plt.show();
    
    return fig 

## END OF FILE
