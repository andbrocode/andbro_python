#!/usr/bin/env python
# coding: utf-8

#from FastFourierTransform import __fast_fourier_transform


def __makeplot_trace_and_spectrum(trace_in, timeaxis=None, timeunit=None, fmax=None, grid=None, axis_scale='linear', smoothing=None, fulloutput=False, flip=False):
    '''
    Calculate and plot trace and spectrum. 
    
    PARAMETER:
        - timeaxis:         x-axis of time
        - timeunit:         unit of the provided timeaxis
        - smoothing:        int to define level of smoothing
        - axis_scale:       linlin, linlog, loglin, loglog
        - fulloutput:       bool (True -> fig, freqs, asd | [False] -> fig)
    
    EXAMPLE:

    fig(, freqs, asd) = __makeplot_trace_and_spectrum(trace_in, timeaxis=None, timeunit=None, fmax=None, grid=None, axis_scale='linear', smoothing=None, fulloutput=True, flip=False)

    
    '''    
    
    import sys
    import matplotlib.pyplot as plt
    from scipy.fft import fft, fftfreq, fftshift
    from scipy import signal
    from numpy import arange, convolve, ones, nanmin, nanmax, isfinite, log10
        
    def moving_average(x, w):
        return convolve(x, ones(w), 'same') / w
    
    def __fast_fourier_transform(signal_in, dt ,window=None, normalize=None):

        '''
        Calculating a simple 1D FastFourierSpectrum of a time series.

        Example:
        >>> N = 600
        >>> dt = 0.01
        >>> x = np.linspace(0.0, N*dt, N)
        >>> y = np.sin(10.0 * 2.0*np.pi*x) + 0.5*np.sin(15.0 * 2.0*np.pi*x)
        >>> sp, ff = __fft(y,dt,window=True,normalize=False)

        '''

        ## determine length of the input time series
        n = int(len(signal_in))


        ## calculate spectrum (with or without window function applied to time series)
        if window is None or window is False:
            spectrum = fft( signal_in )

        elif window is True:
            window = signal.hann(n); print('Hanning window applied \n')
            #window = signal.kaiser(n, beta=14); print('Kaiser window (beta = 14) applied \n')
            #window = signal.gaussian(n, std=20); print('Gaussian window (std = 20) applied \n')
            spectrum = fft( signal_in * window )

        ## calculate frequency array 
        frequencies = fftfreq(n, d=dt)


        ## correct amplitudes of spectrum and optional normalize
        if normalize == None or normalize == False:
            spectrum_out = 2.0 / n * abs( spectrum )

        elif normalize == True:
            spectrum_out = abs( spectrum / abs(spectrum[isfinite(spectrum)]).max()); 
            print('Spectrum normalized \n')

        ## return the positive frequencies
        return spectrum_out[1:n//2], frequencies[1:n//2]


    if str(type(trace_in)) == "<class 'obspy.core.stream.Stream'>":
        trace = trace_in[0].data
        timeline = arange(0, trace_in[0].stats.npts*trace_in[0].stats.delta, trace_in[0].stats.delta)
        l1 = f"{trace_in[0].stats.station}.{trace_in[0].stats.channel}"
        t0 = f"from {trace_in[0].stats.starttime.date} {str(trace_in[0].stats.starttime.time)[:9]} UTC"
        delta = trace_in[0].stats.delta
        
    elif str(type(trace_in)) == "<class 'obspy.core.trace.Trace'>":
        trace = trace_in.data
        timeline = arange(0, trace_in.stats.npts*trace_in.stats.delta, trace_in.stats.delta)
        l1 = f"{trace_in.stats.station}.{trace_in.stats.channel}"
        t0 = f"from {trace_in.stats.starttime.date} {str(trace_in.stats.starttime.time)[:9]} UTC"
        delta = trace_in.stats.delta
        
    else:
        trace = trace_in
        delta = 1
        timeline, timeunit = arange(0, len(trace_in), delta), "sec"
        l1 = "trace1"
        t0 = []

    ## modify timeaxis and timeunit
    if max(timeline) > 2*86400:
        timeline, timeunit = timeline/86400, "days"
    elif max(timeline) > 2*3600:
        timeline, timeunit = timeline/3600, "hours"  
    elif max(timeline) > 5*60: 
        timeline, timeunit = timeline/60, "min"

    if timeaxis is not None:
        if timeunit is None:
            print("Please provide a timeunit for the timeaxis")
        timeline, timeunit = timeaxis, timeunit
        delta = timeline[1]-timeline[0]


    ## calculate spectrum
    N = len(trace)

    trace_fft, ff = __fast_fourier_transform(signal_in=trace, dt=delta , window=None, normalize=None)

    freqs, asd = ff[:N // 2], abs(trace_fft[:N // 2])
    
    if len(asd[isfinite(asd)]) == 0:
        sys.exit("ERROR: all spectral amplitudes not finite! Aborting ...")
        
    ## calculate smoothed spectrum
    if smoothing is not None:
        if smoothing%2 == 0:
            smoothing -= 1
        asd_med = signal.medfilt(asd, kernel_size=smoothing)
  
    
    ## __________________________________________________________
    ## Plotting
    if flip:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15,5))
        plt.subplots_adjust(hspace=0.3)
    else:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15,5))

    font = 13 
        
    ## panel 1
    ax1.plot(timeline, trace, label=l1)
    
    ## panel 2    
    if axis_scale is "linlog":
        ax2.semilogy(freqs, asd)
        if smoothing is not None:
#             ax2.semilogy(freqs, moving_average(asd, smoothing), color="grey")
            ax2.semilogy(freqs, asd_med, color="grey", alpha=0.8)
     
    elif axis_scale is "loglin":
        ax2.semilogx(freqs, asd)
           
    elif axis_scale is "loglog":
        ax2.loglog(freqs, asd)
        if smoothing is not None:
            ax2.loglog(freqs, asd_med, color="grey", alpha=0.8)
        
    elif axis_scale is "linlin":
        ax2.plot(freqs, asd)
        

    ## plot adjustments
    ax1.set_xlabel(f"Time {t0} ({timeunit})", fontsize=font)
    ax2.set_xlabel("Frequency (Hz)", fontsize=font)
    ax1.legend(loc="upper right")
    
    if trace_in.stats.channel[1] == "H":
        ax1.set_ylabel(r"Amplitude ($\frac{m}{s}$)", fontsize=font)
        ax2.set_ylabel(r"ASD ($\frac{m}{s \sqrt{Hz} }$)", fontsize=font)
    elif trace_in.stats.channel[1] == "J": 
        ax1.set_ylabel(r"Amplitude ($\frac{rad}{s}$)", fontsize=font)
        ax2.set_ylabel(r"ASD ($\frac{rad}{s \sqrt{Hz} }$)", fontsize=font)
    else:
        ax1.set_ylabel(r"Amplitude (unit)", fontsize=font)
        ax2.set_ylabel(r"ASD ($unit{\sqrt{Hz} }$)", fontsize=font)

    if grid:
        ax1.grid(ls='--', zorder=-2, color='darkgrey')
        ax2.grid(ls='--', zorder=-2, color='darkgrey')
    
    if fmax:
        if axis_scale in ['linear', 'log']:
            ax2.set_xlim(0, fmax)
        elif axis_scale is 'loglog':
            ax2.set_xlim(nanmin(freqs), nanmax(freqs))
            
    if axis_scale is 'linear':
        maximal_asd = nanmax(asd[isfinite(asd)])
        ax2.set_ylim(0, maximal_asd+0.01*maximal_asd)        
        
    ax1.set_xlim(nanmin(timeline), nanmax(timeline))
    ax2.set_xlim(nanmin(freqs), nanmax(freqs))

    plt.show();
    
    if fulloutput:
        return fig, freqs, asd
    else:
        return fig
    
## End of File
