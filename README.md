# Theta: Balsam site setup
- Set up a Balsam DB and service running on theta login
- At the balsam site, run init-xray-apps to initialize Apps in the DB

# Remote submission
- Run ./create-xray-job --images <image-dir> to submit a DAG for processing a particular image directory


### Build
LD_LIBRARY_PATH=/gpfs/mira-home/msalim/brainImaging-test/misha-build/libs/lib64 time aprun -n 16  -N 16  -cc none  /gpfs/mira-home/msalim/brainImaging-test/misha-build/libs/bin/find_rst -tif -output cmaps/ -max_res 4096 -scale 1.0 -tx -50-50 -ty -50-50 -summary cmaps/summary.out -images images/ -pairs pairs.lst
