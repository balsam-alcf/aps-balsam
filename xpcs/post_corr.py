#!/usr/bin/env python
import os
from balsam.launcher.dag import current_job
from transfer import transfer

print("Stage OUT")
THETA_ENDPOINT = '08925f04-569f-11e7-bef8-22000b9a448b'

here = os.getcwd()
remote_endpoint = current_job.data['endpoint']
h5_path = current_job.data['h5_path']
imm_path = current_job.data['imm_path']

result_top = current_job.data['result_path']

local_paths = [
    os.path.join(here, os.path.basename(h5_path)),
    #os.path.join(here, os.path.basename(imm_path)), # NOT NEEDED
]
remote_paths = [
    h5_path,
    #imm_path,
]

transfer_pairs = zip(local_paths, remote_paths)
transfer(THETA_ENDPOINT, remote_endpoint, transfer_pairs)
