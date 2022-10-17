import os


progress=0
def check_progress(count):
    global progress
    if count % 39900000==0:
        progress+=1
        print(str(progress)+"% "+"of file cleaned")

def no_reverse_lookup(domain):
    if domain.split('.')[0].isdigit():
        return False
    return True


def clean(config):
    path_datasetGARR = config['PATH']['PathDatasetGARR']
    path_datasetGARR_cleaned = config['PATH']['PathDatasetGARRCleaned']

    new_data=open(path_datasetGARR_cleaned,'w')
    dataset=open(path_datasetGARR, "r")
    chunk=dataset.read(1)
    count=1
    
    while chunk!="":        
        domain=""
        while chunk != ",":
            domain+=chunk
            chunk=dataset.read(1)
            count+=1
            check_progress(count)
        check_progress(count)
        lung=len(domain)
        if lung>2 and lung<100:
            if no_reverse_lookup(domain):
                new_data.write(domain+"\n")            
        chunk=dataset.read(1) 
        count+=1
    

    

