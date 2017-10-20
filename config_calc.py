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
import task_manager as tm
from regrid import regrid
from datasrc import cesm_le
import esm_tools as et
easy = et.__file__

#-- directories
calc_name = 'iucn-ch'
diro = {}
diro['out'] = '/glade/scratch/'+os.environ['USER']+'/calcs/'+calc_name
diro['work'] = '/glade/scratch/'+os.environ['USER']+'/calcs/'+calc_name+'/work'
diro['tmp'] = '/glade/scratch/'+os.environ['USER']+'/tmp'
diro['fig'] =  '/glade/p/work/'+os.environ['USER']+'/fig/'+calc_name
diro['logs'] = './logs'

for pth in diro.values():
    if not os.path.exists(pth):
        call(['mkdir','-p',pth])
