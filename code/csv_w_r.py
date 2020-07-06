import csv
import pandas as pd

new_f = open(r'G:\newlabel.csv','w',newline='')
yishan_f = open(r'G:\yijingshanchu.csv','w',newline='')
yuan_f = open(r'G:\panda\train01.csv')
dele_f = open(r'G:\delet.csv')

try:
    new = csv.writer(new_f)
    double = csv.reader(yuan_f)
    delta = csv.reader(dele_f)
    shan = csv.writer(yishan_f)
    for row in double:
        row_rel = str(row)[2:-2]
        #print('原路径:',row_rel)
        bz=0
        dele_f.seek(0)
        for lie in delta:
            lie_rel = str(lie)[2:-2]
            #print('删路径:',lie_rel)
            if lie_rel==row_rel:
                bz = 1
                break

        if bz==0:
            new.writerow([row_rel])
        elif bz==1:
            shan.writerow([row_rel])
        else:
            print('读取出错，文件出错！！ 路径：',[row_rel])


finally:
    new_f.close()
    yuan_f.close()
    dele_f.close()
    yishan_f.close()