import numpy as np

rho_ref = 1026.

def _garcia_gordon_polynomial(S,T,
                              A0 = 0., A1 = 0., A2 = 0., A3 = 0., A4 = 0., A5 = 0.,
                              B0 = 0., B1 = 0., B2 = 0., B3 = 0.,
                              C0 = 0.):

    T_scaled = np.log((298.15 - T) /(273.15 + T))
    return np.exp(A0 + A1*T_scaled + A2*T_scaled**2. + A3*T_scaled**3. + A4*T_scaled**4. + A5*T_scaled**5. + \
                  S*(B0 + B1*T_scaled + B2*T_scaled**2. + B3*T_scaled**3.) + C0 * S**2.)

def _umolkg_to_mmolm3(value):
    return value * rho_ref / 1000.

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
