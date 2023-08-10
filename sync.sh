#!/bin/bash

# syncronize own python methods (*.py files) with method file directory of python

rsync -u ${HOME}/andbro_python/*.py ${HOME}/anaconda3/lib/python3.7/site-packages

rsync -u ${HOME}/andbro_python/*.py ${HOME}/anaconda3/envs/obs/lib/python3.7/site-packages

rsync -u ${HOME}/andbro_python/*.py ${HOME}/anaconda3/envs/spy/lib/python3.7/site-packages
