# Theta Setup

## Set up a Balsam DB
First, login to theta and set up a Balsam DB:
```
module load balsam
balsam init /path/to/testdb
. balsamactivate /path/to/testdb
```
We are going to need a place to store the images as they are transferred over from `alcfxray1`.  Let's place them near the database by making the following directory:
```
mdkir /path/to/testdb/transferred_images
```

## Set up Balsam service
You will want to configure the queue policy in your home directory: `~/.balsam/theta_policy.ini` 
For this demo, set:
 - `submit-jobs = off` for the debug queue 
 - `submit-jobs = on` for the default queue  
 - `max-queued = 1` for the default queue
 
This will ensure the service only queues up one job at a time run in the default queue.
Finally, stand up the balsam service with `balsam service`.  It will be logging to a service logfile in the `/path/to/testdb/log` directory.  

## Populate DB with Apps
Now, grab an AlignTK build, and pull down this repository to set up the workflow. 
```
git clone https://github.com/balsam-alcf/aps-balsam
cd aps-balsam/aligntk
```
You will need to set one line in the `init-xray-apps` script to tell Balsam where your AlignTK binaries are installed.
Set a relative path to the `aps-balsam` directory as follows:
```
aligntk_bin = '../../aligntk-1.0.2/install/bin' # relative to here
```
Now run the script to register the Applications with Balsam.  If all went well, you can verify with `balsam ls` that the applications are properly defined.

```
# after setting aligntk_bin above
./init-xray-apps
balsam ls apps --verbose # ensure the apps show up correctly!
```

That's it for Balsam setup on theta.  You now have a running Balsam DB containing the AlignTK Application definitions, command lines, and pre-processing scripts needed for the workflow.  Let's go over to `alcfxray1` and get the client set up.

# ALCFXray1 Setup

## Install Miniconda & Python3

We are starting on bare metal, so let's get Python from miniconda:

```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod +x Miniconda3-latest-Linux-x86_64.sh
./Miniconda3-latest-Linux-x86_64.sh
source .bashrc
```

## Set up a Balsam Env

Now we can set up a Python3.6 environment in which to run the Balsam client for remote job submission.
We will need to install the `pexpect` package, as well as Balsam.  `pexpect` is used in the `submit` script to allow SSH authentication from inside a Python subprocess.  
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
Our `submit` script leverages shared connections, so that you can authenticate once and keep an SSH tunnel open in the background for repeated job submissions and data transfers.  To make this work, you must configure  `~/.ssh/config` to support shared connections:

```
Host *
ControlMaster auto
ControlPath ~/.ssh/master-%r@%h:%p
```


## Copy server-info from Theta

The Balsam client needs to know which login node and port the Balsam DB server is running on.  This is accomplished by providing a local copy of the `server-info` file.  Create a new directory on alcfxray1 and copy in the remote Balsam DB server-info file.
The `submit` script running on alcfxray1 will use this to point at the correct port on Theta.
```
mkdir ~/db
cd ~/db
scp msalim@theta:/path/to/testdb/server-info .
```


# Run ./submit to initiate the transfer and start the jobs on Theta
Now we are finally ready to submit some work.  The `submit` script will open a tunnel with port forwarding, prompting you to authenticate to Theta. Once this tunnel is open, it should stay active in the background and subsequent `submit` calls will use the existing tunnel.
You will need to provide 3 paths to the submit command:
 - `--db` is the **local** (`alcfxray1`) directory containing server-info
 - `--images` is the **local** (`alcfxray1`) directory containing the *.tif* files to transfer
 - `--destination` is the **remote** (`theta`) directory to which the local images directory will be transferred.
 
 Be sure that you actually created the `--destination` directory earlier on Theta.
 
```
cd ~/aps-balsam/aligntk
./submit --db=~/db --images ~/images/on/alcfxray1 --destination /path/to/testdb/transferred_images
```
  
That's it!  After the images are transferred, a DAG containing the sequence of AlignTK jobs will be registered with Balsam.  You can verify with `balsam ls` that the jobs were actually created.  

The balsam service will immediately start preprocessing the first step (`find_rst`) and subsequently submit a launcher job to process the whole DAG.  You can track the job states with `balsam ls` and submit many more DAGs with `./submit`.  

The beauty of using Balsam's dynamic job launcher  is that new AlignTK jobs will automatically run inside the resources scheduled for other AlignTK jobs if they are ever idle nodes.  The Balsam service will ensure that a batch of resources is always scheduled for running your jobs, as long as there are jobs to run.  Failures are automatically identified and marked for human intervention.  

You can read over the service log (in the `log/` subdirectory of the balsam database) to track the activity of the automated job submission service.  The launcher logs will show detailed information for every single job launch command.  Of course, you can always verify that the job is queued in Cobalt with `qstat` or even terminate jobs with `qdel`, and Balsam will do the right thing, marking `RUNNING` jobs as `RUN_TIMEOUT`.  If you want to stop the service, `ssh` to the theta login node running it (this will be apparent from the top line of the service log), and use `kill <service-pid>`. 
