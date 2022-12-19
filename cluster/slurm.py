import os
import subprocess


def ensure_cuda_modules_loaded():
    subprocess.call("module use /opt/insy/modulefiles".split(" "))
    subprocess.call("module load cuda/11.2 cudnn/11.2-8.1.1.33".split(" "))
