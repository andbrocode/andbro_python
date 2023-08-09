#!/usr/bin/python3

from IPython.display import clear_output
from matplotlib import pyplot as plt
    
def __live_plot(x, y, figsize=(7,5), title=''):
    
    clear_output(wait=True)
    plt.figure(figsize=figsize)

    x= [float(i) for i in x]
    y= [float(i) for i in y]
    
    if len(x) > 1:
        plt.scatter(x,y, label='axis y', color='k', s=0.9) 
        
#         m, b = np.polyfit(x, y, 1)
#         plt.plot(x, [x * m for x in x] + b)

    plt.title(title)
#     plt.grid(True)
    plt.xlabel('axis x')
    plt.ylabel('axis y')
    plt.show();
    
## END OF FILE
