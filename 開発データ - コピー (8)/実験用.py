import pykakasi

kanjis = ['ひらがなのローマ字パターン', 'ジャック']

kks = pykakasi.kakasi()

words = []
for kanji in kanjis:
    word = []
    result = kks.convert(kanji)
    print(result)
    for data in ["orig", "hira", "kana", "hepburn", "kunrei", "passport"]:
        tmp = ""
        for num in range(len(result)):
            tmp += result[num][data]
        word.append(tmp)
    words.append(word)
print(words)
