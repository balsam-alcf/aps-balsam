module load datascience/mpi4py
export PYTHONPATH=$PYTHONPATH:/projects/large3dxrayADSP/pipeline/custom_packages
export PYTHONPATH=$PYTHONPATH:/projects/large3dxrayADSP/pipeline/custom_packages/lib/python3.5/site-packages
export PYTHONPATH=$PYTHONPATH:/projects/large3dxrayADSP/pipeline/custom_packages/autograd
export PMI_NO_FORK=1
export HDF5_USE_FILE_LOCKING=FALSE
export MPICH_MAX_THREAD_SAFETY=multiple

echo "Python is $(which python)"
echo "PYTHONPATH is $PYTHONPATH"
