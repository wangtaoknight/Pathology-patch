import math
import csv
import os
from libtiff import TIFF
import imageio
import matplotlib.pyplot as plt
import openslide
import numpy as np
import cv2
from scipy import misc
import time
start = time.time()

def save_jpg(filel,img,i,m, n):
    if filel==1:
        imageio.imwrite(r'H:\train\1\ ' + '%d'%i+ '_'+'%d'%m+ '_'+'%d'%n+'.jpg', img)
    elif filel ==2:
        imageio.imwrite(r'H:\train\2\ ' + '%d'%i+ '_'+'%d'%m+ '_'+'%d'%n+'.jpg', img)
    elif filel == 3:
        imageio.imwrite(r'H:\train\3\ ' + '%d'%i+ '_'+'%d'%m+ '_'+'%d'%n+'.jpg', img)
    elif filel == 4:
        imageio.imwrite(r'H:\train\4\ ' + '%d'%i+ '_'+'%d'%m+ '_'+'%d'%n+'.jpg', img)
    elif filel == 5:
        imageio.imwrite(r'H:\train\5\ ' + '%d'%i+ '_'+'%d'%m+ '_'+'%d'%n+'.jpg', img)
    else:
        print('警告：出错，不只五类！！')

def bqjz(array,tsz):
    a0 = sum(sum(array == 0))
    a1 = sum(sum(array == 1))
    a2 = sum(sum(array == 2))
    a3 = sum(sum(array == 3))
    a4 = sum(sum(array == 4))
    a5 = sum(sum(array == 5))
    he = a0 + a1 + a2 + a3 + a4 + a5;
    if not he==tsz:
        print('警告：不只五类图像',tsz,'不等于',he)
    bq = [a1, a2, a3, a4, a5]
    bq.sort()

    if  bq[4]==a1:
        fh = 1
    elif bq[4]==a2:
        fh = 2
    elif bq[4]==a3:
        fh = 3
    elif bq[4]==a4:
        fh = 4
    else:
        fh = 5 #返回当前图像块的类标签
    if bq[0]+bq[1]+bq[2]>0:
        fh = 0
    elif bq[3]/(bq[3]+bq[4])>0.1:  #如果第二类占比大于10%则舍去该图
        fh=0
    return fh


def segmentation(img, mask, m, yz=0.2, segsize=600 ):
    masksz = np.array(np.shape(mask))/segsize
    for i in range(math.ceil(masksz[0])):
        if i == math.ceil(masksz[0])-1:
            pass
        else:
            for j in range(math.ceil(masksz[1])):
                if j ==math.ceil(masksz[1])-1:
                    pass
                else:
                    aim = mask[i*segsize:(i+1)*segsize-1, j*segsize:(j+1)*segsize-1]
                    aim_c = img[i*segsize:(i+1)*segsize-1, j*segsize:(j+1)*segsize - 1]
                    sz = np.array(np.shape(aim))
                    bl = sum(sum(aim == 0)) / (sz[0] * sz[1])
                    if bl <= (1 - yz):
                        lei = bqjz(aim, tsz=sz[0] * sz[1])
                        if lei>0:
                            save_jpg(filel=lei, img=aim_c, i=m, m=i, n=j)
                            print('图像比例为:',bl,'    ','第%d张图像'%m)



BASE_PATH = r"G:\panda"
# image and mask directories
data_dir = f'{BASE_PATH}/train_images'
mask_dir = f'{BASE_PATH}/train_label_masks'

imgpath = r"G:\panda\train_images"
maskpath = r"G:\panda\train_label_masks"

filepath = open(r'G:\newlabel.csv')
file = csv.reader(filepath)
#for row in file:
#    filepath= r'G:\panda\train_images\ ' + str(row)[2:-2] + '.tiff'
#    file_mask_path = r'G:\panda\train_label_masks\ ' + str(row)[2:-2] + '_mask.tiff'

#imgs = os.listdir(imgpath)  # 采用listdir来读取所有文件
#imgs.sort()  # 排序
num_file = 0    #用以计数总共几张图

for row in file:
    if num_file<=2502:
        num_file = num_file+1
        print('第%d张图片'%num_file)
        continue
    filepath = r'G:\panda\train_images\\' + str(row)[2:-2] + '.tiff'
    file_mask_path = r'G:\panda\train_label_masks\\' + str(row)[2:-2] + '_mask.tiff'
    #filepath = os.path.join(imgpath , img)  ####
    try:
        tif = TIFF.open(filepath, mode='r')
    except:
        print('图像路径出错:', filepath)
        continue
    stack = []
    for picture in list(tif.iter_images()):
        stack.append(picture)
    stack_num = np.array(stack)
    f_picture = stack_num[0]
    #读取对应的mask图像
    #file_mask_path = os.path.join(maskpath,os.path.splitext(f'{img}')[0] +'_mask.tiff')
    try:
        tif_mask = TIFF.open(file_mask_path, mode='r')
    except:
        print('Msk_file error!!')
        continue

    stack_mask =[]
    for pic in list(tif_mask.iter_images()):
        stack_mask.append(pic)
    stack_mask_num = np.array(stack_mask)
    f_mask = stack_mask_num[0]
    #分割图像 i为第i张图，bl为分割阈值，图像中病灶低于阈值的舍去
    segmentation(f_picture,f_mask[:,:,0], segsize=225,m=num_file ,yz=0.98)
    num_file = num_file+1








