#!/usr/bin/python
#
# description
#
# by AndBro @2022
# __________________________

def __estimate_linear_trend(x_arr, y_arr, derive=None, smooth=None, relative=None, set_odr=None):
    
    '''
    
    >>> output = __estimate_linear_trend(x, y, derive=None, smooth=None, relative=None, odr=None)
  
    INPUT: 
        - x_array:       array: data for x-axis as numpy array
        - y_array:       array: data for y-axis as numpy array 
        - derive:        bool: (if x is derived or not) 
        - smooth:        integer: degree of smoothing 
        - relative:      bool: relative to x[0]
        - odr:           bool: select orthogonal distance regression (ODR) instead of linear regression

        
    OUTPUT:
        - output:        dictionary with output values and information
        
    '''
    
    from scipy import odr
    from scipy.stats import linregress
    from numpy import gradient, power
    
    ## prepare output dictionary
    output = {}
    
    if derive:
        x_arr = gradient(x_arr, 2)
        
    if smooth:
        x_arr = __smooth(x_arr, smooth)

    if relative:
        x_arr -= x_arr[1]
        
    ## compute linear regression of data
    out = linregress(x_arr, y_arr)    
    
    ## extract to output
    output['slope'] = out.slope
    output['intercept'] = out.intercept  
    

    
    ## use an orthogonal distance regression (odr) for trend estimate
    if set_odr is not None:
        
        def f(B, x):
            '''Linear function y = m*x + b'''
            return B[0]*x + B[1]   
        
        s_x, s_y = 1, 1
        print(f" -> std x and y set to: {s_x} and {s_y}")

        beta_x, beta_y = 1e-8, 1e-8
        print(f" -> beta x and y set to: {beta_x} and {beta_y}")

        linear = odr.Model(f)
        mydata = odr.Data(x_arr, y_arr, wd=1./power(s_x,2), we=1./power(s_y,2))
        myodr = odr.ODR(mydata, linear, beta0=[beta_x, beta_y])
        myoutput = myodr.run()
    
        ## extract to output        
        output['slope'] = myoutput.beta[0]
        output['intercept'] = myoutput.beta[1]
    
    
    return output


## End of File
