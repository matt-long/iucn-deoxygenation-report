import os
import sys
from glob import glob
from subprocess import call

path_tools = './subtree/easy-analysis'
sys.path.insert(0,os.path.abspath(os.path.expanduser(path_tools)))

from datetime import datetime
import xarray as xr
import numpy as np

import task_manager as tm
from regrid import regrid
from datasrc import cesm_le
import esm_tools as et

diro = {}
diro['out'] = '/glade/scratch/mclong/calcs/iucn-ch'
diro['work'] = '/glade/scratch/mclong/calcs/iucn-ch/work'
diro['tmp'] = '/glade/scratch/mclong/tmp/iucn-ch'
diro['fig'] =  '/glade/p/work/mclong/fig/iucn-ch'
diro['logs'] = './logs'

for pth in diro.values():
    if not os.path.exists(pth):
        call(['mkdir','-p',pth])
