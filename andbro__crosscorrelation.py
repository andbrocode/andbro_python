#!/usr/bin/python3


def __crosscorrelation(y1, y2, plot=True, deltaT=None, labels=None):
    
    """Calculates the cross correlation and lags.

    PARAMETER:
        - y1, y2     data1, data2 [must be of same length]
        - plot       boolean 
        - deltaT     smpling time     
        - labels     labels of the data

    RETURN:
        output: dictionary 
           - output.ccorr:      Maximum correlation without normalization.
           - output.lag:        The lag in terms of the index.
           - output.maximum:    tuple of maxima location
           
    EXAMPLE:   
    >>> x = np.arange(0, 1000, 1)
    >>> y1 = np.sin(2*np.pi*0.01*x)* np.hanning(len(x))
    >>> y2 = np.roll(y1, -30)
    >>> out = __crosscorrelation(y1, y2, deltaT=1)
    """
    
    from scipy.signal import correlate
    from numpy import dot, ones, argmax, arange, roll, sqrt
    import matplotlib.pyplot as plt

    if len(y1) != len(y2):
        raise ValueError('The lengths of the inputs should be the same.')

    ## check if labels are passed
    if labels is None:
        labels = ["Data 1", "Data 2"]

    ## calulate autocorrelation
    y1_auto_corr = dot(y1, y1) / len(y1)
    y2_auto_corr = dot(y2, y2) / len(y1)
    
    
    ## calculate crorrelation function
    corr = correlate(y1, y2, mode='same')
    
    # The unbiased sample size is N - lag.
    unbiased_sample_size = correlate(ones(len(y1)), ones(len(y1)), mode='same')

    ## scaling
    corr = corr / unbiased_sample_size / sqrt(y1_auto_corr * y2_auto_corr)

    ## calculate lag times 
    xlags = arange(-corr.size//2, corr.size//2, 1)
    
    ## get maximum    
    corr_max_x = argmax(abs(corr))-corr.size//2
    corr_max_y = corr[int(corr_max_x + corr.size//2)]
    
    ## compute shifted signal
    shifted = roll(y2*corr_max_y, corr_max_x)
   
    shift = corr_max_x

    
    ## get time axis
    if deltaT is None:
        timeline = arange(0, len(y1))
    else:
        timeline = arange(0, len(y1)*deltaT, deltaT)
    
    ## Plotting
    if plot == True:
    
        font=13
        
        fig, ax = plt.subplots(3, 1, figsize=(15,8))

        plt.subplots_adjust(hspace=0.3)
        
        ax[0].plot(timeline, y1, label=labels[0], lw=0.9)

        ax[1].plot(timeline, y1, label=labels[0], lw=0.9)

        print(shift)

        if shift>=0:
            ax[1].plot(timeline[abs(shift):], shifted[abs(shift):], label=f"{labels[1]} shifted", lw=0.9)
        elif shift<0:
            ax[1].plot(timeline[:-abs(shift)], shifted[:-abs(shift)], label=f"{labels[1]} shifted", lw=0.9)
            
        ax[0].set_xlim(min(timeline), max(timeline))        
        ax[1].set_xlim(min(timeline), max(timeline))

        ax[2].plot(xlags, corr, color="black", lw=0.9, label="CC-Function")

        ax[2].scatter(corr_max_x, corr_max_y, color='orange', zorder=3, label=f'x:{round(corr_max_x*deltaT,1)}s y:{round(corr_max_y,2)}')

        ax[2].axvline(corr_max_x, color='k', ls=":")
        ax[2].axhline(corr_max_y, color='k', ls=":")
        ax[2].set_xlim(min(xlags), max(xlags))
        
        for i in range(3):
            ax[i].grid(ls=":", zorder=1)
            ax[i].legend(loc="upper right",fontsize=font-1)

        ax[0].set_ylabel("Amplitude",fontsize=font)
        ax[1].set_ylabel("Amplitude",fontsize=font)
        ax[2].set_ylabel("CC value",fontsize=font)
        
        ax[0].set_xlabel("Time (s)",fontsize=font)
        ax[1].set_xlabel("Time (s)",fontsize=font)
        ax[2].set_xlabel("Cross-correlation Lag (samples)",fontsize=font)
            
        plt.show();

    output={}
    output['ccorr'] = corr
    output['xlags'] = xlags
    output['maximum'] = (corr_max_x, corr_max_y)
    
    if plot:
        output['figure'] = fig    

    print(f"Maximum Correlation: \n x: {corr_max_x} \n y: {round(corr_max_y,2)}")

    return output

## END OF FILE
