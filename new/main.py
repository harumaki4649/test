import re
import random
import pykakasi
import pickle
import requests
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import gmail_check_api
# pip install Flask-SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask

app = Flask(__name__, static_folder="./static")
# app.config['SECRET_KEY'] = os.urandom(24)  # セッションのセキュリティキー
app.config['SECRET_KEY'] = "dis@$439if0ekwfkoN/:kefllwflYTJlefefEF"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    ip_addres = db.Column(db.String(100), nullable=False)


reset = False
if reset:
    with app.app_context():
        db.drop_all()  # すべてのテーブルを削除
        db.create_all()  # テーブルを再作成
        # ここで初期データの追加を行う場合は記述


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)


class User_sec_settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    sec = db.Column(db.String(60), nullable=False)


class User_settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    cloudflare_key = db.Column(db.String(20), unique=True, nullable=False)
    cloudflare_email = db.Column(db.String(20), unique=True, nullable=False)


class User_mail_addres(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    mail_addres = db.Column(db.String(20), unique=True, nullable=False)


def ip_get():
    acces_ip = str(request.headers.get('cf-connecting-ip'))
    acces_ip2 = str(request.headers.get('Cf-Pseudo-Ipv4'))
    print(acces_ip)
    print(acces_ip2)
    return acces_ip


@app.route('/', methods=["GET"])
def home():
    try:
        session_id = session['session_id']
        url = "dashboard"
        message = "ダッシュボードはこちら"
    except Exception:
        url = "login"
        message = "ログイン・登録はこちら"
        pass
    return render_template("index.html", url="https://mail.disnana.com/" + url, message=message)


@app.route('/dashboard', methods=["GET"])
def dashboard():
    try:
        session_id = session['session_id']
        tmp = Session.query.filter_by(session_id=session_id).first()
        print(tmp)
        print(tmp.username)
        tmp2 = User_sec_settings.query.filter_by(username=tmp.username).first()
        print(tmp2.sec)
        if not tmp.ip_addres == ip_get() and tmp2.sec == 1:
            session["session_id"] = "warn"
            return redirect(url_for('logout'))
    except Exception:
        url = "login"
        message = "ログイン・登録はこちら"
        flash('本人確認のため再度ログインしてください', 'danger')
        return redirect(url_for('login'))
    return render_template("dashboard.html", username=tmp.username)


@app.route('/mail', methods=["GET", "POST"])
def mail():
    return "Coming Soon..."


@app.route('/settings', methods=["GET"])
def settings():
    try:
        session_id = session['session_id']
        tmp = Session.query.filter_by(session_id=session_id).first()
        print(tmp)
        print(tmp.username)
        tmp2 = User_sec_settings.query.filter_by(username=tmp.username).first()
        print(tmp2.sec)
        if not tmp.ip_addres == ip_get() and tmp2.sec == 1:
            session["session_id"] = "warn"
            return redirect(url_for('logout'))
    except Exception:
        return redirect(url_for('login'))
    return render_template("settings.html", username=tmp.username)


@app.route('/settings/sec', methods=["GET", "POST"])
def setting_sec():
    try:
        session_id = session['session_id']
        tmp = Session.query.filter_by(session_id=session_id).first()
        print(tmp)
        print(tmp.username)
        tmp2 = User_sec_settings.query.filter_by(username=tmp.username).first()
        print(tmp2.sec)
        if not tmp.ip_addres == ip_get() and tmp2.sec == 1:
            session["session_id"] = "warn"
            return redirect(url_for('logout'))
    except Exception:
        return redirect(url_for('login'))
    if request.method == "POST":
        try:
            print("設定 ：", request.form.get('security'))
            session_id = session['session_id']
            tmp = Session.query.filter_by(session_id=session_id).first()
            tmp2 = User_sec_settings.query.filter_by(username=tmp.username).first()
            # 新しい設定を保存
            if request.form.get('security') is None:
                tmp2.sec = 0
            else:
                tmp2.sec = 1
            # 変更をコミット
            db.session.commit()
            flash('設定を変更しました', 'success')
        except Exception as e:
            flash('内部エラーが発生しました', 'warn')
            print(e)
    tmp2 = User_sec_settings.query.filter_by(username=tmp.username).first()
    return render_template("setting_sec.html", username=tmp.username, setting_1=tmp2.sec)


@app.route('/settings/pass', methods=["GET", "POST"])
def setting_pass():
    if request.method == "POST":
        username = request.form.get('username')
        pass1 = request.form.get('key')
        pass2 = request.form.get('key2')
        print(pass1, pass2, username)
        if pass1 == pass2:
            with app.app_context():
                user = User.query.filter_by(username=username).first()
                print(user)
                if user:
                    # 新しいパスワードを設定
                    user.password = pass1

                    # 変更をコミット
                    db.session.commit()
                    flash('パスワードを変更しました', 'success')
                else:
                    flash('ユーザーが見つかりませんでした', 'warn')
        else:
            flash('パスワードが違います', 'warn')
    try:
        session_id = session['session_id']
        tmp = Session.query.filter_by(session_id=session_id).first()
        print(tmp)
        print(tmp.username)
        tmp2 = User_sec_settings.query.filter_by(username=tmp.username).first()
        print(tmp2.sec)
        if not tmp.ip_addres == ip_get() and tmp2.sec == 1:
            session["session_id"] = "warn"
            return redirect(url_for('logout'))
    except Exception:
        return redirect(url_for('login'))
    return render_template("setting_password.html", username=tmp.username)


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        if len(username) > 15 or len(password) > 50:
            flash('文字数制限の解除を検知しました', 'warn')
            flash('IPは管理者に報告されました', 'warn')
            return redirect(url_for('login'))

        with app.app_context():  # アプリケーションコンテキスト内でデータベース操作
            user = User.query.filter_by(username=username).first()
            if user and password == user.password:
                # セッションIDをデータベースに保存
                session_id = os.urandom(24).hex()
                session['session_id'] = session_id
                print(session_id)

                # セッション情報をデータベースに保存
                db.session.add(Session(session_id=session_id, username=username, ip_addres=ip_get()))
                db.session.commit()
                # flash('ログイン成功', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('ログイン失敗', 'danger')
                return redirect(url_for('login'))
    else:
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        pass_check = request.form.get('pass')
        if len(username) > 15 or len(password) > 50 or len(pass_check) > 50:
            flash('文字数制限の解除を検知しました', 'warn')
            flash('IPは管理者に報告されました', 'warn')
            return redirect(url_for('register'))
        print(pass_check, password)
        if not pass_check == password:
            flash('パスワードが一致しません', 'danger')
            return redirect(url_for('register'))
        user = User.query.filter_by(username=username).first()
        if not user is None:
            if user and password == user.password:
                return redirect(url_for('dashboard'))
            flash('ユーザー名は既に使用されています', 'danger')
            return redirect(url_for('register'))

        # 新しいユーザーオブジェクトを作成してデータベースに保存
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        # 新しいユーザーのセキュリティ設定オブジェクトを作成してデータベースに保存
        new_user = User_sec_settings(username=username, sec=0)
        db.session.add(new_user)
        db.session.commit()

        # セッションIDをデータベースに保存
        session_id = os.urandom(24).hex()
        session['session_id'] = session_id
        print(session_id)

        # セッション情報をデータベースに保存
        db.session.add(Session(session_id=session_id, username=username, ip_addres=ip_get()))
        db.session.commit()
        # flash('ログイン成功', 'success')
        return redirect(url_for('dashboard'))

    return render_template('register.html')


@app.route('/logout')
def logout():
    try:
        session_id = session['session_id']
        session_record = Session.query.filter_by(session_id=session_id).first()
        if session_record:
            db.session.delete(session_record)
            db.session.commit()
        session.pop('session_id', None)  # セッションを削除
        if session_id == "warn":
            flash('不審な動作を検知したためログアウトしました', 'warn')
        else:
            flash('ログアウト成功', 'success')
    except Exception:
        session.pop('session_id', None)  # セッションを削除
        pass
    return redirect(url_for('login'))


# 注意、ここから開発段階のコード
# サンプルのメールデータ（仮定）
sample_emails = [
    {
        "id": 1,
        "subject": "メール1",
        "content": "これはメール1の内容です。",
        "sender": "送信者1",
        "date": "2023-09-01 10:00:00",
        "recipient": "recipient@example.com"
    },
    {
        "id": 2,
        "subject": "メール2",
        "content": "これはメール2の内容です。",
        "sender": "送信者2",
        "date": "2023-09-01 11:30:00",
        "recipient": "recipient@example.com"
    },
    {
        "id": 3,
        "subject": "メール3",
        "content": "これはメール3の内容です。",
        "sender": "送信者3",
        "date": "2023-09-02 09:15:00",
        "recipient": "recipient@example.com"
    },
    {
        "id": 4,
        "subject": "メール1",
        "content": "これはメール1の内容です。",
        "sender": "送信者1",
        "date": "2023-09-01 10:00:00",
        "recipient": "recipient@example.com"
    },
    {
        "id": 5,
        "subject": "メール2",
        "content": "これはメール2の内容です。",
        "sender": "送信者2",
        "date": "2023-09-01 11:30:00",
        "recipient": "recipient@example.com"
    },
    {
        "id": 6,
        "subject": "メール3",
        "content": "これはメール3の内容です。",
        "sender": "送信者3",
        "date": "2023-09-02 09:15:00",
        "recipient": "recipient@example.com"
    }
]


@app.route('/debug')
def debug():
    return render_template('mailbox.html')


@app.route('/get_emails', methods=['GET'])
def get_emails():
    try:
        session_id = session['session_id']
        tmp = Session.query.filter_by(session_id=session_id).first()
        print(tmp)
        print(tmp.username)
        tmp2 = User_sec_settings.query.filter_by(username=tmp.username).first()
        print(tmp2.sec)
        if not tmp.ip_addres == ip_get() and tmp2.sec == 1:
            session["session_id"] = "warn"
            return redirect(url_for('logout'))
    except Exception:
        return redirect(url_for('login'))

    mails = gmail_check_api.get_mail(tmp.username + "@nanaharu.net")
    sample_emails = []

    for cnt in range(len(mails[1])):
        email_data = {
            "id": cnt,
            "subject": mails[1][cnt],
            "sender": mails[0][cnt][0],
            "date": mails[2][cnt],
            "recipient": tmp.username + "@nanaharu.net"
        }

        if not mails[4][cnt] == "":  # body_htmlが存在するかチェック
            email_data["content"] = mails[3][cnt]
            email_data["body_type"] = "body_html"
            email_data["body"] = mails[4][cnt]  # bodyも追加
        else:
            email_data["content"] = mails[3][cnt]
            email_data["body_type"] = "body"
            email_data["body"] = ""  # body_htmlの場合、空文字列を追加

        sample_emails.append(email_data)

    # メールデータをJSON形式で返す
    return jsonify(sample_emails)


def huseihantei(score, heikin):
    if heikin >= 20 or score >= 10000:
        return True
    else:
        return False


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
        if session["mode"] == "false" or session["mode"] == "" or session["mode"] == None:
            mondai_path = "./templates/mondai_new.pic"
            f = open(mondai_path, "rb")
            mondais = pickle.load(f)
            f.close()
            r = random.randint(0, len(mondais[0]))
            try:
                words.append(mondais[0][r])
                moto_words.append(mondais[1][r])
            except Exception:
                pass
        else:
            # r = requests.get("https://random-word-api.herokuapp.com/word?number=1000")
            # r = requests.get(f"https://random-word.ryanrk.com/api/jp/word/random?minlength={min}&maxlength={max}")
            # r = requests.get("https://random-word-api.vercel.app/api?words=100")
            r = requests.get("https://tango-gacha.com/API/")
            for tmp in r.json()["words"]:
                try:
                    if min <= len(tmp) <= max:
                        result = kks.convert(tmp)
                        for data in ["hira"]:
                            tmp2 = ""
                            for num in range(len(result)):
                                tmp2 += result[num][data]
                        if contains_hiragana_or_non_numeric(tmp2):
                            words.append(tmp2)
                            moto_words.append(tmp)

                        print(tmp, tmp2, len(words))
                except Exception:
                    pass
    return jsonify(words, moto_words)
    # return jsonify(words)


@app.route('/typing', methods=["GET"])
def typing_mode():
    return render_template("typing_mode.html")


@app.route('/typing/<path:path>', methods=["GET"])
def typing(path):
    session["mode"] = request.args.get('mode', '')
    if path == "default":
        return render_template("typing.html", css="typing.css")
    elif path == "small":
        return render_template("typing.html", css="small-typing.css")
    elif path == "default2":
        return render_template("typing.html", css="typing2.css")
    else:
        return render_template("typing_mode.html")


@app.route("/ranking", methods=["POST"])
def ranking():
    data = request.json["data"]
    print(data)
    if len(data[0]) >= 15:
        data[0] = data[0][:15 - len(data[0])]
    pic_path = "./ranking.pic"
    husei = huseihantei(data[1], data[2])
    print(husei)
    if not husei:
        if os.path.exists(pic_path):
            f = open(pic_path, "rb")
            ranking = pickle.load(f)
            f.close()
            ranking.append(data)
        else:
            ranking = [["null", 0, 0] for _ in range(10000)]
            ranking.append(data)
        ranking = sorted(ranking, key=lambda x: float(x[1]), reverse=True)
        ranking = ranking[:-1]
        f = open(pic_path, 'wb')
        pickle.dump(ranking, f)
        f.close()
        if data in ranking:
            juni = ranking.index(data) + 1
        else:
            juni = 10001
    else:
        ranking = [["", 0, ""] for _ in range(10000)]
        juni = 10001
    ans = [juni, ranking, husei]
    print(ans)
    return jsonify(ans)


if __name__ == '__main__':
    with app.app_context():  # アプリケーションコンテキスト内でデータベースを作成
        db.create_all()
    app.run(host="0.0.0.0",
            port=80,
            threaded=True)