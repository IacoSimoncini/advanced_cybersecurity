def commute_to_unigram(dataset,path):
    with open(dataset, 'r') as f:
        line = f.read()
        unigram = list(line)
        g = open(path, "w")
        for i in unigram:
            if ( i == "."):
                pass
            elif ( i != "\n"):
                g.write(str(i) + ",")
            else:
                g.write(str(i))



#TRASFORMARE IN BIGRAMMI

def commute_to_bigram(dataset,path):
    with open(dataset, 'r') as f:
        line = f.read()
        g = open(path, "w")
        line = line.replace(".","")
        bigram = [line[i:i+2] for i in range(0, len(line) , 1)]
        for i in bigram:
            if ("\n" not in i):
                g.write(i + ",")
            else:
                g.write("\n")


#TRASFORMARE IN TRIGRAMMI

def commute_to_trigram(dataset,path):
    with open(dataset, 'r') as f:
        line = f.read()
        g = open(path, "w")
        line = line.replace(".","")
        trigram = [line[i:i+3] for i in range(0, len(line) , 1)]
        for i in trigram:
            if ("\n" not in i):
                g.write(i + ",")
            else:
                g.write("\n")

def commute_to_123gram(dataset,path_unigram,path_bigram,path_trigram):
    with open(dataset, 'r') as f:
        uni=open(path_unigram, "w")
        bi=open(path_bigram, "w")
        tri=open(path_trigram, "w")
        try:
            
            lines=f.readlines()
            for line in lines:
                line=line.replace(".","")
                uni.write(",".join(list(line)))
                bi.write(",".join([line[i:i+2] for i in range(0, len(line)-2 , 1)]))
                tri.write(",".join([line[i:i+3] for i in range(0, len(line)-3 , 1)]))
        except EOFError:
            pass
def transform(config):
    path_datasetGARR = config['PATH']['PathDatasetGARR']
    path_unigram = config['PATH']['PathUni']
    path_bigram = config['PATH']['PathBi']
    path_trigram = config['PATH']['PathTri']
    #commute_to_unigram(path_datasetGARR, path_unigram)
    #commute_to_bigram(path_datasetGARR, path_bigram)
    #commute_to_trigram(path_datasetGARR, path_trigram)
    commute_to_123gram(path_datasetGARR,path_unigram,path_bigram,path_trigram)