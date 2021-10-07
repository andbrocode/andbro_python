#!/bin/python

#def __save_to(figs, outpath, outname, mode):
def __save_to(figs, outpath=None ,  outname=None, mode=None):
	''' 
	Saving figures in array figs continously to pdf-file

	figs: 		list of several or single figure object    
	outpath:	path to save figs to
	outname: 	name of saved figure

	Example:
	__save_to([fig], outpath='/test/' , outname='test', mode='pdf')

	''' 
	from matplotlib.backends.backend_pdf import PdfPages
	from datetime import datetime


	## define default parameters
	default_opath="/home/brotzer/notebooks/figs/"
	default_mode = "pdf"
	
	date = str(datetime.now().date())
	t = str(datetime.now().time())
	time = t[0:2]+t[3:5]+t[6:8]

	
	
	## start user interaction
	save = input('\n* SAVE FIGURE (y/n) ??:  ')

	if save == 'y':
		
		## check for alternative output PATH
		outpath = input(f'\n* Enter path (default: {default_opath}): ')
		if len(outpath) == 0:
			outpath = default_opath
		if outpath[-1] != "/":
			outpath = f"{outpath}/"
		## check for alternative output NAME
		outname = input(f'\n* Enter name (default: ROMY_{date}_{time}): ')
		if len(outname) == 0:
			outname = 'ROMY_{}_{}'.format(str(date),str(time))
			outname = outname.replace(' ','_')    
		
		## check for alternative FORMAT
		mode    = input('\n* Enter format (default: pdf): ')
		if len(mode) == 0:
			mode = default_mode


		
		## check if figs is a LIST
		if type(figs) is list:

			if mode == 'pdf':
				print(f'\n saving {mode} to {outpath}{outname}.{mode}...') 
				pdf = PdfPages("{}{}.pdf".format(outpath,outname))				
				for f in figs: 
					pdf.savefig( f, 
					             bbox_inches='tight',
					             pad_inches=0.15, 
					             )
					pdf.close()

			elif mode == 'png':
				print(f'\n saving {mode} to {outpath}{outname}.{mode}...\n')
				for f in figs: 
					f.savefig(outpath+outname+".png", 
					          dpi=300, 
					          facecolor='w',
					          edgecolor='w', 
					          orientation='portrait',
					          papertype='A4', 
					          format='png', 
					          transparent=False, 
					          bbox_inches='tight', 
					          pad_inches=0.15, 
					          )
			else:
				print('mode not correct!')
		

		## check if figs is a FIGURE OBJECT
		elif str(type(figs)) == "<class 'matplotlib.figure.Figure'>":


			if mode == 'pdf':
				print(f'\n saving {mode} to {outpath}{outname}.{mode}... \n') 
				pdf = PdfPages("{}{}.pdf".format(outpath,outname))				
				pdf.savefig( figs, 
				             bbox_inches='tight', 
				             pad_inches=0.15, 
				             )
				pdf.close()

			elif mode == 'png':
				print(f'\n saving {mode} to {outpath}{outname}.{mode}...\n')
				figs.savefig( outpath+outname+".png", 
				              dpi=300, 
				              facecolor='w', 
				              edgecolor='w', 
				              orientation='portrait',
				              papertype='A4',
				              format='png', 
				              transparent=False, 
				              bbox_inches='tight', 
				              pad_inches=0.15, 
				              )
			
			else:
				print('mode not correct!')


	else: 
		print('*\n* Figure discared!\n*')


# END OF FILE
