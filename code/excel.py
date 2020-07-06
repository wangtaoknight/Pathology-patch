import csv
import os
from libtiff import TIFF
import imageio
import matplotlib.pyplot as plt
import openslide
import numpy as np

i=1
aimpath = r'G:\panda\train_images'
with open(r'G:\panda\train01.csv', 'r') as f:
    reader = csv.reader(f)
    print(type(reader))
    for row in reader:
        a = str(row)
        a = a[2:-2]
        filepath = os.path.join(aimpath,a + '.tiff')
        try:
            tif = TIFF.open(filepath, mode='r')
        except:
            print('路径出错，文件打不开第%d次'%i)
            i = i+1
            continue
        stack = []
        for picture in list(tif.iter_images()):
            stack.append(picture)
        stack_num = np.array(stack)
        f_picture = stack_num[2]
        imageio.imwrite(r'G:\panda_round\ '+a + '_2.jpg', f_picture)

