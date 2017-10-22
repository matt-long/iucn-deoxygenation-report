#! /usr/bin/env python
#BSUB -P NCGD0011
#BSUB -W 24:00
#BSUB -n 1
#BSUB -J toe-map
#BSUB -o logs/toe-map.%J
#BSUB -e logs/toe-map.%J
#BSUB -q geyser
#BSUB -N

from config_calc import *
import proc_cesm_le
import time

'''
To evaluate ToE on the basis of changes in trend magnitude in the CESM-LE, we
compute retrospective linear trends in each ensemble member starting at the year
2000 and continuing through the year 2100. For each year, we compute linear
trends over record lengths from 10 to 100 years. We normalize the trends
computed at each year and record length by the standard deviation of trends
within the full CESM-LE, yielding a signal-to-noise ratio estimate. We then
diagnose ToE as the earliest year in which a trend of any length is more than
2$\sigma$ outside the variability in trends across the ensemble and does not
return to within 2$\sigma$ for all remaining years in the simulation.
'''
v = 'O2'
file_std = os.path.join(diro['out'],'toe_thermocline.%s.std.nc'%v)


#--------------------------------------------------------------------------------
#---- class
#--------------------------------------------------------------------------------

class timer(object):
    def __init__(self, name=None):
        self.name = name
    def __enter__(self):
        self.tstart = time.time()
        if self.name:
            print('\n'.join(['-'*80,'%s'%self.name,'-'*80,'']))
    def __exit__(self, type, value, traceback):
        print('Elapsed: %s' % (time.time() - self.tstart))
        print

#-------------------------------------------------------------------------------
#-- function
#-------------------------------------------------------------------------------

def compute_trends(index_ens=None):

    #-- load the data
    print('\n'.join(['-'*80,'load data','-'*80,]))
    varlist = ['O2','AOU']
    tr85 = proc_cesm_le.open_ens('tr85','ann_dft',varlist,
                                 sel={'z_t':slice(200e2,600e2)})

    if 'AOU' in tr85:
        v = 'O2sat'
        tr85[v] = tr85.AOU + tr85.O2
        varlist.append(v)

    if index_ens is not None:
        tr85 = tr85.isel(ens=index_ens)
    print tr85

    #-------------------------------------------------------------------------------
    #-- take mean over depth
    #-------------------------------------------------------------------------------

    print('\n'.join(['','-'*80,'compute thermocline','-'*80,]))
    tr85_tc = tr85.mean(dim='z_t')

    if index_ens is not None:
        tr85_tc = tr85_tc.compute()
    print tr85_tc

    #-------------------------------------------------------------------------------
    #-- set-up trend arrays
    #-------------------------------------------------------------------------------

    print('\n'.join(['','-'*80,'set-up trend arrays','-'*80,]))
    min_yr = 1920
    trnd_lngth = xr.DataArray(np.arange(10,81,1),dims=('trend_length'))
    trnd_yr = xr.DataArray(np.arange(2000,2101,1),dims=('time'))

    n_trnd = len(trnd_lngth)
    n_yr = len(trnd_yr)

    nlat = tr85.TLONG.shape[0]
    nlon = tr85.TLONG.shape[1]

    if index_ens is None:
        nens = len(tr85.ens)
    else:
        nens = 1

    empty_trend = xr.DataArray(np.nan*np.ones((n_yr,n_trnd,nlat,nlon)),dims=('time','trend_length','nlat','nlon'))
    trend = xr.Dataset({'trend_length':trnd_lngth,'time':trnd_yr})
    for v in varlist:
        trend[v] = empty_trend.copy()
    print trend

    #-------------------------------------------------------------------------------
    #-- compute trends
    #-------------------------------------------------------------------------------

    print('\n'.join(['','-'*80,'compute trends','-'*80,]))
    time = tr85_tc.year.values

    files = []
    for ie in range(nens):

        if index_ens is None:
            file_out = os.path.join(diro['out'],'toe_thermocline_trends.ens_i_%03d.nc'%ie)
        else:
            file_out = os.path.join(diro['out'],'toe_thermocline_trends.ens_i_%03d.nc'%index_ens)

        files.append(file_out)
        if os.path.exists(file_out): continue

        print('\n'.join(['-'*30,'Ens: %d'%ie,'-'*30]))


        #-- reset trend arrays
        print('\tresetting arrays')
        for v in varlist: trend[v].values[:] = np.nan

        #-- loop over trend year
        for iy in range(n_yr):
            print('\tcomputing trends for year %d'%trnd_yr[iy])

            #-- loop over trend length
            for ip in range(n_trnd):
                print('\t\ttrend length: %f'%trnd_lngth.values[ip])

                #-- subset record for the right period
                x2 = trnd_yr.values[iy]
                x1 = x2 - trnd_lngth.values[ip] + 1.
                if x1 < min_yr: continue
                tnx = np.where( (x1 <= time) & (time <= x2 ))[0]

                if index_ens is None:
                    ds = tr85_tc.isel(ens=ie)
                else:
                    ds = tr85_tc
                ds = ds.isel(time=slice(tnx[0],tnx[-1]+1))

                #-- compute trends on each variable
                x = ds.year.values
                nt = len(x)
                for v in varlist:
                    print('\t\t\t Var: %s'%v)
                    y = ds[v].values.reshape((nt,-1))
                    I = (~np.isnan(y[0,:])) # eliminate nan columns
                    beta = np.polyfit(x,y[:,I],1)
                    slope = np.ones(y.shape[1:])
                    slope[:] = np.nan
                    slope[I] = beta[0,:]
                    trend[v].values[iy,ip,:,:] = slope.reshape((nlat,nlon))
                    del y
                    del slope

        print('writing %s'%file_out)
        trend.to_netcdf(file_out)
        print

    print('done.')

#-------------------------------------------------------------------------------
#-- function
#-------------------------------------------------------------------------------

def compute_std_dask_relient():
    files = os.path.join(diro['out'],'toe_thermocline_trends.ens_i_[0-9][0-9][0-9].nc')

    with timer('load ens data'):
        chunks = {'nlat':16,'nlon':16}
        ds = xr.open_mfdataset(files,concat_dim='ens',chunks=chunks)
        trend_year = ds.time.values
        trend_length = ds.trend_length.values
        n_trend = len(trend_length)
        n_year = len(trend_year)
        print ds

    with timer('compute std'):
        ds_std = ds.std(dim='ens')
        print ds_std

    with timer('write %s'%file_std):
        ds_std.to_netcdf(file_std)

#-------------------------------------------------------------------------------
#-- function
#-------------------------------------------------------------------------------

def compute_std():
    files = sorted(glob(os.path.join(diro['out'],'toe_thermocline_trends.ens_i_[0-9][0-9][0-9].nc')))

    for i,f in enumerate(files):
        with timer('computing file %s'%f):
            ds = xr.open_dataset(f)

            if i == 0:
                trend_year = ds.time.values
                trend_length = ds.trend_length.values
                n_trend = len(trend_length)
                n_year = len(trend_year)
                nlat = ds[v].shape[2]
                nlon = ds[v].shape[3]


                dso = xr.Dataset({v:xr.DataArray(np.zeros((n_year,n_trend,nlat,nlon)).astype(np.float64),
                                                 dims=('time','trend_length','nlat','nlon')),
                                  v+'_cnt':xr.DataArray(np.zeros((n_year,n_trend,nlat,nlon)).astype(np.float64),
                                                        dims=('time','trend_length','nlat','nlon')),
                                  v+'_std':xr.DataArray(np.zeros((n_year,n_trend,nlat,nlon)).astype(np.float64),
                                                        dims=('time','trend_length','nlat','nlon'))})
            xnew = ds[v].values
            cnt = ~np.isnan(xnew)*1

            xbar = dso[v].values
            n = dso[v+'_cnt'].values
            s2 = dso[v+'_std'].values

            n += cnt
            dev = np.where(np.isnan(xnew),0.,xnew - xbar)
            xbar += np.divide(dev, n, where=n>0)
            dev2 = np.where(np.isnan(xnew),0.,xnew - xbar)
            s2 += dev*dev2

            dso[v].values = xbar
            dso[v+'_cnt'].values = n
            dso[v+'_std'].values = s2

            print dso

    #-- apply normalizations and fill values
    #-- count
    n = dso[v+'_cnt'].values

    #-- normalize variance
    var = dso[v+'_std'].values
    dso[v+'_std'].values = np.where(n > 2, np.divide(var,(n-1),where=n-1>0), np.nan)

    #-- set missing values
    var = dso[v].values
    dso[v].values = np.where(n == 0, np.nan, var)

    dso[v+'_std'].values = np.sqrt(dso[v+'_std'].values)

    #-- output single precisions
    dso[v] = dso[v].astype(np.float32)
    dso[v+'_cnt'] = dso[v+'_cnt'].astype(np.float32)
    dso[v+'_std'] = dso[v+'_std'].astype(np.float32)

    #-- write to file
    dso.to_netcdf(file_std)

#-------------------------------------------------------------------------------
#-- function
#-------------------------------------------------------------------------------

def compute_toe(index_ens=None):

    with timer('load std data'):
        ds_std = xr.open_dataset(file_std)
        print ds_std

    with timer('load ens data'):
        chunks = {'nlat':16,'nlon':16}
        files = os.path.join(diro['out'],'toe_thermocline_trends.ens_i_%03d.nc'%index_ens)
        print files
        ds = xr.open_dataset(files) #,concat_dim='ens',chunks=chunks)
        trend_year = ds.time.values
        trend_length = ds.trend_length.values
        n_trend = len(trend_length)
        n_year = len(trend_year)
        print ds

    with timer('normalize trends'):
        ds_norm = ds[v] / ds_std[v+'_std']
        ds_norm = ds_norm.compute()
        print ds_norm

    with timer('compute ToE'):

        nlat = ds[v].shape[2]
        nlon = ds[v].shape[3]

        toe = xr.DataArray(np.ones((nlat,nlon)),dims=('nlat','nlon'))
        record_length = xr.DataArray(np.ones((nlat,nlon)),dims=('nlat','nlon'))

        ncomp = nlat*nlon
        n = 0
        for i in range(nlat):
            for j in range(nlon):

                if ds_norm[:,:,j,i].isnull().all():
                    continue

                detected = (ds_norm.values[:,:,j,i] <= -2.)

                toe_x = np.ones(n_trend)*np.nan
                for ii in range(n_trend):
                    for jj in range(n_year):

                        if detected[jj:,ii].all():
                            toe_x[ii] = trend_year[jj]
                            break

                toe.values[j,i] = np.min(toe_x)
                record_length.values[j,i] = trend_length[np.argmin(toe_x)]

                n += 1
                percent_complete = n*100./ncomp
                print "\r{:0.2f} %".format(percent_complete),

        dso = xr.Dataset({'toe':toe,'record_length':record_length})
        file_out = os.path.join(diro['out'],'toe_thermocline.%s.ens_i_%d.nc'%(v,index_ens))
        dso.to_netcdf(file_out)

#-------------------------------------------------------------------------------
#-- main
#-------------------------------------------------------------------------------

if __name__ == '__main__':
    import sys
    step = sys.argv[1]
    ie = sys.argv[2]

    if step == 'compute_trends':
        compute_trends(index_ens=int(ie))
    elif step == 'compute_std':
        compute_std()
    elif step == 'compute_toe':
        compute_toe(index_ens=int(ie))
    else:
        print('no')
