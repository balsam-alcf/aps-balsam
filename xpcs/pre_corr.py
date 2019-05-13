#!/usr/bin/env python
from balsam.launcher.dag import current_job
import glob
import os

def basepath(path):
    '''Strip name out of path'''
    return os.path.splitext(os.path.basename(path))[0]

# Link to requisite files in job workdir
h5_path = current_job.data['h5_path']
imm_path = current_job.data['imm_path']
os.symlink(h5_path, os.path.basename(h5_path))
os.symlink(imm_path, os.path.basename(imm_path))
