# Theta Setup

## Startup Balsam server
First, login to theta and set up a Balsam DB:
```
module load balsam
balsam init /path/to/testdb
. balsamactivate /path/to/testdb
```

## Populate DB with Apps
Now, grab an AlignTK build, configure the init-xray-apps script to point at them,
and run it to register the AlignTK  apps with the current DB.
```
git clone https://github.com/balsam-alcf/aps-balsam
cd aps-balsam
# modify init-xray-apps as needed
./init-xray-apps
balsam ls apps --verbose # ensure the apps show up correctly!
```


# ALCFXray1 Setup

## Install Miniconda & Python3

```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod +x Miniconda3-latest-Linux-x86_64.sh
./Miniconda3-latest-Linux-x86_64.sh
source .bashrc
```

## Set up a Balsam Env

```
conda config --add channels intel
conda create -p balsam-env intelpython3_core python=3.6
conda activate /home/msalim/balsam-env
pip install pexpect

git clone https://github.com/balsam-alcf/balsam.git
cd balsam
pip install -e.
cd ~
git clone https://github.com/balsam-alcf/aps-balsam
```


## SSH Config
Set up ~/.ssh/config to support shared connections:

```
Host *
ControlMaster auto
ControlPath ~/.ssh/master-%r@%h:%p
```


## Copy testdb/server-info over to testdb/alcfxray1

Create a new directory on alcfxray1 and copy in the remote Balsam DB server-info file.
The balsam client on alcfxray1 needs this file to point at the correct port on Theta.
```
mkdir db
cd db
scp msalim@theta:/path/to/testdb/server-info .
```

# Run ./submit to initiate the transfer and start the jobs on Theta
Pass the DB (directory containing server-info) and one or more --images arguments (each specifying an images/ directory)
to the aps-balsam/submit script.  This also requires batch job submission parameters for Cobalt (e.g. how many nodes and
how much walltime is requested for the processing workflow).  The script will open a tunnel with port forwarding, prompting you
to authenticate to Theta. The rest is automatically initiated.
```
./submit --db=/path/to/testdb --images <image-dir1> --images <image-dir2> -n Num_Nodes -A Project -q Queue -t WallTimeMinutes
```
