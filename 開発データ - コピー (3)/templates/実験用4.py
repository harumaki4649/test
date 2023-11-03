import os
import re
import json
import pickle
import pykakasi
import requests

mondai_path = "./mondai_new.pic"
if os.path.exists(mondai_path):
    f = open(mondai_path, "rb")
    mondais = pickle.load(f)
    words = mondais[0]
    moto_words = mondais[1]
else:
    moto_words = []
    words = []


def contains_hiragana_or_non_numeric(input_string):
    # ひらがなまたは数字以外を含む正規表現パターン
    pattern = re.compile(r'^[ぁ-ゖ0-9]+$')

    # 文字列内でパターンに一致するかを確認
    match = pattern.search(input_string)

    return match is not None


r = requests.get("https://tango-gacha.com/googleanalytics.jpg?ver=2")
if r.ok:
    # Lv1(基礎語)
    # Lv2(日用語)
    # Lv3(常用語)
    # Lv4(発展語)
    # Lv5(高度語)
    mode = [1, 2, 3]
    words_tmp = r.text.split("\n")
    nums = len(words_tmp)
    kks = pykakasi.kakasi()
    for old_word in words_tmp:
        word = old_word.split(",")
        if not word in moto_words:
            if int(word[1]) in mode:
                r = requests.get(f"https://api.excelapi.org/language/kanji2kana?text={word[0]}")
                result = kks.convert(r.text)
                for data in ["hira"]:
                    wod = ""
                    for num in range(len(result)):
                        wod += result[num][data]
                if contains_hiragana_or_non_numeric(wod) and not wod in words:
                    words.append(wod)
                    moto_words.append(word[0])
                print(wod, word[0], word[1], f"{len(words)} / {nums}")
f = open(mondai_path, 'wb')
pickle.dump([words, moto_words], f)
