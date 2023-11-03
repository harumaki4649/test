import os
import re
import json
import pickle
import pykakasi
import requests

mondai_path = "./mondai.pic"
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


def hiragana_convert(moto):
    # APIはこちら https://labs.goo.ne.jp/apiusage/
    r = requests.post("https://labs.goo.ne.jp/api/hiragana",
                      data={"app_id": "f6405c0a382ca73ba2827659b540138657c149c7a78458f2ff43bc6698180729",
                            "output_type": "hiragana",
                            "sentence": moto})
    return r.json()["converted"]


min = 3
max = 15
kks = pykakasi.kakasi()
while not len(words) >= 6647:
    # r = requests.get("https://random-word-api.herokuapp.com/word?number=1000")
    # r = requests.get(f"https://random-word.ryanrk.com/api/jp/word/random?minlength={min}&maxlength={max}")
    # r = requests.get("https://random-word-api.vercel.app/api?words=100")
    r = requests.get("https://tango-gacha.com/API/")
    for tmp in r.json()["words"]:
        try:
            if min <= len(tmp) <= max and not tmp in moto_words:
                result = kks.convert(tmp)
                for data in ["hira"]:
                    tmp2 = ""
                    for num in range(len(result)):
                        tmp2 += result[num][data]
                if contains_hiragana_or_non_numeric(tmp2) and not tmp2 in words:
                    words.append(tmp2)
                    moto_words.append(tmp)

                print(tmp, tmp2, len(words))
        except Exception:
            pass
f = open(mondai_path, 'wb')
pickle.dump([words, moto_words], f)
