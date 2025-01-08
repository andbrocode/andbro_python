def __crosscorrelationTraces(tr1, tr2, plot=True):

    """Calculates the cross correlation and lags.

    PARAMETER:
        - tr1, tr2     trace1, trace2 [must be of same length]
        - plot         boolean

    RETURN:
        output: dictionary
           - output['ccor']r:      Maximum correlation without normalization.
           - output['lag']:        The lag in terms of the index.
           - output['maximum']:    tuple of maxima location

    """

    from scipy.signal import correlate
    from numpy import dot, ones, argmax, arange, roll, sqrt
    import matplotlib.pyplot as plt

    y1 = tr1.data
    y2 = tr2.data

    deltaT = tr1.stats.delta

    if len(y1) != len(y2):
        raise ValueError('The lengths of the inputs should be the same.')

    # check if labels are passed
    labels = [tr1.get_id(), tr2.get_id()]

    # calulate autocorrelation
    y1_auto_corr = dot(y1, y1) / len(y1)
    y2_auto_corr = dot(y2, y2) / len(y1)

    # calculate crorrelation function
    corr = correlate(y1, y2, mode='same')

    # The unbiased sample size is N - lag.
    unbiased_sample_size = correlate(ones(len(y1)), ones(len(y1)), mode='same')

    # scaling
    corr = corr / unbiased_sample_size / sqrt(y1_auto_corr * y2_auto_corr)

    # calculate lag times
    xlags = arange(-corr.size//2, corr.size//2, 1)

    # get maximum
    corr_max_x = argmax(abs(corr))-corr.size//2
    corr_max_y = corr[int(corr_max_x + corr.size//2)]

    # compute shifted signal
    shifted = roll(y2*corr_max_y, corr_max_x)

    shift = corr_max_x

    # get time axis
    if deltaT is None:
        timeline = arange(0, len(y1))
    else:
        timeline = arange(0, len(y1)*deltaT, deltaT)

    # Plotting
    if plot:

        font = 13

        fig, ax = plt.subplots(3, 1, figsize=(15, 8))

        plt.subplots_adjust(hspace=0.3)

        ax[0].plot(timeline, y1, label=labels[0], lw=0.9)

        ax[1].plot(timeline, y1, label=labels[0], lw=0.9)

        if shift >= 0:
            ax[1].plot(timeline[abs(shift):], shifted[abs(shift):], label=f"{labels[1]} shifted", lw=0.9, zorder=2)
        elif shift < 0:
            ax[1].plot(timeline[:-abs(shift)], shifted[:-abs(shift)], label=f"{labels[1]} shifted", lw=0.9, zorder=2)

        ax[0].set_xlim(min(timeline), max(timeline))
        ax[1].set_xlim(min(timeline), max(timeline))

        ax[2].plot(xlags, corr, color="black", lw=0.9, label="CC-Function", zorder=2)

        ax[2].scatter(corr_max_x, corr_max_y, color='darkred',
                      zorder=1, label=f'x:{round(corr_max_x*deltaT, 1)}s y:{round(corr_max_y, 2)}')

        ax[2].axvline(corr_max_x, color='darkred', ls=":")
        ax[2].axhline(corr_max_y, color='darkred', ls=":")
        ax[2].set_xlim(min(xlags), max(xlags))

        for i in range(3):
            ax[i].grid(ls=":", zorder=1)
            ax[i].legend(loc="upper right", fontsize=font-1)

        ax[0].set_ylabel("Amplitude", fontsize=font)
        ax[1].set_ylabel("Amplitude", fontsize=font)
        ax[2].set_ylabel("CC value", fontsize=font)

        ax[0].set_xlabel("Time (s)", fontsize=font)
        ax[1].set_xlabel("Time (s)", fontsize=font)
        ax[2].set_xlabel("Cross-correlation Lag (samples)", fontsize=font)

        plt.show();

    output = {}
    output['ccorr'] = corr
    output['xlags'] = xlags
    output['maximum'] = (corr_max_x, corr_max_y)

    if plot:
        output['figure'] = fig

    print(f"Maximum Correlation: \n x: {corr_max_x}s \n y: {round(corr_max_y,2)}")

    return output
