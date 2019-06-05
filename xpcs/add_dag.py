#!/usr/bin/env python
import os
import sys

# Set run parameters here
common_params = {
    'num_nodes': 1,
    'ranks_per_node': 1,
    'cpu_affinity': "none", # -cc none
    'threads_per_rank': 64,
}

ENDPOINT_ID=os.environ['GLOBUS_ENDPOINT']

def add_dag(h5_path, imm_path, result_top):
    '''Add a Corr job to the DB'''
    from balsam.core.models import ApplicationDefinition as App
    from balsam.core.models import BalsamJob as Job
    from balsam.launcher import dag

    args = f'{os.path.basename(h5_path)} -imm {os.path.basename(imm_path)}'
    corr_job = Job(
        name=os.path.basename(imm_path),
        workflow=os.path.basename(h5_path),
        application="corr",
        args = args,
        environ_vars = "HDF5_USE_FILE_LOCKING=FALSE:OMP_NUM_THREADS=64",
        **common_params,
    )
    corr_job.data['h5_path'] = h5_path
    corr_job.data['imm_path'] = imm_path
    corr_job.data['result_path'] = result_top
    corr_job.data['endpoint'] = ENDPOINT_ID
    return corr_job
