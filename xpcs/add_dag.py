#!/usr/bin/env python
import os
import sys

# Set run parameters here
common_params = {
    'num_nodes': 1,
    'ranks_per_node': 1,
    'cpu_affinity': "none", # -cc none
}


def add_dag(h5_path, imm_path, wf_tag):
    '''Add a Corr job to the DB'''
    from balsam.core.models import ApplicationDefinition as App
    from balsam.core.models import BalsamJob as Job
    from balsam.launcher import dag

    common_params['input_files'] = 'images cmaps maps images.lst pairs.lst amaps grids aligned schedule.lst'

    args = f'{os.path.basename(h5_path)} -imm {os.path.basename(imm_path)}'
    corr_job = Job(
        name="corr",
        workflow=wf_tag,
        application="corr",
        args = args,
        **common_params,
    )
    corr_job.data['h5_path'] = h5_path
    corr_job.data['imm_path'] = imm_path
    corr_job.save()
    print(f"Created new corr job")
    return corr_job
