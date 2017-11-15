#! /usr/bin/env python
from config_calc import *
import proc_cesm_le


def tropical_hilat(index_ens):

    #-------------------------------------------------------------------------------
    #-- load the data
    #-------------------------------------------------------------------------------

    print('\n'.join(['-'*80,'load data','-'*80,]))
    sc = 'tr85'
    op = 'ann_dft'

    varlist = ['O2','AOU','TEMP','IAGE']
    dsi = []
    for v in varlist:
        glob_patt = os.path.join(diro['work'],'%s.[0-9][0-9][0-9].%s.%s.1920-2100.nc'%(sc,op,v))
        files = sorted(glob(glob_patt))
        dsi.append(xr.open_dataset(files[index_ens],decode_times=False,decode_coords=False))
    tr85 = xr.merge(dsi)

    if 'AOU' in tr85:
        v = 'O2sat'
        tr85[v] = tr85.AOU + tr85.O2
        varlist.append(v)

    #-- xarry bug: there's some inconsistency with chunksizes
    #   I can't write the file resulting from the computation below:
    #   https://github.com/pydata/xarray/issues/1225
    #   related: https://github.com/pydata/xarray/issues/1458
    # using `engine=scipy` as a workaround.
    print tr85

    #-------------------------------------------------------------------------------
    #--compute region mask
    #-------------------------------------------------------------------------------

    nz = tr85.z_t.shape[0]
    nlat = tr85.KMT.shape[0]
    nlon = tr85.KMT.shape[1]
    zmask = xr.DataArray(np.ones(nz),dims='z_t')

    rmask = xr.DataArray(np.zeros((3,nz,nlat,nlon)),dims=('region','z_t','nlat','nlon'))
    rmask[0,:,:,:] = np.where(tr85.KMT > 0, 1., 0.)
    rmask[1,:,:,:] = np.where((np.abs((tr85.TLAT)) <= 20.) & (tr85.KMT > 0), 1., 0.)
    rmask[2,:,:,:] = np.where((np.abs((tr85.TLAT)) > 20.) & (tr85.KMT > 0), 1., 0.)

    zmask = (tr85.z_t.where(tr85.z_t < 1000e2)/tr85.z_t.where(tr85.z_t < 1000e2)).fillna(0)
    rmask = rmask * zmask
    rmask = rmask.transpose('region','z_t','nlat','nlon')
    print rmask

    #-------------------------------------------------------------------------------
    #--compute region mask
    #-------------------------------------------------------------------------------

    file_out = os.path.join(diro['out'],'region_0glb_1trp_2hlt_upper1000m.%s.ens_i_%03d.nc'%(op,index_ens))

    tr85r = et.pop_calc_spatial_mean(tr85.copy(),avg_over_dims=['z_t','nlat','nlon'],
                                     region_mask=rmask)
    print tr85r

    tr85r.to_netcdf(file_out,engine='scipy')
    print '-'*80
    print
    print

    #-------------------------------------------------------------------------------
    #--compute region mask
    #-------------------------------------------------------------------------------

    nlat = tr85.KMT.shape[0]
    nlon = tr85.KMT.shape[1]

    rmask = xr.DataArray(np.zeros((3,nlat,nlon)),dims=('region','nlat','nlon'))
    rmask[0,:,:] = np.where(tr85.KMT > 0, 1., 0.)
    rmask[1,:,:] = np.where((np.abs((tr85.TLAT)) <= 20.) & (tr85.KMT > 0), 1., 0.)
    rmask[2,:,:] = np.where((np.abs((tr85.TLAT)) > 20.) & (tr85.KMT > 0), 1., 0.)

    print rmask

    #-------------------------------------------------------------------------------
    #--compute region mask
    #-------------------------------------------------------------------------------

    file_out = os.path.join(diro['out'],'region_0glb_1trp_2hlt_profile.%s.ens_i_%03d.nc'%(op,index_ens))
    tr85r = et.pop_calc_spatial_mean(tr85.copy(),avg_over_dims=['nlat','nlon'],
                                     region_mask=rmask)
    print tr85r

    tr85r.to_netcdf(file_out,engine='scipy')#,format = NETCDF3_64BIT)
    print('done.')

if __name__ == '__main__':
    import sys
    ie = sys.argv[1]
    tropical_hilat(index_ens=int(ie))
