#!/bin/python



from numpy import isnan, ones, nan

def __create_NAN_masks(st):
	''' 
	Subsituting NaN values in data with zeros for e.g. processing and providing mask of ones and nan values. By multiplying the 		mask with the data after processing one regains the nan values.

	st: 		stream with data

	Example:
	__create_NAN_masks(st)

	''' 
    masks, masks_count = [], 0

    for tr in st:
        if isnan(tr.data).any():
            mask = ones(len(tr.data))
            for i, e in enumerate(tr.data): 
                if isnan(e):
                    tr.data[i] = 0
                    mask[i] = nan
            masks.append(mask)
            masks_count += 1
        else: 
            masks.append([])
            
    if masks_count == 0:
        print("\n   -> no mask(s) created")
    else:
        print(f"\n   -> created {masks_count} mask(s) for NaN values")

    return st, masks

## END OF FILE
