#!/bin/python


def __fft(signal_in, dt ,window=None,normalize=None):


	'''
	Calculating a simple 1D FastFourierSpectrum of a time series.

	Example:
	>>> N = 600
	>>> dt = 0.01
	>>> x = np.linspace(0.0, N*dt, N)
	>>> y = np.sin(10.0 * 2.0*np.pi*x) + 0.5*np.sin(15.0 * 2.0*np.pi*x)
	
	RETURN: 
	
	spectrum, frequencies, phase
	
	TEST: 
	
	>>> spectrum, frequencies, phase = __fft(signal_in, dt ,window=None,normalize=None)
	'''

	from scipy.fft import fft, fftfreq, fftshift
	from scipy import signal
	from numpy import angle
	    
	## determine length of the input time series
	n = int(len(signal_in))



	## calculate spectrum (with or without window function applied to time series)
	if window is None or window is False:
		spectrum = fft( signal_in )

	elif window == "hanning":
		window = signal.hann(n); print('Hanning window applied \n')
		spectrum = fft( signal_in * window )

	elif window == "kaiser":
		window = signal.kaiser(n, 8.6); print('Kaiser window (beta = 8.6) applied \n')
		#window = signal.gaussian(n, std=20); print('Gaussian window (std = 20) applied \n')
		spectrum = fft( signal_in * window )
		
	else:
		print("choose either 'hanning' or 'kaiser' as window")
		
	## calculate frequency array 
	frequencies = fftfreq(n, d=dt)
	

	## correct amplitudes of spectrum and optional normalize
	if normalize == None or normalize == False:
		spectrum_out = 2.0 / n * abs( spectrum )
	
	elif normalize == True:
		spectrum_out = abs( spectrum / abs(spectrum).max()); print('Spectrum normalized \n')

	## return the positive frequencies
	return spectrum_out[1:n//2], frequencies[1:n//2], angle( spectrum[1:n//2] )


