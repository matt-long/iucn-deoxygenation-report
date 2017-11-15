'''
.. module:: grid_tools

Tools for grids.
'''

import xarray as xr
import numpy as np

Re = 6.37122e6 # m
deg2rad = np.pi/180.

def compute_grid_area(longitude,latitude):
    dx = np.diff(longitude)
    if not (dx == dx[0]).all():
        print('dx not constant')
        exit(1)
    dx = dx[0]

    dy = np.diff(latitude)
    if not (dy == dy[0]).all():
        print('dy not constant')
        exit(1)
    dy = dy[0]

    ny = latitude.shape[0]
    nx = longitude.shape[0]

    yc = np.broadcast_to(latitude[:,None],(ny,nx))
    xc = np.broadcast_to(longitude[None,:],(ny,nx))

    yv = np.stack((yc-dy/2.,yc-dy/2.,yc+dy/2.,yc+dy/2.),axis=2)
    xv = np.stack((xc-dx/2.,xc+dx/2.,xc+dx/2.,xc-dx/2.),axis=2)

    y0 = np.sin(yv[:,:,0]*deg2rad) # south
    y1 = np.sin(yv[:,:,3]*deg2rad) # north
    x0 = xv[:,:,0]*deg2rad         # west
    x1 = xv[:,:,1]*deg2rad         # east
    area = (y1-y0)*(x1-x0)*Re**2.

    print('total area = %.16e'%np.sum(area))
    print('check area = %.16e'%(4.*np.pi*Re**2.))

    return area

#------------------------------------------------------------------------
#-- FUNCTION
#------------------------------------------------------------------------
def generate_latlon_grid(nx,ny,lon0=0.,file_out=''):
    '''
    .. function:: generate_latlon_grid(nx,ny[,file_out=''])

    Generate a regular lat,lon grid file.

    :param nx: number of x points.

    :param ny: number of y points.

    :param file_out: optional output file.

    :returns: dataset with grid variables

    '''

    dx = 360./nx
    dy = 180./ny

    if file_out:
        print('dx = %.6f'%dx)
        print('dy = %.6f'%dy)

    latitude = np.arange(-90.+dy/2.,90.,dy)
    longitude = np.arange(lon0+dx/2.,lon0+360.,dx)

    yc = np.broadcast_to(latitude[:,None],(ny,nx))
    xc = np.broadcast_to(longitude[None,:],(ny,nx))

    yv = np.stack((yc-dy/2.,yc-dy/2.,yc+dy/2.,yc+dy/2.),axis=2)
    xv = np.stack((xc-dx/2.,xc+dx/2.,xc+dx/2.,xc-dx/2.),axis=2)

    y0 = np.sin(yv[:,:,0]*deg2rad) # south
    y1 = np.sin(yv[:,:,3]*deg2rad) # north
    x0 = xv[:,:,0]*deg2rad         # west
    x1 = xv[:,:,1]*deg2rad         # east
    area = (y1-y0)*(x1-x0)*Re**2.

    if file_out:
        print('total area = %.16e'%np.sum(area))
        print('check area = %.16e'%(4.*np.pi*Re**2.))

    ds = xr.Dataset(
        {'lat':xr.DataArray(latitude,
                                 dims=('lat'),
                                 attrs={'units':'degrees_north',
                                        'long_name':'Latitude'}),
         'lon':xr.DataArray(longitude,
                                  dims=('lon'),
                                  attrs={'units':'degrees_east',
                                         'long_name':'Longitude'})})

    ds['xc'] = xr.DataArray(xc,dims=('lat','lon'),
                            attrs={'units':'degrees_east',
                                   'long_name':'longitude of cell centers'})

    ds['yc'] = xr.DataArray(yc,dims=('lat','lon'),
                            attrs={'units':'degrees_north',
                                   'long_name':'latitude of cell centers'})

    ds['xv'] = xr.DataArray(xv,dims=('lat','lon','nv'),
                            attrs={'units':'degrees_east',
                                   'long_name':'longitude of cell corners'})
    ds['yv'] = xr.DataArray(yv,dims=('lat','lon','nv'),
                            attrs={'units':'degrees_north',
                                   'long_name':'latitude of cell corners'})

    ds['area'] = xr.DataArray(area,dims=('lat','lon'),
                              attrs={'units':'m^2',
                                     'long_name':'area'})

    if file_out:
        ds.to_netcdf(file_out)

    return ds
