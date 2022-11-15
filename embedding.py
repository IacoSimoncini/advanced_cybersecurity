import fasttext
model = fasttext.train_unsupervised('bigram.txt', "skipgram",dim=128)
#SALVATAGGIO DEL MODELLO
model.save_model('bigram_model.bin')
print(model.words)
"""model = fasttext.load_model("unigram_model.bin")
print(model.words)"""
"""model = fasttext.train_unsupervised('ciao.txt', "skipgram",minCount=1,dim=128,thread=2)
print(model.words)"""