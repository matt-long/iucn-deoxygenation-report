#! /usr/bin/env python
from config_calc import *


nens = 33

#-- compute trends
if False:
    for i in range(nens):
        jid = tm.submit(['compute_toe_trends.py','compute_trends','%d'%i],bset_in={'q':'geyser','m':'60000'})
    tm.wait()

#-- compute std
if False:
    jid = tm.submit(['compute_toe_trends.py','compute_std'],bset_in={'q':'geyser','m':'60000'})
    tm.wait()

#-- compute std
if True:
    for i in range(nens):
        jid = tm.submit(['compute_toe_trends.py','compute_toe','%d'%i],bset_in={'q':'geyser','m':'60000'})
    tm.wait()
