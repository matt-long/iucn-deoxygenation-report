#! /usr/bin/env python
#BSUB -P NCGD0011
#BSUB -W 24:00
#BSUB -n 1
#BSUB -J o2dist
#BSUB -o logs/o2dist.%J
#BSUB -e logs/o2dist.%J
#BSUB -q caldera
#BSUB -N
from config_calc import *
from glob import glob

clobber = False

time_chunks = 5 * 12 # read data in 5 year chunks
xr_open_dataset = {
    'chunks':{'time' : time_chunks},
    'mask_and_scale' : True,
    'decode_times' : False,
    'decode_coords': False}

easy = './subtree/easy-analysis/esm_tools.py'


#-------------------------------------------------------------------------------
#-- script
#-------------------------------------------------------------------------------

year_range = (1920,2100)
component = 'ocn'
freq = 'monthly'

varlist = ['OUR:AOU,IAGE','TEMP',
           'AOU','O2_PRODUCTION','STF_O2','O2','O2_CONSUMPTION','PD','IAGE']

#-- compute annual means
#-- get case info
info = cesm_le.case_info(include_control = True,
                         include_rcp85 = True,
                         include_rcp45 = True)

#-------------------------------------------------------------------------------
#-- function
#-------------------------------------------------------------------------------

def ensemble_ops(file_list,scenario):
    file_in_list = [f for f,s in zip(file_list,info['scenario'])
                    if s == scenario]
    if not file_in_list:
        return

    file_out_avg = file_in_list[0].copy().update(ens='avg')
    file_out_std = file_in_list[0].copy().update(ens='std')
    if not file_out_avg.exists() or not file_out_std.exists():
        control = {'task' : 'ensemble_mean_std',
                   'kwargs': {'file_in_list':[f() for f in file_in_list],
                   'file_out_avg':file_out_avg(),
                   'file_out_std':file_out_std()}}
        jid = tm.submit([easy,et.json_cmd(control)])

#-------------------------------------------------------------------------------
#-- function
#-------------------------------------------------------------------------------

def open_ens(sc,op,varlist):
    plot_grid_vars = ['TLAT','TLONG','KMT','TAREA','ULAT','ULONG','UAREA',
                      'z_t','z_t_150m','z_w','dz',
                      'area_sum','vol_sum']

    if not isinstance(varlist,list):
        varlist = [varlist]
    dss = []
    for v in varlist:
        glob_patt = os.path.join(
            diro['work'],'%s.[0-9][0-9][0-9].%s.%s.1920-2100.nc'%(sc,op,v))
        files = sorted(glob(glob_patt))
        if not files:
            print('no files')
            print(glob_patt)
            sys.exit(1)
        dsi = xr.open_mfdataset(files,
                                concat_dim='ens',
                                decode_times=False,
                                decode_coords=False)
        dsi = dsi.drop([k for k in dsi
                        if k not in varlist+plot_grid_vars])
        dss.append(dsi)

    return xr.merge(dss)


if __name__ == '__main__':

#-------------------------------------------------------------------------------
#-- compute ann means
#-------------------------------------------------------------------------------

    file_ann = {}
    for variable in varlist:

        preprocess = ['calc_ann_mean']

        #-- "derived variables" are made from combinations of multiple variables
        if ':' in variable:
            var_varlist = variable.split(':')[1].split(',')
            file_list = []
            for j,v in enumerate(var_varlist):
                file_list_v = cesm_le.tseries_files(info['caselist'],component,freq,v)
                for i,case_files in enumerate(file_list_v):
                    if j == 0:
                        file_list.append({v:case_files})
                    else:
                        file_list[i].update({v:case_files})
            preprocess = ['pop_derive_var_'+variable]+preprocess

        else:
            #-- list of files = [[case_files],[case_files]...]
            file_list = cesm_le.tseries_files(info['caselist'],component,freq,variable)
            if file_list is None: sys.exit(1)

        file_ann[variable] = []

        #-- loop over cases
        for i,case_files in enumerate(file_list):

            file_out = et.hfile(dirname=diro['work'],
                                prefix=info['scenario'][i],
                                ens=info['ens'][i],
                                varname=variable,
                                op='ann',
                                datestr='%d-%d'%year_range)

            file_ann[variable].append(file_out)
            if not file_out.exists() or clobber:
                control = {'task' : 'open_tsdataset',
                           'kwargs': {'file_out':file_out(),
                                      'paths':case_files,
                                      'year_offset':info['yr0'][i],
                                      'year_range':year_range,
                                      'preprocess' : preprocess}}
                jid = tm.submit([easy,et.json_cmd(control)])

    tm.wait()

#-------------------------------------------------------------------------------
#-- drift correct
#-------------------------------------------------------------------------------

    if info['scenario'][0] != 'ctrl':
        print('need control for drift correction')
        sys.exit(1)

    #-- apply drift coorrection
    file_ann_dft = {}
    for variable in varlist:

        file_out_list = [f.copy().append(op='dft') for f in file_ann[variable]]
        file_ann_dft[variable] = file_out_list
        file_drift = file_ann[variable][0]().replace('.nc','.drift_corr.nc')
        if not all([f.exists() for f in file_out_list]):
            control = {'task' : 'apply_drift_correction_ann',
                       'kwargs': {'variable':variable,
                                  'file_ctrl':file_ann[variable][0](),
                                  'file_drift':file_drift,
                                  'file_in_list':[f() for f in file_ann[variable]],
                                  'file_out_list':[f() for f in file_out_list]}}
            jid = tm.submit([easy,et.json_cmd(control)])

    tm.wait()

    #for variable in varlist:
    #    ensemble_ops(file_ann_dft[variable],'tr85')
    #    ensemble_ops(file_ann_dft[variable],'tr45')

#-------------------------------------------------------------------------------
#-- compute zonal means
#-------------------------------------------------------------------------------

    file_ann_za = {}
    for variable in varlist:
        file_ann_za[variable] = []
        for file_in in file_ann_dft[variable]:

            file_out = file_in.copy().append(op='za')
            file_ann_za[variable].append(file_out)
            if not file_out.exists() or clobber:
                control = {'task' : 'pop_calc_zonal_mean',
                           'kwargs': {'file_out':file_out(),
                                      'file_in':file_in()}}
                jid = tm.submit([easy,et.json_cmd(control)])

    tm.wait()

    for variable in varlist:
        ensemble_ops(file_ann_za[variable],'tr85')
        ensemble_ops(file_ann_za[variable],'tr45')

#-------------------------------------------------------------------------------
#-- compute global means
#-------------------------------------------------------------------------------

    file_ann_glb = {}
    for variable in varlist:
        file_ann_glb[variable] = []
        for file_in in file_ann_dft[variable]:

            file_out = file_in.copy().append(op='glb')
            file_ann_za[variable].append(file_out)
            if not file_out.exists() or clobber:
                control = {'task' : 'transform_file',
                           'kwargs': {'file_out':file_out(),
                                      'file_in':file_in(),
                                      'preprocess' : ['pop_calc_global_mean']}}
                jid = tm.submit([easy,et.json_cmd(control)])

    tm.wait()

    for variable in varlist:
        ensemble_ops(file_ann_glb[variable],'tr85')
        ensemble_ops(file_ann_glb[variable],'tr45')



#-------------------------------------------------------------------------------
#-- compute area means
#-------------------------------------------------------------------------------

    file_ann_aavg = {}
    for variable in varlist:
        file_ann_aavg[variable] = []
        for file_in in file_ann_dft[variable]:

            file_out = file_in.copy().append(op='aavg')
            file_ann_aavg[variable].append(file_out)
            if not file_out.exists() or clobber:
                control = {'task' : 'transform_file',
                           'kwargs': {'file_out':file_out(),
                                      'file_in':file_in(),
                                      'preprocess' : ['pop_calc_area_mean']}}
                jid = tm.submit([easy,et.json_cmd(control)])

    tm.wait()

    for variable in varlist:
        ensemble_ops(file_ann_aavg[variable],'tr85')
        ensemble_ops(file_ann_aavg[variable],'tr45')

    tm.wait()

#-------------------------------------------------------------------------------
#-- compute vertical integrals
#-------------------------------------------------------------------------------

    file_ann_zint = {}
    for variable in varlist:

        file_ann_zint[variable] = []
        for file_in in file_ann_dft[variable]:

            file_out = file_in.copy().append(op='zint')
            file_ann_zint[variable].append(file_out)

            if not file_out.exists() or clobber:
                control = {'task' : 'transform_file',
                           'kwargs': {'file_out':file_out(),
                                      'file_in':file_in(),
                                      'preprocess' : ['pop_calc_vertical_integral']}}
                jid = tm.submit([easy,et.json_cmd(control)])

    tm.wait()
