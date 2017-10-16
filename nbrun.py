#! /usr/bin/env python
import os
import sys

def exec_nb(notebook_filename,kernel_name='python2'):
    '''execute a notebook
    see http://nbconvert.readthedocs.io/en/latest/execute_api.html
    '''
    import nbformat
    from nbconvert.preprocessors import ExecutePreprocessor

    with open(notebook_filename) as f:
        nb = nbformat.read(f, as_version=4)

    ep = ExecutePreprocessor(timeout=600, kernel_name=kernel_name)

    ep.preprocess(nb, {'metadata': {'path': './'}})

    with open(os.path.basename(notebook_filename), 'wt') as f:
        nbformat.write(nb, f)

if __name__ == '__main__':
    nb = sys.argv[1]

    exec_nb(nb)
