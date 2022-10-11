import random
import paramiko
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

c_days=[
[14, 10, 23, 11, 6, 24, 16, 18, 20, 13], #GIUGNO20        
[19, 28, 26, 25, 7, 23, 1, 16, 15, 13], #LUGLIO20
[30, 25, 2, 9, 12, 29, 14, 27, 24, 6], #AGOSTO20
[1, 9, 8], #SETTEMBRE20 (3)
[28,27], #FEBBRAIO21 (2)
[22, 7, 23, 29, 11, 6, 27, 13, 9, 15], #MARZO21
[1, 20, 7, 11, 3, 5, 24, 8, 0, 16], #APRILE21
[17, 5, 23, 28, 8, 11, 16, 3, 6, 18], #MAGGIO21
[4, 23, 6, 3, 22, 17, 7, 28, 29, 14], #GIUGNO21
[13, 16, 11, 27, 29, 17, 24, 28, 23, 0], #LUGLIO21
[24, 11, 2, 12, 10, 27, 29, 26, 25, 7], #AGOSTO21
[4, 27, 3, 26, 16, 9, 0, 30, 25, 5], #SETTEMBRE21
[0, 26, 22, 4, 17, 27, 15, 9, 20, 12], #OTTOBRE21
[13, 4, 16, 11, 12] #NOVEMBRE 21 (5)   
] 
#I MESI CON PARENTESI INSIEME FANNO UN MESE INTERO

def file_divisi(files):
    exists = os.path.exists(path_files_divisi)
    if exists:
        isempty = os.stat(path_files_divisi).st_size == 0
    else:
        isempty = True
    if not isempty and exists:
        file = open(path_files_divisi, "r")
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
            
            
            if "2021" in f and m != 1 and m!=12:
                m=int(f.split("_")[2])
                list_files[m+2].append(f)
            elif "2020" in f and m>5 and m<10:
                m=int(f.split("_")[2])
                list_files[m-6].append(f)

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
            count=0

            for i in range(0,14):
                for filename in files_divisi[i]:
                    if filename!='\n':
                        if (int(filename.split("_")[3])-1) in c_days[i]:
                            sftp.get(path_VOL250 + filename, path_dir_compressed + filename) 
                count+=len(c_days[i])
                print("completamento: "+str(count/120*100)+"%")
def unzip():
    import lzma
    files = [f for f in os.listdir(path_dir_compressed) if os.path.isfile(os.path.join(path_dir_compressed, f))]
    filew = open(path_datasetGARR,"a")
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
