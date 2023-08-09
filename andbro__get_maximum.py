#!/bin/python

def __get_maximum(x,y):
	'''finds maximum in y array and returns index, x(max) and y(max).
	
	dependency: 
		from numpy import array, where
	often used for annotation: 
	--> plt.annotate(f"{myy}",(mxx,myy), bbox=dict(fc="white", pad=0.5, ec="white"))
	'''
	from numpy import where, array

	Y = array(y)
	X = array(x)

	max_idx = where(Y==max(y))
	
	if len(max_idx) > 1:
		print(f"multiple maxima!! N = {len(max_idx)}")

	return int(max_idx[0]), float(x[max_idx]), float(y[max_idx])

