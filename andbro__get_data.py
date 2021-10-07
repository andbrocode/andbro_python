#!/bin/python

def __get_data(path_name, file_name, head, delim, colnames):

	''' 
	retrieve data from file and store it as dataframe 

	dependencies: 
	import os 
	import pandas as pd
	    
	example: 
	get_data(path_name, file_name, head, delim, colnames)
	'''

	import pandas as pd

	## try to find and read mjd-files of ROMY
	try:

		df = pd.read_csv(path_name+file_name,delimiter=delim,header=head,names=colnames, error_bad_lines=False)

	except:
		raise('\n!!! ERROR IMPORTING!!! \n \n--> Possibliy file does not exist?!   {}\n'.format(path_name+file_name))
		return

	## print file name 
	print('\n reading   {} ... \n'.format(file_name))    


	## print top of file 
	print(f'{df.head(2)} \n')
	print(f'{df.tail(2)} \n')

	## print number of rows
	rows, cols = df.shape
	print('\n number of rows: {} \n number of columns: {} \n'.format(rows,cols))


	return df

