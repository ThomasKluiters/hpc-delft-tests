import dask
import sys
from distributed import Client
from dask_jobqueue import SLURMCluster
import os
quality_of_service = "short"
partition = "general"
time = "0:01:00"

cluster = SLURMCluster(
    cores=2,
    processes=2,
    queue="tmkluiters",
    memory="12 GB",
    job_extra_directives=[f'--qos="{quality_of_service}"', f'--partition={partition}', f'--time={time}', f'--gres={"gpu:turing:1"}'],
)
cluster.scale(2)
client = Client(cluster)

@dask.delayed
def inc():
   from tensorflow.python.client import device_lib
   import platform
   #os.system("module use /opt/insy/modulefiles")
   #os.system("module load cuda/11.2")
   platform =(platform.node())
   return [platform] + (device_lib.list_local_devices())


@dask.delayed
def add(x, y):
   return x + y

a = inc()       # no work has happened yet
b = inc()       # no work has happened yet
c = add(a, b)    # no work has happened yet


c = c.compute()  # This triggers all of the above computations

print(c)
