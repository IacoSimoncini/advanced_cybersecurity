import lzma
import random
import os


def unzip(config):
    
    path_dir_compressed = config['PATH']['PathDirCompressed']
    path_dir_uncompressed = config['PATH']['PathDirUncompressed']
    path_datasetGARR = config['PATH']['PathDatasetGARR']
    
    files = [f for f in os.listdir(path_dir_compressed) if os.path.isfile(os.path.join(path_dir_compressed, f))]
    filew = open(path_datasetGARR,"w")
    count = 0

    for filename in files:
        try:
            file = lzma.open(path_dir_compressed + filename, mode='rt', encoding='utf-8')
            count += 1
            if count % 36 == 0:
                print("scrittura al "+str(count/2880*100)+"%")
            countLine = 0
            domPos = random.randint(0,9)
            for line in file:            
                if domPos == countLine:
                    filew.write(line.split(";")[5]+",")   
                countLine += 1
                if countLine == 10:
                    domPos = random.randint(0,9) 
                    countLine = 0       
        except EOFError:
            pass
