from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import hashlib
import datetime

# 自身の名称を app という名前でインスタンス化する
app = Flask(__name__)

# ここからウェブアプリケーション用のルーティングを記述
# index にアクセスしたときの処理
@app.route('/')
def index():
    title = "nsd ver0.0.1"
    message = "予言したい文字列を入力してください"
    # index.html をレンダリングする
    return render_template('index.html', message=message, title=title)

# /post にアクセスしたときの処理
@app.route('/post', methods=['GET', 'POST'])
def post():
    title = "実行結果"
    if request.method == 'POST':
        # リクエストフォームから「ハッシュ化したい文字列」を取得して
        name = request.form['name']
        if name == "":
            # 空っぽだった時用
            return render_template('index.html', name="error: 空白です", title=title)
        # 日付取得
        now = datetime.datetime.now().isoformat()
        # ハッシュ化
        m = hashlib.sha256()
        m.update(name.encode("utf-8"))
        # index.html をレンダリングする
        return render_template('index.html', name=m.hexdigest() + "\n timefrom:" +now, title=title)
    else:
        # エラーなどでリダイレクトしたい場合はこんな感じで
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.debug = True # デバッグモード有効化
    app.run(host='0.0.0.0') # どこからでもアクセス可能に