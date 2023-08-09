#!/usr/bin/python
#
# description
#
# by AndBro @2022
# __________________________


'''

VARIABLES:
 - psd_array		array
 - bins		int
 - density		bool 
 - y_log_scale		bool
 - axis		0 or 1 
 
DEPENDENCIES:


OUTPUT:
 - output	dictionary with several elements
 
EXAMPLE:

>>> __calculate_propabilistic_distribution(psd_array, bins=20, density=False, y_log_scale=False, axis=1)

'''

def __calculate_propabilistic_distribution(psd_array, bins=20, density=False, y_log_scale=False, axis=1):

    from numpy import argmax, std, median, isnan, array, histogram, nan, log10
    from scipy.stats import median_abs_deviation as mad
    
    ## exclude psds with only NaN values
    psd_array = array([psd0 for psd0 in psd_array if not isnan(psd0).all()])

    ## adjust for log scale
    if y_log_scale:
        psd_array = array([log10(psd0) for psd0 in psd_array])
    
    ## find overall minimum and maxium values
    max_value = max([max(sublist) for sublist in psd_array])
    min_value = min([min(sublist) for sublist in psd_array])

    
    ## define empty lists
    dist, dist_maximas, bins_maximas, bins_medians, stds, mads = [], [], [], [], [], []
    
    errors = 0
    for h in range(len(psd_array[axis])):
        
        psdx = psd_array[:,h]
        
        
        ## compute histograms
        hist, bin_edges = histogram(psdx, bins=bins, range=(min_value, max_value), density=density);
                
        ## center bins
        bin_mids = 0.5*(bin_edges[1:] + bin_edges[:-1])
#         bin_mids = bin_edges
        
        ## normalization
#         if  True:
#             hist = [val / len(psd_array[:,h]) for val in hist]
#             config['set_density'] = True

        ## check if density works
        DX = abs(max_value-min_value)/bins
        SUM = sum(hist)
        if str(round(SUM*DX,1)) != "1.0":
#            print(round(SUM*DX,1))
            errors+=1
        
        ## modify histogram with range increment
        hist = hist*DX
        
        ## append values to list
        dist.append(hist)
        stds.append(std(hist))
        dist_maximas.append(max(hist))
        bins_maximas.append(bin_mids[argmax(hist)])
        mads.append(mad(hist)) 
        
        ## compute median
        psdx = psdx[~(isnan(psdx))]
        bins_medians.append(median(psdx[psdx != 0]))
    
    ## adjust for log scale
    if y_log_scale:
        dist = array([10**(dd) for dd in array(dist)])
        bin_mids = 10**bin_mids
    
    ## undo log conversion    
    output = {}
    output['dist'] = array(dist)
    output['bin_mids'] = array(bin_mids)
    output['bins_maximas'] = array(bins_maximas)
    output['stds'] = array(stds)
    output['mads'] = array(mads)
    output['bins_medians'] = array(bins_medians)
    output['set_density'] = density
    output['total'] = psd_array.shape[0]
    
    if errors > 0:
        print(f" {errors} errors found for density computation!!!")
    
    return output

## End of File
