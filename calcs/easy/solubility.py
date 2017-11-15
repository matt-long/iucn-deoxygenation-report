#! /usr/bin/env python
import numpy as np

#-------------------------------------------------------------------------------
#-- FUNCTION
#-------------------------------------------------------------------------------

def _garcia_gordon_polynomial(S,T,
                              A0 = 0., A1 = 0., A2 = 0., A3 = 0., A4 = 0., A5 = 0.,
                              B0 = 0., B1 = 0., B2 = 0., B3 = 0.,
                              C0 = 0.):

    T_scaled = np.log((298.15 - T) /(273.15 + T))
    return np.exp(A0 + A1*T_scaled + A2*T_scaled**2. + A3*T_scaled**3. + A4*T_scaled**4. + A5*T_scaled**5. + \
                  S*(B0 + B1*T_scaled + B2*T_scaled**2. + B3*T_scaled**3.) + C0 * S**2.)

#-------------------------------------------------------------------------------
#-- FUNCTION
#-------------------------------------------------------------------------------

def _umolkg_to_mmolm3(value):
    from constants import rho_ref
    return value * rho_ref / 1000.

#-------------------------------------------------------------------------------
#-- FUNCTION
#-------------------------------------------------------------------------------

def O2(S,T,**kwargs):
    '''
    Solubility of O2 in sea water
    INPUT:
    S = salinity    [PSS]
    T = temperature [degree C]

    conc = solubility of O2 [mmol/m^3]

    REFERENCE:
    Hernan E. Garcia and Louis I. Gordon, 1992.
    "Oxygen solubility in seawater: Better fitting equations"
    Limnology and Oceanography, 37, pp. 1307-1312.
    '''

    # constants from Table 4 of Hamme and Emerson 2004
    conc = _garcia_gordon_polynomial(S,T,
                                     A0 = 5.80871,
                                     A1 = 3.20291,
                                     A2 = 4.17887,
                                     A3 = 5.10006,
                                     A4 = -9.86643e-2,
                                     A5 = 3.80369,
                                     B0 = -7.01577e-3,
                                     B1 = -7.70028e-3,
                                     B2 = -1.13864e-2,
                                     B3 = -9.51519e-3,
                                     C0 = -2.75915e-7)
    return _umolkg_to_mmolm3(conc)

#-------------------------------------------------------------------------------
#-- FUNCTION
#-------------------------------------------------------------------------------

def O2_Kh(S,T,Z):
    '''This function computes solubility of O2 in seawater
    The solubility (Kh) is based on Henry's Law, but includes a
    correction for the effect of hydrostatic pressure of the water column.
    This allows the partial pressure of O2 to be computed at depth from
        pO2 = O2 / Kh
    The relevant equation is (see Enns et al., J. Phys. Chem. 1964)
    d(ln p)/dP = V/RT
    where p = partial pressure of O2, P = hydrostatic pressure
    V = partial molar volume of O2, R = gas constant, T = temperature
    '''

    import constants
    import atm_mixing_ratio
    from seawater.eos80 import pres as sw_pres

    XO2 = atm_mixing_ratio.O2
    Patm = 1.

    V = 32e-6 # partial molar volume of O2 (m3/mol)
    R = constants.R_gasconst

    #-- compute pressure correction
    # Warning - z*0 neglects gravity differences w/ latitude
    P = sw_pres(Z,Z*0.); # seawater pressure [db]
    dP = constants.unit_db_to_Pa(P)

    pCor = np.exp(V * dP / (R * ( T + constants.T0_Kelvin )))

    #-- solubility with pressure correction
    Kh0 = O2(S,T) / (Patm * XO2) # solubility at surface (atm) pressure [mmol/m3/atm]
    return Kh0 * pCor

#-------------------------------------------------------------------------------
#-- FUNCTION
#-------------------------------------------------------------------------------

def CFC12(S,T):
    return _calc_cfcsol(S,T,12)

#-------------------------------------------------------------------------------
#-- FUNCTION
#-------------------------------------------------------------------------------

def CFC11(S,T):
    return _calc_cfcsol(S,T,11)

#-------------------------------------------------------------------------------
#-- FUNCTION
#-------------------------------------------------------------------------------

def _calc_cfcsol(PS,PT,kn):
    '''
    FUNCTION: calc_cfcsol
    CFC 11 and 12 Solubilities in seawater
    ref: Warner & Weiss (1985) , Deep Sea Research, vol32
    translated from cfc11_mod.F90 (MCL, 2011)
    INPUT:
    PT: temperature (degree Celsius)
    PS: salinity
    kn: 11 = CFC11, 12 = CFC12
    OUTPUT:
    SOLUBILITY_CFC: returned value in mol/m3/pptv
    1 pptv = 1 part per trillion = 10^-12 atm = 1 picoatm
    '''
    T0_Kelvin = 273.16
    c1000     = 1000.0

    if kn == 11:
      a1 = -229.9261
      a2 =  319.6552
      a3 =  119.4471
      a4 =   -1.39165
      b1 =   -0.142382
      b2 =    0.091459
      b3 =   -0.0157274
    elif kn == 12:
      a1 = -218.0971
      a2 =  298.9702
      a3 =  113.8049
      a4 =   -1.39165
      b1 =   -0.143566
      b2 =    0.091015
      b3 =   -0.0153924
    else:
      print('error')
      sys.exit(1)

    WORK = ((PT + T0_Kelvin) * 0.01)

    #-----------------------------------------------------------------------
    #  coefficient for solubility in  mol/l/atm
    #-----------------------------------------------------------------------

    SOLUBILITY_CFC = np.exp( a1 + a2 / WORK + a3 * np.log ( WORK )
                           + a4 * WORK * WORK
                           + PS * ( ( b3 * WORK + b2 ) * WORK + b1 ) )

    #-----------------------------------------------------------------------
    #  conversion from mol/(l * atm) to mol/(m^3 * atm) to mol/(m3 * pptv)
    #-----------------------------------------------------------------------

    SOLUBILITY_CFC = c1000 * SOLUBILITY_CFC
    SOLUBILITY_CFC = 1.0e-12 * SOLUBILITY_CFC

    return SOLUBILITY_CFC # mol/m^3/patm

#-------------------------------------------------------------------------------
#--- main
#-------------------------------------------------------------------------------
if __name__ == '__main__':

    print CFC12(35.,15.)
    print CFC11(35.,15.)
