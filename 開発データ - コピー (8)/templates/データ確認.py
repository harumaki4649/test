import os
import pickle

mondai_path = "./mondai_new.pic"
if os.path.exists(mondai_path):
    f = open(mondai_path, "rb")
    mondais = pickle.load(f)
    f.close()
    words = mondais[0]
    moto_words = mondais[1]
else:
    moto_words = []
    words = []

for num in range(len(words)):
    print(words[num], moto_words[num])
