from operator import truediv

import paramiko
import os

"""
DECOMMENTA E RUNNA PER SINGOLO DOWNLOAD VELOCE

import configparser

config = configparser.ConfigParser()
config.read('config.ini')
hostname = config['SSH']['Host']
port = int(config['SSH']['Port'])
username = config['SSH']['Username']
password = config['SSH']['Password']
path_dir_compressed = config['PATH']['PathExtraData']
path_VOL250 = config['PATH']['PathVOL250']
with paramiko.SSHClient() as ssh:
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(port=port, hostname=hostname, username=username, password=password)
    with ssh.open_sftp() as sftp:\
        sftp.get(path_VOL250 + "pdns_2019_10_21_14.log.xz", path_dir_compressed + "pdns_2019_10_21_14.log.xz")""" 


c_days=[
[30, 8, 6, 3, 16, 18, 20, 9, 25, 12],#JULY19
[13, 11, 17, 27, 8, 0, 25, 10, 22, 21],#AUGUST19
[4, 28, 1, 0, 29, 18, 11, 17, 14, 6],#SEPTEMBER19
[2, 17, 10, 15, 6, 1, 27, 13, 8, 20],#OCTOBER19
[18, 10, 19, 16, 14, 15, 1, 28, 20, 21], #MAY20
[14, 10, 23, 11, 6, 24, 16, 18, 20, 13], #JUNE20        
[19, 28, 26, 25, 7, 23, 1, 16, 15, 13], #JULY20
[30, 25, 2, 9, 12, 29, 14, 27, 24, 6], #AUGUST20
[1, 9, 8], #SEPTEMBER20 (3)
[27], #FEBRUARY21 (1)  
[22, 7, 23, 29, 11, 6, 27, 13, 9, 15], #MARCH21
[1, 20, 7, 11, 28, 5, 24, 8, 0, 16], #APRIL21
[17, 5, 23, 28, 8, 11, 16, 3, 6, 18], #MAY21
[4, 23, 6, 3, 22, 17, 7, 28, 29, 14], #JUNE21
[13, 16, 11, 27, 29, 17, 24, 28, 23, 0], #JULY21
[24, 11, 2, 12, 10, 27, 29, 26, 25, 7], #AUGUST21
[4, 27, 3, 26, 16, 9, 0, 20, 25, 5], #SEPTEMEBR21
[0, 26, 22, 4, 17, 27, 15, 9, 20, 12], #OCTOBER21
[13, 4, 16, 11, 12, 7] #NOVEMBER 21 (6)
]
c_hours=[
[21, 8, 12, 19, 22, 3, 2, 18, 10, 1],#JULY19
[19, 17, 18, 0, 2, 22, 12, 21, 15, 13],#AUGUST19
[18, 17, 4, 12, 11, 15, 21, 23, 2, 16],#SEPTEMBER19
[21, 10, 5, 1, 15, 14, 17, 12, 0, 7],#OCTOBER19
[1, 7, 15, 22, 9, 10, 14, 0, 11, 16], #MAY20
[18, 17, 22, 15, 23, 1, 2, 16, 10, 5], #JUNE20
[21, 1, 10, 22, 2, 16, 20, 19, 18, 7], #JULY20
[23, 3, 0, 18, 13, 4, 17, 19, 14, 18], #AUGUST20
[20, 0, 11], #SEPTEMBER20
[22, 16], #FEBRUARY21
[4, 13, 7, 11, 0, 3, 14, 9, 6, 12], #MARCH21
[6, 19, 5, 7, 21, 20, 9, 6, 12, 1], #APRIL21
[3, 20, 9, 1, 10, 16, 13, 2, 7, 21], #MAY21
[13, 10, 5, 21, 3, 1, 16, 8, 19, 6], #JUNE21
[22, 16, 4, 0, 17, 12, 19, 7, 15, 5], #JULY21
[19, 9, 0, 12, 11, 22, 21, 15, 6, 18], #AUGUST21
[7, 19, 14, 11, 12, 8, 22, 1, 6, 18], #SEPTEMBER21
[13, 9, 21, 23, 8, 16, 17, 5, 10, 11], #OCTOBER21
[7, 23, 14, 6, 8, 11] #NOVEMBER21
]


def files_separator(files,path_separated_files):

    exists = os.path.exists(path_separated_files)
    if exists:
        isempty = os.stat(path_separated_files).st_size == 0
    else:
        isempty = True
    if not isempty and exists:
        file = open(path_separated_files, "r")
        list_files = []
        for i in range(len(c_days)):
            list_files.append([])
        for i in range(len(c_days)):
            list_files[i] = file.readline().split(", ")
        file.close()
        return list_files
    else:
        list_files = []
        for i in range(len(c_days)):
            list_files.append([])
        
        for f in files:
            if "pdns" in f:
                m=int(f.split("_")[2])
                if "2021" in f and m != 1 and m!=12:
                    list_files[m+7].append(f)
                elif "2020" in f and m>4 and m<10:
                    list_files[m-1].append(f)
                elif "2019" in f and m>6 and m<11:
                    list_files[m-7].append(f)

        filew = open(path_separated_files, "w")
        for i in list_files:
            for a in i:
                filew.write(a+", ")
            filew.write("\n")

        filew.close()    
        
        return list_files
def check_hour(h,g,m):

    h1=abs(h-c_hours[m][c_days[m].index(g)])
    if h1==0:
        return True

    if h1==8 or h1==16:
        return True
    
    return False
def download(config):
    hostname = config['SSH']['Host']
    port = int(config['SSH']['Port'])
    username = config['SSH']['Username']
    password = config['SSH']['Password']

    path_VOL250 = config['PATH']['PathVOL250']
    path_dir_compressed = config['PATH']['PathDirCompressed']
    path_separated_files = config['PATH']['PathSeparatedFiles']
    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(port=port, hostname=hostname, username=username, password=password)
        
        with ssh.open_sftp() as sftp:\

            files = sftp.listdir(path_VOL250)
            separated_files = files_separator(files,path_separated_files)
            count=0
        
            for m in range(0, len(c_days)): 
                
                for filename in separated_files[m]:
                    if not os.path.exists(path_dir_compressed + filename):
                        if filename!='\n':
                            g=int(filename.split("_")[3])-1
                            if g in c_days[m]:
                                h=int(filename.split("_")[4].split(".")[0])
                                try:
                                    if (check_hour(h,g,m)):
                                        sftp.get(path_VOL250 + filename, path_dir_compressed + filename) 
                                except:
                                    pass
                count+=1
                print(str(count/len(c_days)*100)+"% "+"of files downloaded")  
