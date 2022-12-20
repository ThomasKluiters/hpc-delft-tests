import os
import subprocess

LOADED_MODULES = False


def ensure_cuda_modules_loaded():
    global LOADED_MODULES
    if not LOADED_MODULES:
        #subprocess.call("/usr/share/lmod/lmod/libexec/lmod load cuda/11.2 cudnn/11.2-8.1.1.33 bash", shell=True)
        os.system("module use /opt/insy/modulefiles && module load cuda/11.2 cudnn/11.2-8.1.1.33")
        LOADED_MODULES = True
