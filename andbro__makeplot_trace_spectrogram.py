#!/usr/bin/env python
# coding: utf-8



def __makeplot_trace_spectrogram(tr, f_upper=None, spec_param=None, ylabel=None, full_output=False, normalize=False, unit=None):
    ''' 
    plot two traces with the correspsonding spectrogram

    VARIABLES:
        - tr:               trace or array 
        - f_upper:          upper frequency limit
        - ylabel:           tuple (label1, label2) for label on y-axis 
        - spec_param:       [nfft, nsegments, overlap]
        - full_output:      defines return valuse [fig  or  fig,Sxx,freqs]
        - normalize:        bool, normalize Spectrogram (default: False)
        - unit:             unit of time axis (['sec'], 'min', 'hour', 'day')

    DEPENDENCIES:
    
        import matplotlib.pyplot as plt
        from numpy import arange, where
        from scipy.signal import spectrogram

    OUTPUT:
        
        - fig               [full_output = False] 
        - fig, Sxx, freqs   [full_output = True]

    EXAMPLE:
    
        >>> fig = __makeplot_trace_spectrogram(tr, f_upper=None, spec_param=None, ylabel=None)

    '''
    
    import sys
    import matplotlib.pyplot as plt
    from scipy.signal import spectrogram
    from numpy import arange, where, nanmax

    
    if spec_param is None:
        nfft, nseg, overlap = None, 256, 64
    else:
        nfft, nseg, overlap = spec_param

        
    if str(type(tr)) == "<class 'obspy.core.stream.Stream'>":
        sys.exit("ERROR: Please enter a trace not a stream object! Aborting ...")
        
    elif str(type(tr)) == "<class 'obspy.core.trace.Trace'>":
        
        dt = tr.stats.delta
        
        timeline = arange(0, tr.stats.npts*tr.stats.delta, tr.stats.delta)
        
        l1, l2 = f"{tr.stats.station}.{tr.stats.channel}", f"{tr.stats.station}.{tr.stats.channel}"
        
        t0 = f"{tr.stats.starttime.date} {str(tr.stats.starttime.time)[:9]} UTC"
        
        freqs, times, Sxx = spectrogram(
                                        tr.data, 
                                        fs=1/tr.stats.delta,
                                        nfft=nfft,
                                        nperseg=nseg,
                                        noverlap=overlap,
                                        scaling="density",
                                        )
        print(f"Using windows of {round(tr.stats.delta*tr.stats.npts/nseg, 2)} seconds ")
    else:
        timeline = arange(0, len(tr), 1)
        l1 = "array"
        t0 = []

    ## reduce to upper frequency limit if provided
    if f_upper is not None:
        idx = where(freqs>=f_upper)[0][0]
        f_upper=freqs[idx]
        Sxx = Sxx[:idx][:]
    else:
        f_upper = 0.5/tr.stats.delta

        
    ## normalize the spectrogram
    if normalize:
        Sxx /= abs(Sxx).max(axis=0)
        
    if unit in ['min', 'sec', 'hour', 'day']:
        if unit is 'min':
            scale=60
        elif unit is 'hour':
            scale=3600
        elif unit is 'day':
            scale=86400
    else:
        scale=1
        unit='sec'         

    timeline /= scale
    times /= scale

    ## Plotting #####################################
        
    fig, ax = plt.subplots(2, 1, figsize=(17,10), sharex=True)

    plt.subplots_adjust(hspace=0.1)
    
    font = 14
        
    ax[0].plot(timeline, tr.data, label=l1)

    im1 = ax[1].imshow(Sxx[:][:], aspect='auto', cmap='viridis', origin='lower', 
                       extent=[min(times), max(times), 0, f_upper])

    cbaxes1 = fig.add_axes([0.92, 0.12, 0.02, 0.38]) 
    cb1 = plt.colorbar(im1 ,cax=cbaxes1, orientation='vertical')
#    cb1.set_label(label="Power (dB)", size=font-1)    
    
    ax[0].tick_params(axis='both', labelsize=font-1)
    ax[1].tick_params(axis='both', labelsize=font-1)
        
    if ylabel is None:
        if tr.stats.channel[1] == "H":
            ax[0].set_ylabel(r"Velocity (m/s)", fontsize=font)
#            ax[1].set_ylabel(r"ASD (m$^2$/(s$^2$ Hz))", fontsize=font)
            ax[1].set_ylabel(r"Frequency (Hz)", fontsize=font)
            cb1.set_label(label="ASD (m$^2$/(s$^2$ Hz))", size=font-1)    
        elif tr.stats.channel[1] == "J": 
            ax[0].set_ylabel(r"$\dot \Omega$ (rad/s)", fontsize=font)
#            ax[1].set_ylabel(r"$\dot \Omega$ (rad$^2$/(s$^2$ Hz))", fontsize=font)
            ax[1].set_ylabel(r"Frequency (Hz)", fontsize=font)
            cb1.set_label(label=r"$\dot \Omega$ (rad$^2$/(s$^2$ Hz))", size=font-1)    
        else:
            ax[0].set_ylabel(r"Amlitude", fontsize=font)
#            ax[1].set_ylabel(r"Amplitude (unit$^2$/ Hz))", fontsize=font) 
            ax[1].set_ylabel(r"Frequency (Hz)", fontsize=font)
            cb1.set_label(label=r"Amplitude (unit$^2$/ Hz))", size=font-1)
    else:
        ax[0].set_ylabel(ylabel[1], fontsize=font)
        ax[1].set_ylabel(ylabel[1], fontsize=font)
    
   
    ax[0].legend(loc="upper right", fontsize=font-2)
    ax[1].set_xlabel(f"Time ({unit}) from {t0} ", fontsize=font)  
#     ax[1].set_ylim(0, f_upper)

    plt.show();
    
    if full_output:
        return fig, Sxx, freqs
    else:
        return fig 



## End of File
