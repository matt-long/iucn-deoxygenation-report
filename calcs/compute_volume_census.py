#! /usr/bin/env python
from config_calc import *
import proc_cesm_le


def volume_census(index_ens):

    #-------------------------------------------------------------------------------
    #-- load the data
    #-------------------------------------------------------------------------------

    print('\n'.join(['-'*80,'load data','-'*80,]))
    sc = 'tr85'
    op = 'ann_dft'

    v = 'O2'
    glob_patt = os.path.join(diro['work'],'%s.[0-9][0-9][0-9].%s.%s.1920-2100.nc'%(sc,op,v))
    files = sorted(glob(glob_patt))
    tr85 = xr.open_dataset(files[index_ens],decode_times=False,decode_coords=False)
    print tr85

    #-------------------------------------------------------------------------------
    #-- compute ocean volume
    #-------------------------------------------------------------------------------

    print('\n'.join(['-'*80,'compute volume','-'*80,]))
    tr85['VOL'] = et.pop_ocean_volume(tr85)
    print tr85

    #-------------------------------------------------------------------------------
    #-- bin by o2
    #-------------------------------------------------------------------------------

    print('\n'.join(['-'*80,'sum volumes','-'*80,]))
    tr85o = tr85.copy()
    tr85o['V60INT'] = tr85.VOL.where(tr85.O2 <= 60.).sum(dim=['z_t','nlat','nlon'])
    tr85o['V50INT'] = tr85.VOL.where(tr85.O2 <= 50.).sum(dim=['z_t','nlat','nlon'])
    tr85o['V5INT'] = tr85.VOL.where(tr85.O2 <= 5.).sum(dim=['z_t','nlat','nlon'])

    tr85o.V60INT.values = tr85o.V60INT.values * 1e-6
    tr85o.V60INT.attrs['units'] = 'm^3'

    tr85o.V50INT.values = tr85o.V50INT.values * 1e-6
    tr85o.V50INT.attrs['units'] = 'm^3'

    tr85o.V5INT.values = tr85o.V5INT.values * 1e-6
    tr85o.V5INT.attrs['units'] = 'm^3'

    tr85o = tr85o.drop([k for k in tr85o if k not in ['V60INT','V50INT','V5INT']])
    print tr85o

    #-------------------------------------------------------------------------------
    #--compute region mask
    #-------------------------------------------------------------------------------

    print('\n'.join(['-'*80,'write file','-'*80,]))
    file_out = os.path.join(diro['out'],'volume_timeseries.%s.ens_i_%03d.nc'%(op,index_ens))
    tr85o.to_netcdf(file_out,engine='scipy')#,format = NETCDF3_64BIT)
    print('done.')

if __name__ == '__main__':
    import sys
    ie = sys.argv[1]
    volume_census(index_ens=int(ie))
