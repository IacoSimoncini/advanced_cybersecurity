import lzma
import csv
from os import listdir
from os.path import isfile, join, getsize
import random

path_dir_compressed = "/home/iacos/codes/adv_cyber/compressed/"
path_dir_uncompressed = "/home/iacos/codes/adv_cyber/uncompressed/"

files = [f for f in listdir(path_dir_compressed) if isfile(join(path_dir_compressed, f))]
filew = open(path_dir_uncompressed+"datasetGARR.txt","a")
count = 0


for filename in files:
    try:
        file=lzma.open(path_dir_compressed+filename, mode='rt', encoding='utf-8')
        count+=1
        if count % 50 == 0:
            print("scrittura al "+str(count/2400*100)+"%")
        countLine=0
        domPos=random.randint(0,9)
        for line in file:            
            if domPos==countLine:
                filew.write(line.split(";")[5]+",")   
            countLine+=1
            if countLine==10:
                domPos=random.randint(0,9) 
                countLine=0       
    except EOFError:
        pass