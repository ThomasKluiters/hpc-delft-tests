import os
import subprocess

LOADED_MODULES = False


def ensure_cuda_modules_loaded():
    global LOADED_MODULES
    if not LOADED_MODULES:
        subprocess.call("module use /opt/insy/modulefiles".split(" "))
        subprocess.call("module load cuda/11.2 cudnn/11.2-8.1.1.33".split(" "))
        LOADED_MODULES = True
