def __compare_psd_stream(st0, twin_sec=3600, psd="welch", time_bandwidth=None, n_win=5, plot=True):

    def __welch_psd(arr, dt, twin_sec=60):

        from scipy.signal import welch
        from scipy.signal.windows import hann

        nblock = int(1/dt * twin_sec)
        overlap = int(0.5*nblock)
        win = hann(nblock, True)

        ff, Pxx = welch(arr,
                        fs=1/dt,
                        window=win,
                        noverlap=overlap,
                        nfft=nblock,
                        scaling="density",
                        return_onesided=True)

        return ff, Pxx

    def __multitaper_psd(arr, dt, n_win=5, time_bandwidth=4.0):

        import multitaper as mt

        out_psd = mt.MTSpec(arr, nw=time_bandwidth, kspec=n_win, dt=dt, iadapt=2)

        _f, _psd = out_psd.rspec()

        f = _f.reshape(_f.size)
        psd = _psd.reshape(_psd.size)

        ## 95% confidence interval
        # _psd95 = out_psd.jackspec()
        # psd95_lower, psd95_upper = psd95[::2, 0], psd95[::2, 1]

        return f, psd

    fxxs, pxxs = {}, {}

    for tr in st0:

        seed = tr.get_id()

        if psd == "welch":
            fxxs[seed], pxxs[seed] = __welch_psd(tr.data, tr.stats.delta, twin_sec)
        elif psd == "multitaper":
            fxxs[seed], pxxs[seed] = __multitaper_psd(tr.data, tr.stats.delta, n_win=n_win, time_bandwidth=time_bandwidth)

    if plot:

        Nrow, Ncol = 1, 1

        font = 12

        fig, ax = plt.subplots(Nrow, Ncol, figsize=(15, 8))

        for tr in st0:

            ax.plot(fxxs[tr.get_id()], pxxs[tr.get_id()], label=tr.get_id())

        ax.set_xscale("log")
        ax.set_yscale("log")

        ax.grid(ls=":", zorder=0)
        ax.legend(loc=1)

        ax.set_xlim(1/twin_sec, 0.5/tr.stats.delta)

        ax.set_xlabel("Frequency (Hz")
        ax.set_ylabel("PSD")

        plt.show();

    return fxxs, pxxs
