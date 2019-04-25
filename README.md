# Theta Setup

## Startup Balsam server
First, login to theta and set up a Balsam DB:
```
module load balsam
balsam init /path/to/testdb
. balsamactivate /path/to/testdb
```

You will want to configure the queue policy in ~/.balsam/theta_policy.ini. 
For this demo, set `submit-jobs = off` for the debug queue, and 
`submit-jobs = on` for the default queue.  Also, set `max-queued = 1`.
Then, stand up the balsam service with `balsam service`.  It will be logging to
a service log file in the log/ subdirectory.  

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
The `submit` script will open a tunnel with port forwarding, prompting you to authenticate to Theta. 

```
./submit --db=/path/to/testdb --images /path/to/images/on/alcfxray1 --destination /path/to/workdir/on/theta
```
The rest is automatically initiated:
  - file transfer
  - DAG creation
  
That's it!  You can check with `balsam ls` that the jobs were actually created.  The balsam service will immediately start preprocessing `find_rst` and subsequently submit a launcher job to process the whole DAG. You can read over the service log (in the log/ subdirectory of the balsam database); that will show activity for the submitted jobs. Of course, you can always double-verify the job is queued in Cobalt with `qstat`.
