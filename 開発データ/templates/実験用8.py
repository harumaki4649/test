import re


def contains_only_english(text):
    pattern = re.compile(r'^[a-zA-Z\s.]+$')  # 英語のアルファベット、空白、ピリオドのみを許容

    if pattern.match(text):
        return True  # テキストが英語のみを含む場合はTrueを返す
    else:
        return False  # 英語以外の文字が含まれている場合はFalseを返す


# テスト用の文字列
text1 = "words."
text2 = "これは日本語の文章です。"
text3 = "period"

# 文字列が英語のみかどうかをチェック
print(contains_only_english(text1))  # 出力: True
print(contains_only_english(text2))  # 出力: False
print(contains_only_english(text3))  # 出力: True
