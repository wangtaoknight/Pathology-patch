import matplotlib.pyplot as plt
from scipy import misc
import scipy
import csv
import os

i = 1
filepath = open(r'G:\delet.csv')
file = csv.reader(filepath)
for row in file:
    pathq = str(row)[2:-2]
    path = os.path.join('G:\panda_round\ ' + pathq + '_2.jpg')
    print(path)
    img = misc.imread(path)
    plt.figure(num='对比显示', figsize=(8,60))
    #axs = plt.subplot(8,2)
    #plt.imshow(img)
    #plt.figure()
    plt.subplot(20,2,i)  # facecolor指定背景颜色 在之前的Python版本使用的是axisbg 现在已经改成了facecolor
    plt.imshow(img)
    i +=1
    if i ==41:
        break
plt.savefig('G:/result.jpg',dpi =500)
plt.show()
