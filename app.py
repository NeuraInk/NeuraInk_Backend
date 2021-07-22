import os
command = "python test.py --dataroot {} --name {} --results_dir {} --gpu_ids -1 --model test --no_dropout --load_size {} --crop_size {} --display_winsize {}"
dataroot = "/home/ubuntu/cyclegan/datasets/testA"
name = "inkwash"
results_dir = "/home/ubuntu/cyclegan/datasets/testA"
load_size = "256"
crop_size = "256"
display_winsize = "256"

os.system(command.format(dataroot,name,results_dir,load_size,crop_size,display_winsize))