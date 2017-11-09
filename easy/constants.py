
T0_Kelvin = 273.15
rho_ref = 1026.
R_gasconst = 8.3144621 # J/mol/K

cp = 3985. # J/kg/K

g = 9.8
spd = 86400.
dps = 1./spd
dpy = 365.

boltz = 8.6173324E-5 # eV/K

epsTinv = 3.17e-8 # small inverse time scale: 1/year (1/sec)
epsC = 1.00e-8


mw = {'O2':   32.,
      'N2' :  28.,
      'Ne' :  20.,
      'Ar' :  40.,
      'Kr' :  84.,
      'Xe' : 131.}

def unit_db_to_Pa(value):
    return value * 1e4

def unit_atm_to_Pa(value):
    return value * 1.01325e5
