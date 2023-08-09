#!/usr/bin/python3
#
# calculate a polynomial fit for data
#
# by AndBro @2022
# __________________________

def __calculate_polynomial_fit(x_array, y_array, order_of_fit=2, gradient=False, smoothing=False, cc_shift=False):
    '''
    __calculate_polynomial_fit(x_array, y_array, order_of_fit=2, gradient=False, smoothing=False, cc_shift=False)
    
    INPUT: 
        - x_array:       data for x-axis as numpy array
        - y_array:       data for y-axis as numpy array
        - order_of_fit:  highest order of polynom
        - gradient:      bool
        - smoothing:     value of smoothing+
        - cc_shift:      cross-correlation lag 
    OUTPUT:
        - output directory
    '''
    
    import numpy.polynomial.polynomial as poly
    from numpy import gradient
    
    output = {}
    output['gradient'] = gradient
    output['order_of_fit'] = order_of_fit
    output['smoothing'] = smoothing
    
    ## apply time shift according to crosscorrelation lag
    if cc_shift:
        y_array = roll(y_array, -cc_shift)
    
    ## calcuate gradient, if selected
    if gradient:
        x_array = gradient(x_array, 2)
        
    ## smoothing gradient
    if smoothing:
        x_array = __smooth(x_array,  smoothing)

    ## get poly coefficients
    output['coefficients'] = poly.polyfit(x_array, y_array, order_of_fit)

    ## calulate polynomial function
    output['fit'] = poly.polyval(x_array, output['coefficients'])

    return output

## END OF FILE
