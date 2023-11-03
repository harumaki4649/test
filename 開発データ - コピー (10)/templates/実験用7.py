import os
import re
import json
import pickle
import time

import pykakasi
import requests

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


def contains_only_english(text):
    pattern = re.compile(r'^[a-zA-Z\s.]+$')  # 英語のアルファベット、空白、ピリオドのみを許容

    if pattern.match(text):
        return True  # テキストが英語のみを含む場合はTrueを返す
    else:
        return False  # 英語以外の文字が含まれている場合はFalseを返す


r = requests.get("https://tango-gacha.com/googleanalytics.jpg?ver=2")
if r.ok:
    # Lv1(基礎語)
    # Lv2(日用語)
    # Lv3(常用語)
    # Lv4(発展語)
    # Lv5(高度語)
    mode = [1, 2, 3]
    words_tmp = r.text.replace(",\r", "").split("\n")
    nums = len(words_tmp)
    kks = pykakasi.kakasi()


    def call_slow_request(old_word):
        word = old_word.split(",")
        if word[0] == "":
            return
        if not word in moto_words:
            if "Don" in word[1] or "feel." in word[1]:
                return
            if word[1] == "x":
                md = 2
            else:
                md = 1
            try:
                if int(word[md].replace("\r", "")) in mode and not word[0] in moto_words:
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
                    }
                    r = requests.get(f"https://api.excelapi.org/language/kanji2kana?text={word[0]}", headers=headers)
                    while "ERROR" in r.text:
                        print(r.text)
                        print("レート制限を検知しました。\n10秒後リトライします。")
                        time.sleep(10)
                        r = requests.get(f"https://api.excelapi.org/language/kanji2kana?text={word[0]}", headers=headers)
                    result = kks.convert(r.text)
                    for data in ["hira"]:
                        wod = ""
                        for num in range(len(result)):
                            wod += result[num][data]
                    words.append(wod)
                    moto_words.append(word[0])
                    print(wod, word[0], word[1], {len(words)}, {f"{cnt} / {nums}"})
                    return
            except Exception as e:
                print(e)
                print("スキップしました")
            print(word[0], word[1], {len(words)}, {f"{cnt} / {nums}"})


    if __name__ == "__main__":
        count = 0
        cnt = 0

        # データが同じ場合排除
        set_B = set(moto_words)  # リストBをセットに変換して高速な検索を可能にする
        list_A = [x for x in words_tmp if x not in set_B]  # リストA内の要素をリストBのセット内で高速に検索
        print(len(list_A), len(words), len(words_tmp))  # 残った要素を表示

        for old_word in words_tmp:
            cnt += 1
            while True:
                # try:
                call_slow_request(old_word)
                break
            # except Exception as e:
            #    print("エラーが発生しました")
            #    print(e)
            #    print(old_word)
            count += 1
            if count == 100:
                count = 0
                f = open(mondai_path, 'wb')
                pickle.dump([words, moto_words], f)
                f.close()
                print("Saveしました")
