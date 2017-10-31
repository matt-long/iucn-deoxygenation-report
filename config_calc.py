#-- os interaction
import os
import sys
from glob import glob
from subprocess import call

#-- path additions
path_tools = ['./easy']
for p in path_tools:
    sys.path.insert(0,os.path.abspath(os.path.expanduser(p)))

#-- analysis
from datetime import datetime
import xarray as xr
import numpy as np

#-- easy
import esm_tools as et
easy = et.__file__.replace('.pyc','.py')

#-- machine
hostname = os.environ['HOSTNAME']
if 'cgd.ucar.edu' in hostname:
    scratch = '/project/oce/mclong/scratch'
else:
    import task_manager as tm
    from regrid import regrid
    from datasrc import cesm_le
    scratch = '/glade/scratch/'+os.environ['USER']

#-- directories
calc_name = 'iucn-ch'
diro = {}
diro['out'] = os.path.join(scratch,'calcs',calc_name)
diro['work'] = os.path.join(scratch,'calcs',calc_name,'work')
diro['tmp'] = os.path.join(scratch,'tmp')
diro['fig'] =  './ms/fig'
diro['logs'] = './logs'

for pth in diro.values():
    if not os.path.exists(pth):
        call(['mkdir','-p',pth])
