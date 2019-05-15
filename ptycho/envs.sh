module load datascience/mpi4py
#export PYTHONPATH=$PYTHONPATH:/projects/large3dxrayADSP/pipeline/custom_packages
export PTYCHO_BASE=/projects/datascience/msalim/large3dxrayADSP
export PYTHONPATH=$PYTHONPATH:$PTYCHO_BASE/custom_packages
export PYTHONPATH=$PYTHONPATH:$PTYCHO_BASE/custom_packages/lib/python3.5/site-packages
export PYTHONPATH=$PYTHONPATH:$PTYCHO_BASE/custom_packages/autograd
export PYTHONPATH=$PYTHONPATH:$PTYCHO_BASE
export PMI_NO_FORK=1
export HDF5_USE_FILE_LOCKING=FALSE
export MPICH_MAX_THREAD_SAFETY=multiple

echo "Python is $(which python)"
echo "PYTHONPATH is $PYTHONPATH"
