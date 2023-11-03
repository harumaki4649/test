import random
import pykakasi
import requests
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
# import gmail_check_api
# pip install Flask-SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask

app = Flask(__name__, static_folder="./static")
# app.config['SECRET_KEY'] = os.urandom(24)  # セッションのセキュリティキー
app.config['SECRET_KEY'] = "dis@$439if0ekwfkoN/:kefllwflYTJlefefEF"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

import re


def contains_hiragana_or_non_numeric(input_string):
    # ひらがなまたは数字以外を含む正規表現パターン
    pattern = re.compile(r'^[ぁ-ゖ0-9]+$')

    # 文字列内でパターンに一致するかを確認
    match = pattern.search(input_string)

    return match is not None


@app.route('/get_random_sentence')
def get_random_sentence():
    words = []
    moto_words = []
    min = 3
    max = 15
    kks = pykakasi.kakasi()
    while not len(words) >= 1000:
        import pickle

        mondai_path = "./templates/mondai_new.pic"
        f = open(mondai_path, "rb")
        mondais = pickle.load(f)
        f.close()
        r = random.randint(0, len(mondais[0]))
        words.append(mondais[0][r])
        moto_words.append(mondais[1][r])
    return jsonify(words, moto_words)
    # return jsonify(words)


@app.route('/typing', methods=["GET"])
def typing_mode():
    return render_template("typing_mode.html")


@app.route('/typing/<path:path>', methods=["GET"])
def typing(path):
    if path == "default":
        return render_template("typing.html", css="typing.css")
    elif path == "small":
        return render_template("typing.html", css="small-typing.css")
    elif path == "default2":
        return render_template("typing.html", css="typing2.css")
    else:
        return render_template("typing_mode.html")


@app.route("/")
def index():
    return render_template("ind.html")


if __name__ == '__main__':
    with app.app_context():  # アプリケーションコンテキスト内でデータベースを作成
        db.create_all()
    app.run(host="0.0.0.0",
            port=80,
            threaded=True)
