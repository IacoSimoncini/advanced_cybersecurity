import random
import paramiko
import configparser
import os





c_days=[
[14, 10, 23, 11, 6, 24, 16, 18, 20, 13], #JUNE20        
[19, 28, 26, 25, 7, 23, 1, 16, 15, 13], #JULY20
[30, 25, 2, 9, 12, 29, 14, 27, 24, 6], #AUGUST20
[1, 9, 8], #SEPTEMBER20 (3)
[27], #FEBRUARY21 (2)  #change 28
[22, 7, 23, 29, 11, 6, 27, 13, 9, 15], #MARCH21
[1, 20, 7, 11, 28, 5, 24, 8, 0, 16], #APRIL21  #change3
[17, 5, 23, 28, 8, 11, 16, 3, 6, 18], #MAY21
[4, 23, 6, 3, 22, 17, 7, 28, 29, 14], #JUNE21
[13, 16, 11, 27, 29, 17, 24, 28, 23, 0], #JULY21
[24, 11, 2, 12, 10, 27, 29, 26, 25, 7], #AUGUST21
[4, 27, 3, 26, 16, 9, 0, 20, 25, 5], #SEPTEMEBR21
[0, 26, 22, 4, 17, 27, 15, 9, 20, 12], #OCTOBER21
[13, 4, 16, 11, 12, 7] #NOVEMEBR 21 (5)   
]
c_hours=[
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
        for i in range(14):
            list_files.append([])
        for i in range(14):
            list_files[i] = file.readline().split(", ")
        file.close()
        return list_files
    else:
        list_files = []
        for i in range(14):
            list_files.append([])
        
        for f in files:
            if "pdns" in f:
                m=int(f.split("_")[2])
                if "2021" in f and m != 1 and m!=12:
                    list_files[m+2].append(f)
                elif "2020" in f and m>5 and m<10:
                    list_files[m-6].append(f)

        filew = open(path_separated_files, "w")
        for i in list_files:
            for a in i:
                filew.write(a+", ")
            filew.write("\n")

        filew.close()    
        
        return list_files

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
        
            for m in range(0,14):
                
                for filename in separated_files[m]:
                    if not os.path.exists(path_dir_compressed + filename):
                        if filename!='\n':
                            g=int(filename.split("_")[3])-1
                            if g in c_days[m]:
                                h=int(filename.split("_")[4].split(".")[0])
                                try:
                                    if (h == c_hours[m][c_days[m].index(g)]):
                                        sftp.get(path_VOL250 + filename, path_dir_compressed + filename) 
                                except:
                                    pass
                count+=len(c_days[m])
                print(str(count/120*100)+"% "+"of files downloaded")
