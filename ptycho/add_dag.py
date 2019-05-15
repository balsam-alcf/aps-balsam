#!/usr/bin/env python
import os
import sys

# Set run parameters here
common_params = {
    'num_nodes': 128,
    'ranks_per_node': 1,
    'threads_per_rank' : 128,
    'threads_per_core' : 2,
    'cpu_affinity': "depth", # -cc depth
}


def add_dag(input_path, wf_tag):
    '''Add a job to the DB'''
    from balsam.core.models import ApplicationDefinition as App
    from balsam.core.models import BalsamJob as Job
    from balsam.launcher import dag

    job = Job(
        name="reco_cone",
        workflow=wf_tag,
        application="reconstruct_cone",
        **common_params,
    )
    job.data['input_path'] = input_path
    job.save()
    print(f"Created new job")
    return job
