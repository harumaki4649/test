import imapclient
from backports import ssl
from OpenSSL import SSL
import pyzmail
import pandas as pd
from email import utils


def get_mail(mailaddress):
    pd.options.display.max_columns = None
    pd.options.display.max_rows = None

    """ (要編集) 引数指定 """
    # ログイン情報
    my_mail = "progamerharumaki@gmail.com"
    app_password = "yepujhhfmrvepvkk"

    # SSL暗号化
    context = ssl.SSLContext(SSL.TLSv1_2_METHOD)

    # IMAP接続用のオブジェクト作成
    imap = imapclient.IMAPClient("imap.gmail.com", ssl=True, ssl_context=context)

    # IMAPサーバーログイン
    imap.login(my_mail, app_password)

    # メールフォルダを指定
    imap.select_folder("INBOX", readonly=True)

    # ① 検索キーワードを設定 & 検索キーワードに紐づくメールID検索
    KWD = imap.search(["TO", mailaddress])

    # ② メールID→メール本文取得
    raw_message = imap.fetch(KWD, ["BODY[]", "INTERNALDATE"])  # 受信日を追加

    # 解析メールの結果保存用
    From_list = []
    Cc_list = []
    Bcc_list = []
    Subject_list = []
    Body_list = []
    Body_html_list = []  # HTML本文を保存するリストを追加
    Date_list = []  # 受信日を保存するリストを追加

    # 検索結果保存
    for j in range(len(KWD)):
        # 特定メール取得
        message = pyzmail.PyzMessage.factory(raw_message[KWD[j]][b"BODY[]"])

        # 宛先取得
        From = message.get_addresses("from")
        From_list.append(From)

        Cc = message.get_addresses("cc")
        Cc_list.append(Cc)

        Bcc = message.get_addresses("bcc")
        Bcc_list.append(Bcc)

        # 件名取得
        Subject = message.get_subject()
        Subject_list.append(Subject)

        # テキスト本文
        if not message.text_part is None:
            Body = message.text_part.get_payload().decode(message.text_part.charset)
            Body_list.append(Body)
        else:
            Body_list.append("")

        # HTML本文
        html_part = message.html_part
        if html_part:
            Body_html = html_part.get_payload().decode(html_part.charset)
        else:
            Body_html = ""
        Body_html_list.append(Body_html)

        # 受信日を取得
        from datetime import datetime, timezone, timedelta
        internal_date = raw_message[KWD[j]][b"INTERNALDATE"]
        utc_time = internal_date
        jst_timezone = timezone(timedelta(hours=+9))  # 日本時間のタイムゾーン
        jst_time = utc_time.astimezone(jst_timezone)
        formatted_date = jst_time.strftime("%Y-%m-%d %H:%M:%S")
        Date_list.append(formatted_date)

    return From_list, Subject_list, Date_list, Body_list, Body_html_list


# check = get_mail("apitest@nanaharu.net")
# print(check)
