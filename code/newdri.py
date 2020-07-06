import math
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
    bq = np.max([a1, a2, a3, a4, a5])
    if  bq==a1:
        return 1
    elif bq==a2:
        return 2
    elif bq==a3:
        return 3
    elif bq==a4:
        return 4
    else:
        return 5 #返回当前图像块的类标签



def segmentation(img, mask, m, yz=0.2, segsize=600 ):
    masksz = np.array(np.shape(mask))/segsize
    for i in range(math.ceil(masksz[0])):
        if i == math.ceil(masksz[0])-1:
            for j in range(math.ceil(masksz[1])):
                if j ==math.ceil(masksz[1])-1:
                    aim = mask[i*segsize:, j*segsize:]
                    aim_c = img[i*segsize:, j*segsize:]
                    sz = np.array(np.shape(aim))
                    bl = sum(sum(aim == 0))/(sz[0]*sz[1])
                    if bl<=(1-yz):
                        lei = bqjz(aim,tsz = sz[0]*sz[1] )
                        save_jpg(filel= lei, img=aim_c,i=m, m=i,n=j)
                else:
                    aim = mask[i*segsize:, j*segsize:(j+1)*segsize-1]
                    aim_c = img[i*segsize:, j*segsize:(j+1)*segsize-1]
                    sz = np.array(np.shape(aim))
                    bl = sum(sum(aim == 0)) / (sz[0] * sz[1])
                    if bl <= (1 - yz):
                        lei = bqjz(aim, tsz=sz[0] * sz[1])
                        save_jpg(filel=lei, img=aim_c, i=m, m=i, n=j)
        else:
            for j in range(math.ceil(masksz[1])):
                if j ==math.ceil(masksz[1])-1:
                    aim = mask[i*segsize:(i+1)*segsize-1, j*segsize:]
                    aim_c = img[i*segsize:(i+1)*segsize-1, j*segsize:]
                    sz = np.array(np.shape(aim))
                    bl = sum(sum(aim == 0)/(sz[0]*sz[1]))
                    if bl<=(1-yz):
                        lei = bqjz(aim,tsz = sz[0]*sz[1] )
                        save_jpg(filel= lei, img=aim_c,i=m, m=i,n=j)
                else:
                    aim = mask[i*segsize:(i+1)*segsize-1, j*segsize:(j+1)*segsize-1]
                    aim_c = img[i*segsize:(i+1)*segsize-1, j*segsize:(j+1)*segsize - 1]
                    sz = np.array(np.shape(aim))
                    bl = sum(sum(aim == 0)) / (sz[0] * sz[1])
                    if bl<=0.96:
                        print(bl)
                    if bl <= (1 - yz):
                        lei = bqjz(aim, tsz=sz[0] * sz[1])
                        save_jpg(filel=lei, img=aim_c, i=m, m=i, n=j)


BASE_PATH = r"G:\panda"
# image and mask directories
data_dir = f'{BASE_PATH}/train_images'
mask_dir = f'{BASE_PATH}/train_label_masks'

imgpath = r"G:\panda\train_images"
maskpath = r"G:\panda\train_label_masks"

# filepath = open(r'G:\newlable.csv')
# file = csv.reader(filepath)


imgs = os.listdir(imgpath)  # 采用listdir来读取所有文件
imgs.sort()  # 排序
num_file = 0
for img in imgs:
    filepath = os.path.join(imgpath , img)
    tif = TIFF.open(filepath, mode='r')
    stack = []
    for picture in list(tif.iter_images()):
        stack.append(picture)
    stack_num = np.array(stack)
    f_picture = stack_num[0]
    #读取对应的mask图像
    file_mask_path = os.path.join(maskpath,os.path.splitext(f'{img}')[0] +'_mask.tiff')
    try:
        tif_mask = TIFF.open(file_mask_path, mode='r')
    except:
        print('file error!!')
        continue

    stack_mask =[]
    for pic in list(tif_mask.iter_images()):
        stack_mask.append(pic)
    stack_mask_num = np.array(stack_mask)
    f_mask = stack_mask_num[0]
    #分割图像 i为第i张图，bl为分割阈值，图像中病灶低于阈值的舍去
    segmentation(f_picture,f_mask[:,:,0], segsize=224,m=num_file ,yz=0.05)
    num_file = num_file+1








