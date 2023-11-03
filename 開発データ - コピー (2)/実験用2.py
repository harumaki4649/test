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
            "ちゃ": [],
            "ちゅ": [],
            "ちょ": [],
            "しぇ": [],
            "じぇ": [],
            "ちぇ": [],
            "っ": [],
            "うぃ": [],
            "うぇ": [],
            "くぁ": [],
            "くぃ": [],
            "くぇ": [],
            "くぉ": [],
            "てぃ": [],
            "でぃ": [],
            "てゅ": [],
            "とぅ": [],
            "どぅ": [],
            "ふゅ": []}
for kanji in kanjis:
    result = kks.convert(kanji)
    for data in ["hira"]:
        tmp = ""
        for num in range(len(result)):
            tmp += result[num][data]
    words.append(tmp)
print(words)
