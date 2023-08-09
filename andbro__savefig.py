#!/bin/python


def __savefig(figs, outpath=None, outname=None, mode=None, dpi=None):
	''' 
	Saving figures in array figs continously to pdf-file

	figs: 		list of several or single figure object    
	outpath:	path to save figs to
	outname: 	name of saved figure
    mode:       type of figure [pdf, png]
    dpi:        resolution of figure (default: 300)

	Example:
	__save_to([fig], '/test/' , 'test', mode='pdf' , dpi=None)

	''' 
	from matplotlib.backends.backend_pdf import PdfPages
	from datetime import datetime
	from os import path

	## define default parameters
	date = str(datetime.now().date())
	t = str(datetime.now().time())

	
	if outpath is None:
		outpath="/home/brotzer/notebooks/figs/"
	if outname is None:
		outname=f"test_{date}_{t[0:2]+t[3:5]+t[6:8]}"
	if mode is None:
		mode = "pdf"
	if dpi is None:
		dpi = 300
		

	## check if figs is a LIST
	if type(figs) is list:

		if mode == 'pdf':
			print('\n saving pdf to {}{}.{}... \n'.format(outpath,outname,mode)) 
			pdf = PdfPages("{}{}.pdf".format(outpath,outname))				
			for f in figs: 
				pdf.savefig(f , bbox_inches='tight', pad_inches=0.1)
				pdf.close()

		elif mode == 'png':
			print(f'\n   -> saving {outpath}{outname}.{mode} ...\n')
			for f in figs: 
				f.savefig(f"{outpath}{outname}.{mode}", dpi=dpi, facecolor='w', edgecolor='w', orientation='portrait', format='png', transparent=False , bbox_inches='tight', pad_inches=0.1)
		else:
			print('\n   -> mode not correct!')
	

	## check if figs is a FIGURE OBJECT
	elif str(type(figs)) == "<class 'matplotlib.figure.Figure'>":


		if mode == 'pdf':
			print('\n   -> saving pdf to {}{}.{}... \n'.format(outpath,outname,mode)) 
			pdf = PdfPages("{}{}.pdf".format(outpath,outname))				
			pdf.savefig( figs , bbox_inches='tight', pad_inches=0.1)
			pdf.close()

		elif mode == 'png':
			print(f'\n   -> saving {outpath}{outname}.{mode} ...\n')
			figs.savefig(f"{outpath}{outname}.{mode}", dpi=dpi, facecolor='w', edgecolor='w', orientation='portrait', format='png', transparent=False , bbox_inches='tight', pad_inches=0.1)
		
		else:
			print('\n   -> mode not correct!')

	if path.isfile(f"{outpath}{outname}.{mode}"):
		print("   -> Done\n")
	else:
		print("   -> Something failed while saving\n")		

## END OF FILE
