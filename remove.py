import os
import numpy as np

def remove(config):
    path_datasetGARR = config['PATH']['PathDatasetGARR']
    path_datasetGARR_cleaned = config['PATH']['PathDatasetGARRCleaned']

    new_data=open(path_datasetGARR_cleaned,'w')
    filer= open(path_datasetGARR,'r')
    dataset=filer.readlines()
    names=set()
    print(str(len({'a','a','b'})))
    print(str(len(dataset)))
    for d in dataset:
        names.add(d)
    print(str(len(names)))

    
    

    

