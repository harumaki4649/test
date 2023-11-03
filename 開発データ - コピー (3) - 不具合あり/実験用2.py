import pykakasi

kanjis = ['ひらがなのローマ字パターン', 'ジャック']

kks = pykakasi.kakasi()

words = []
converts = {"ん": ["n", "nn"],
            "し": ["si", "shi"],
            "じ": ["zi", "ji"],
            "ち": ["ti", "chi"],
            "つ": ["tu", "tsu"],
            "ふ": ["hu", "hu"],
            "しゃ": ["sya", "sha"],
            "しゅ": ["syu", "shu"],
            "しょ": ["syo", "sho"],
            "じゃ": ["zya", "ja"],
            "じゅ": ["zyu", "ju"],
            "じょ": ["zyo", "jo"],
            "ちゃ": ["tya", "cha"],
            "ちゅ": ["thu", "chu"],
            "ちょ": ["tho", "cho"],
            "しぇ": ["sye", "she"],
            "じぇ": ["zye", "je"],
            "ちぇ": ["tye", "che"],
            "っ": ["xtu", "xtsu"],
            "うぃ": ["whi", "wi"],
            "うぇ": ["whe", "we"],
            "くぁ": ["kwa", "qa"],
            "くぃ": ["kwi", "qi"],
            "くぇ": ["kwe", "qe"],
            "くぉ": ["kwo", "qo"],
            "ふゅ": ["fyu", "hwyu"]}
converts_one = {"てぃ": ["thi"],
                "でぃ": ["dhi"],
                "てゅ": ["thu"],
                "でゅ": ["dhu"],
                "とぅ": ["twu"],
                "どぅ": ["dwu"],
                "あ": ["a"],
                "い": ["i"],
                "う": ["u"],
                "え": ["e"],
                "お": ["o"],
                "か": ["ka"],
                "き": ["ki"],
                "く": ["ku"],
                "け": ["ke"],
                "こ": ["ko"],
                "が": ["ga"],
                "ぎ": ["gi"],
                "ぐ": ["gu"],
                "げ": ["ge"],
                "ご": ["go"],
                "ざ": ["za"],
                "ず": ["zu"],
                "ぜ": ["ze"],
                "ぞ": ["zo"],
                "さ": ["sa"],
                "す": ["su"],
                "せ": ["se"],
                "そ": ["so"]}
for kanji in kanjis:
    result = kks.convert(kanji)
    for data in ["hira"]:
        tmp = ""
        for num in range(len(result)):
            tmp += result[num][data]
    words.append(tmp)
print(words)
bungi = []


def run():
    moji = ""
    datas = []
    for temp in pt:
        for data in temp:
            datas.append(data)
    print(datas)
    bungi.append(datas)
    pass


for word in words:
    moji = ""
    pt = []
    for tmp in word:
        tryok = False
        moji += tmp
        print(tmp, moji)
        try:
            pt.append(converts[tmp])
        except Exception:
            pass
        try:
            pt.append(converts_one[tmp])
        except Exception:
            pass
        try:
            pt.append(converts_one[moji])
            tryok = True
            pt.append(converts[moji])
        except Exception:
            if tryok:
                run()
            else:
                try:
                    pt.append(converts[moji])
                except Exception:
                    run()
    print("==============")
print(bungi)
