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

experiments = ['esmHistorical','esmrcp85']

cmip5_root = '/glade/p/CMIP/CMIP5'
models =  ['IPSL/IPSL-CM5A-LR',
                 'MOHC/HadGEM2-ES',
           'MPI-M/MPI-ESM-LR',
           'MRI/MRI-ESM1',
           'NCC/NorESM1-ME',
           'NOAA-GFDL/GFDL-ESM2G',
           'NOAA-GFDL/GFDL-ESM2M',
           'NSF-DOE-NCAR/CESM1-BGC']

other_models = ['CCCma/CanESM2','FIO/FIO-ESM','FIO/fio-esm','BNU/BNU-ESM',
                'BCC/bcc-csm1-1','BCC/bcc-csm1-1-m','INM/inmcm4',
                'MIROC/MIROC-ESM']

domain_list = ['fx'] #'ocean','ocnBgchem/fx']
varname_list = ['o2']


info = {k: {e : {'version' : '',
                 'droot' : [],
                 'files' : []}
                for e in experiments}
                for k in models}

for m in models:
    for e in experiments:
        walk = [os.walk(os.path.join(cmip5_root,o,m,e))
                for o in ['output','output1','output2']]

        for w in walk:
            for root, dirs, files in w:
                if not files: continue # we want files
                if dirs: print('ERROR'); exit(1) # should be no subdirs

                #-- pick the domain
                if not any(['/'+d+'/' in root for d in domain_list]): continue

                #-- path is .../path-to-here/ensemble/version/varname
                varname = root.split('/')[-1]
                version = root.split('/')[-2]
                ens = root.split('/')[-3]
                #if varname not in varname_list: continue
                if ens != 'r1i1p1': continue

                print ' '.join([m,e,varname,version,ens])

                if info[m][e]['version']:
                    version = sorted([info[m][e]['version'],version])[-1]
                    #-- if version has not been updated, move on
                    if version == info[m][e]['version']:
                        print('keeping version: %s'%version)
                        continue
                info[m][e]['version'] = version
                info[m][e]['files'] = files
                info[m][e]['droot'] = root


for m in models:
    print('-'*80+'\n%s'%m)

    for e in experiments:
        print('\t%s: %s'%(e,info[m][e]['droot']))

        for f in info[m][e]['files']:
            print('\t\t%s'%f)
