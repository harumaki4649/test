import random

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

# Random list of sentences (Please add sentences as needed)


@app.route('/get_random_sentence')
def get_random_sentence():
    words = []
    min = 3
    max = 15
    while not len(words) >= 1000:
        # r = requests.get("https://random-word-api.herokuapp.com/word?number=1000")
        # r = requests.get(f"https://random-word.ryanrk.com/api/jp/word/random?minlength={min}&maxlength={max}")
        # r = requests.get("https://random-word-api.vercel.app/api?words=100")
        r = requests.get("https://tango-gacha.com/API/")
        for tmp in r.json()["words"]:
            if min <= len(tmp) <= max:
                words.append(tmp)
                print(tmp, len(words))
    return jsonify(words)


@app.route('/typing', methods=["GET"])
def typing():
    return render_template("typing.html")


if __name__ == '__main__':
    with app.app_context():  # アプリケーションコンテキスト内でデータベースを作成
        db.create_all()
    app.run(host="0.0.0.0",
            port=80,
            threaded=True)
