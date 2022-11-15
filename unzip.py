
import lzma

import random
import os
from time import sleep

def domain_isclean(domain):
    lung=len(domain)
    if lung<3 or lung>99:
        return False
    domain_splitted=domain.split('.')
    count_num=0
    for i,d in enumerate(domain_splitted):
        if i>3:
            break
        if d.isdigit():
            count_num+=1
    if "in_addr" in domain:
        return False
    if count_num>1:
        return False
    return True
    
def write_domains(domain_set,path_datasetGARR,total_domains):
    filew = open(path_datasetGARR,"w")

    for i,domain in enumerate(domain_set):
        filew.write(domain+"\n")
        if i%200000==0:
            print(str(round(i/total_domains*100))+"% "+"of domains name written ")

def read_GARR(path_data):
    filer = open(path_data,"r")
    return set(filer.readlines())

def unzip(config):
    
    path_dir_compressed = config['PATH']['PathDirCompressed']#config['PATH']['PathExtraData'] 
    path_datasetGARR = config['PATH']['PathDatasetGARR']
    
    files = [f for f in os.listdir(path_dir_compressed) if os.path.isfile(os.path.join(path_dir_compressed, f))]
    
    count = 0
   
    domain_set=set()
    #domain_set=read_GARR(path_datasetGARR)

    for filename in files:
        try:
            
            
            try:

                            
                file = lzma.open(path_dir_compressed + filename, mode='rt', encoding='utf-8')
                    
                    
                count += 1
                    
                if count % 5 == 0:
                    print(str(round(count/506*100))+"% "+"of dataset read ")
                countLine = 0
                domPos = random.randint(0,9)
                resPos= random.randint(0,9)
                if resPos==domPos:
                    resPos=abs(resPos-1)
                
                for line in file:            
                    if domPos == countLine:
                        domain=line.split(";")[5]
                        domain=domain.split(",")[0]
                        domain=domain.lower()
                       
                        check=domain_isclean(domain)
                        if check:                                          
                            domain_set.add(domain)
                    if resPos==countLine:
                        reserve=line.split(";")[5]
                        reserve=reserve.split(",")[0]
                        reserve=reserve.lower()
                    countLine += 1
                    if countLine == 10:
                        if not check:                            
                            if domain_isclean(reserve):
                                domain_set.add(reserve)
                        domPos = random.randint(0,9) 
                        resPos= random.randint(0,9)
                        if resPos==domPos:
                            resPos=abs(resPos-1)
                        countLine = 0   
                          
                

                    
            except Exception as e:
                print(e)
        except EOFError:
            pass
    total_domains=len(domain_set)
    print("All the files are been read. Writing of "+ str(total_domains)+ " Domains name will be start in 10 seconds unless you stop it.")
    sleep(10)
    print("write started")
    write_domains(domain_set,path_datasetGARR,total_domains)

