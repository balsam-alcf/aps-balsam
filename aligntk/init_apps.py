#!/usr/bin/env python
import os
from aps.register import define_apps, App

this_dir = os.path.dirname(os.path.abspath(__file__))
aligntk_bin = '../aligntk-1.0.2/install/bin' # relative to this_dir
BIN = os.path.abspath(os.path.join(this_dir, aligntk_bin))

define_apps(
    exe_dir=BIN,
    apps =
    {
        'find_rst' : 
            dict(
                fixed_args = [
                    '-tif',
                    '-output cmaps/',
                    '-max_res 4096',
                    '-scale 1.0',
                    '-tx -50-50',
                    '-ty -50-50',
                    'summary cmaps/summary.out',
                    'images images/',
                    '-pairs pairs.lst',
                ],
                preprocess = os.path.join(this_dir, "pre_findrst.py")
            ),
        'register' :
            dict(
                fixed_args = [
                    '-tif',
                    '-output maps/',
                    '-distortion 4.0',
                    'images images/',
                    '-pairs pairs.lst',
                    '-output_level 6',
                    '-depth 6',
                    '-quality 03',
                    'summary maps/summary.out',
                    '-initial_map cmaps/'
                ],
            ),
        'align' :
            dict(
                fixed_args = [
                    '-image_list images.lst',
                    '-map_list pairs.lst',
                    '-maps /maps/',
                    '-output /amaps/',
                    '-schedule schedule.lst',
                    '-incremental',
                    '-output_grid /grids/',
                    '-grid_size 13642x23904',
                    '-fixed S_0000',
                    '-images images/'
                ],
            ),
    }
)
