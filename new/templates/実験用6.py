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
    words_tmp = r.text.replace(",\r", "").split("\n")
    nums = len(words_tmp)
    kks = pykakasi.kakasi()


    def call_slow_request(old_word):
        word = old_word.split(",")
        if not word in moto_words:
            if int(word[1]) in mode:
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
                print(contains_hiragana_or_non_numeric(wod), not wod in words)
                if contains_hiragana_or_non_numeric(wod) and not wod in words:
                    words.append(wod)
                    moto_words.append(word[0])
                print(wod, word[0], word[1], {len(words)}, {f"{cnt} / {nums}"})


    if __name__ == "__main__":
        while True:
            count = 0
            cnt = 0

            # データが同じ場合排除
            set_B = set(moto_words)  # リストBをセットに変換して高速な検索を可能にする
            list_A = [x for x in words_tmp if x not in set_B]  # リストA内の要素をリストBのセット内で高速に検索
            print(len(list_A), len(words), len(words_tmp))  # 残った要素を表示

            for old_word in words_tmp:
                cnt += 1
                while True:
                    try:
                        call_slow_request(old_word)
                        break
                    except Exception as e:
                        print("エラーが発生しました")
                        print(e)
                        print(old_word)
                count += 1
                if count == 100:
                    count = 0
                    f = open(mondai_path, 'wb')
                    pickle.dump([words, moto_words], f)
                    print("Saveしました")
