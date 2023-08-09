#!/usr/bin/python3
#
# calculate a polynomial fit for data
#
# by AndBro @2022
# __________________________

def __calculate_linear_regression(x_array, y_array, odr_mode=None, odr_std=[None, None], derive=None, smoothing=None, cc_shift=None):
    '''
    __calculate_linear_regression(x_array, y_array, odr=None, odr_std=[None, None] derive=None, smooth=None)
  
    INPUT: 
        - x_array:       data for x-axis as numpy array
        - y_array:       data for y-axis as numpy array
        - gradient:      bool
        - smoothing:     value of smoothing+
        - odr_mode:      select orthogonal distance regression (ODR) instead of linear regression
        - odr_std:       standard deviations for x-axis data and y-axis data [std_x, std_y]
        - cc_shift:      cross-correlation lag 
    OUTPUT:
        - output:        dictionary with output values and information
    '''
    
    from scipy import odr
    from numpy import gradient, roll, power, ones, convolve
    
    def __smooth(y, box_pts):
        box = ones(box_pts)/box_pts
        y_smooth = convolve(y, box, mode='same')
        return y_smooth
    
    def f(B, x):
        '''Linear function y = m*x + b'''
        return B[0]*x + B[1]

    ## avoid error change to dummy
    if odr_std[0] is None and odr_std[1] is None:
        odr_std = [1,1]
        
    ## define output dictionary
    output = {}
    output['gradient']  = gradient
    output['smoothing'] = smoothing
    output['cc_shift']  = cc_shift
    
    ## apply time shift according to crosscorrelation lag
    if cc_shift is not None:
        y_array = roll(y_array, -cc_shift)
    
#     ## calcuate gradient, if selected
    if derive is not None:
        x_array = gradient(x_array, 2)
        
#     ## smoothing gradient
    if smoothing is not None:
        x_array = __smooth(x_array,  smoothing)

    if odr_mode is not None: 
        sx, sy = odr_std[0], odr_std[1]
        linear = odr.Model(f)
        mydata = odr.Data(x_array, y_array, wd=1./power(sx,2), we=1./power(sy,2))
        myodr = odr.ODR(mydata, linear, beta0=[1e-8, 1e-8])
        myoutput = myodr.run()
        
        output['slope'] = myoutput.beta[0]
        output['intercept'] = myoutput.beta[1]
        
    else:
        linreg = scipy.stats.linregress(x_array, y_array)
        output['slope'] = linreg.slope
        output['intercept'] = linreg.intercept

    return output

## END OF FILE
