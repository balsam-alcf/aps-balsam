#!/usr/bin/env python
import os
from balsam.launcher.dag import current_job
from transfer import transfer

print("Stage IN")
THETA_ENDPOINT = '08925f04-569f-11e7-bef8-22000b9a448b'

here = os.getcwd()
remote_endpoint = current_job.data['endpoint']
h5_path = current_job.data['h5_path']
imm_path = current_job.data['imm_path']

remote_paths = [h5_path, imm_path]
local_paths = [
    os.path.join(here, os.path.basename(h5_path)),
    os.path.join(here, os.path.basename(imm_path)),
]

transfer_pairs = zip(remote_paths, local_paths)
transfer(remote_endpoint, THETA_ENDPOINT, transfer_pairs)
