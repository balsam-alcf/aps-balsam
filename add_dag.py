#!/usr/bin/env python
import os
import sys

# Set run parameters here
common_params = {
    'num_nodes': 16,
    'ranks_per_node': 1,
    'cpu_affinity': "none", # -cc none
}


def add_dag(images_dir):
    '''Add a sequence of AlignTK Jobs to the DB'''
    from balsam.core.models import ApplicationDefinition as App
    from balsam.core.models import BalsamJob as Job
    from balsam.launcher import dag

    workflow = os.path.basename(images_dir)
    if Job.objects.filter(workflow=workflow).exists():
        existing = Job.objects.get(workflow=workflow, name="find_rst")
        existing = existing.data.get("images_dir")
        print(f"A workflow named '{workflow}' has already been created for {existing}")
        print(f"Please give the --images folder a unique base name to avoid a naming collision")
        sys.exit(1)

    common_params['workflow'] = workflow
    common_params['input_files'] = 'images cmaps maps images.lst pairs.lst amaps grids aligned schedule.lst'

    find_rst = Job(
        name="find_rst",
        application="find_rst",
        **common_params,
    )
    register = Job(
        name="register",
        application="register",
        **common_params,
    )
    align = Job(
        name="align",
        application="align",
        **common_params,
    )
    find_rst.data['images_dir'] = images_dir
    find_rst.save()
    register.save()
    align.save()
    dag.add_dependency(find_rst, register)
    dag.add_dependency(register, align)
    print(f"Created new DAG to process {images_dir}")
    return find_rst, register, align
