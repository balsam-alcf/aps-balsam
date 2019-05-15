#!/usr/bin/env python
from balsam.launcher.dag import current_job
import glob
import os

def basepath(path):
    '''Strip name out of path'''
    return os.path.splitext(os.path.basename(path))[0]

# Link to requisite folder in job workdir
input_path = current_job.data['input_path']
os.symlink(input_path, os.path.basename(input_path))
