#! /usr/bin/env python
from config_calc import *

nens = 33
for i in range(nens):
    jid = tm.submit(['compute_regional_means.py','%d'%i],bset_in={'q':'geyser','m':'300000'})

tm.wait()
