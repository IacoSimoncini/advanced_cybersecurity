import paramiko 
import regex
import random
import configparser
import os

config = configparser.ConfigParser()
config.read('config.ini')

hostname = config['SSH']['Host']
port = int(config['SSH']['Port'])
username = config['SSH']['Username']
password = config['SSH']['Password']

path_VOL250 = config['PATH']['PathVOL250']
path_dir_compressed = config['PATH']['PathDirCompressed']
path_files_divisi = config['PATH']['PathFileDivisi']
path_dir_uncompressed = config['PATH']['PathDirUncompressed']
path_datasetGARR = config['PATH']['PathDatasetGARR']

c_days = [
[30, 25, 2, 9, 12, 29, 14, 3, 24, 4],
[14, 0, 5, 22, 13, 21, 24, 1, 19, 4],
[10, 30, 17, 20, 15, 8, 26, 11, 2, 28],
[22, 7, 23, 29, 11, 6, 27, 13, 9, 15],
[1, 20, 7, 4, 3, 5, 24, 8, 0, 16],
[17, 5, 23, 28, 8, 11, 16, 3, 6, 18],
[4, 25, 6, 3, 22, 17, 7, 28, 29, 14],
[13, 16, 11, 27, 29, 17, 24, 28, 23, 0],
[24, 11, 2, 12, 10, 27, 29, 26, 25, 7],
[4, 27, 3, 26, 16, 9, 0, 30, 25, 5],
[0, 26, 22, 4, 17, 27, 15, 9, 20, 12],
[14, 26, 20, 8, 7, 16, 28, 3, 0, 4]]

def file_divisi(files):
    exists = os.path.exists(path_files_divisi)
    if exists:
        isempty = os.stat(path_files_divisi).st_size == 0
    else:
        isempty = True
    if not isempty and exists:
        file = open(path_files_divisi, "r")
        list_files = []
        for i in range(12):
            list_files.append([])
        for i in range(12):
            list_files[i] = file.readline().split(", ")
        file.close()
        return list_files
    else:
        list_files = []
        for i in range(12):
            list_files.append([])

        for f in files:
            if "2021_10" in f or "2021_11" in f or "2021_12" in f:
                list_files[int(f.split("_")[2]) - 1].append(f)
            elif "2022" in f:
                m = int(f.split("_")[2]) - 1
                if m < 9:
                    list_files[m].append(f)

        filew = open(path_files_divisi, "w")
        for i in list_files:
            for a in i:
                filew.write(a+", ")
            filew.write("\n")

        filew.close()    
        print("ho scritto!")
        return list_files

def download():
    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(port=port, hostname=hostname, username=username, password=password)
        
        with ssh.open_sftp() as sftp:\

            files = sftp.listdir(path_VOL250)
            files_divisi = file_divisi(files)
            
            for i in range(0,12):
                for filename in files_divisi[i]:
                    if filename!='\n':
                        if (int(filename.split("_")[3])-1) in c_days[i]:
                            sftp.get(path_VOL250 + filename, path_dir_compressed + filename) 
                print("completamento: "+str((i+1)*8)+"%")

def unzip():
    import lzma
    files = [f for f in os.listdir(path_dir_compressed) if os.path.isfile(os.path.join(path_dir_compressed, f))]
    filew = open(path_datasetGARR,"a")
    count = 0

    for filename in files:
        try:
            file = lzma.open(path_dir_compressed + filename, mode='rt', encoding='utf-8')
            count += 1
            if count % 50 == 0:
                print("scrittura al "+str(count/2400*100)+"%")
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
