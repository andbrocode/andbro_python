#!/usr/bin/env python
# coding: utf-8

import matplotlib.pyplot as plt

#from FastFourierTransform import __fast_fourier_transform
from numpy import arange, abs

def __makeplot_trace_and_spectrum(trace_in, timeaxis=None, fmax=None, grid=None):
    
    
    def __fast_fourier_transform(signal_in, dt ,window=None,normalize=None):

        '''
        Calculating a simple 1D FastFourierSpectrum of a time series.

        Example:
        >>> N = 600
        >>> dt = 0.01
        >>> x = np.linspace(0.0, N*dt, N)
        >>> y = np.sin(10.0 * 2.0*np.pi*x) + 0.5*np.sin(15.0 * 2.0*np.pi*x)

        >>> sp, ff = __fft(y,dt,window=True,normalize=False)

        '''

        from scipy.fft import fft, fftfreq, fftshift
        from scipy import signal

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
            spectrum_out = abs( spectrum / abs(spectrum).max()); print('Spectrum normalized \n')

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
        timeline = arange(0, len(trace_in), delta)
        l1 = "trace1"
        t0 = []
        
    if timeaxis is not None:
        timeline = timeaxis
        delta = timeline[1]-timeline[0]




    ## __________________________________________________________
    ## Plotting

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15,5))

    font = 13

    N = len(trace)    
    
    
    trace_fft, ff = __fast_fourier_transform(signal_in=trace, dt=delta , window=None, normalize=None)

    ax1.plot(timeline, trace, label=l1)

    ax2.plot(ff[:N // 2],abs(trace_fft[:N // 2]))

    ax1.set_xlabel(f"Time {t0} (s)", fontsize=font)
    ax1.set_ylabel(r"Amplitude $\frac{rad}{s}$", fontsize=font)

    ax1.legend(loc="upper right")
    
    ax2.set_xlabel("Frequency (Hz)", fontsize=font)
    ax2.set_ylabel(r"Amplitude Spectral Density ($\frac{rad}{s \sqrt{Hz} }$)", fontsize=font)

    if grid:
        ax1.grid(ls='--', zorder=-2, color='darkgrey')
        ax2.grid(ls='--', zorder=-2, color='darkgrey')
    
    if fmax:
        ax2.set_xlim(0, fmax)

    plt.show();

    return fig
