import os


def ensure_cuda_modules_loaded():
    os.system("module use /opt/insy/modulefiles")
    os.system("module load cudnn/11.2-8.1.1.33 cuda/11.2")
