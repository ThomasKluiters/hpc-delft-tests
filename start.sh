module use /opt/insy/modulefiles
module load cuda/11.2 cudnn/11.2-8.1.1.33
nohup python main.py > logs.txt &
