from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import hashlib
import datetime

from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# 自身の名称を app という名前でインスタンス化する
app = Flask(__name__)

engine = create_engine('sqlite:///myyogens', echo=True)
Base = declarative_base()
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

class Yogen(Base):
    __tablename__ = 'yogens'
    id = Column(Integer, primary_key=True)
    time = Column(String)
    hash256 = Column(String)
    def __repr__(self):
        return "<User(time='%s', hash256='%s')>" % (self.time, self.hash256)

# ここからウェブアプリケーション用のルーティングを記述
# index にアクセスしたときの処理
@app.route('/')
def index():
    title = "nsd ver0.0.1"
    message = 'ようこそ'
    return render_template('index.html', message=message, title=title)


@app.route('/yogen')
def yogen():
    title = "nsd ver0.0.1"
    message = '予言したい文字列を入力してください'
    # index.html をレンダリングする
    return render_template('yogen.html', message=message, title=title)

# /post にアクセスしたときの処理
@app.route('/yogen/post', methods=['GET', 'POST'])
def yogen_post():
    title = '実行結果'
    if request.method == 'POST':
        # リクエストフォームから「ハッシュ化したい文字列」を取得して
        name = request.form['name']
        if name == "":
            # 空っぽだった時用
            return render_template('yogen.html', name='error: 空白です', title=title)
        # 日付取得
        now = datetime.datetime.now().isoformat()
        # ハッシュ化
        m = hashlib.sha256()
        m.update(name.encode("utf-8"))
        yogen = Yogen(hash256=m.hexdigest(), time=now)
        session.add(yogen)
        session.commit()
        # index.html をレンダリングする
        return render_template('index.html', name=m.hexdigest() + '\n timefrom:' +now, title=title)
    else:
        # エラーなどでリダイレクトしたい場合はこんな感じで
        return redirect(url_for('index'))

@app.route('/rev')
def rev():
    title = "nsd ver0.0.1"
    message = '作成時間を調べたいハッシュを入力してください'
    # index.html をレンダリングする
    return render_template('rev.html', message=message, title=title)

# /post にアクセスしたときの処理
@app.route('/rev/post', methods=['GET', 'POST'])
def rev_post():
    title = '実行結果'
    name = request.form['name']
    if request.method == 'POST':
        searched_yogen = session.query(Yogen).filter_by(hash256=name).first()
        # index.html をレンダリングする
        return render_template('rev.html', name=searched_yogen.hash256 + '\n timefrom:' +searched_yogen.time, title=title)
    else:
        # エラーなどでリダイレクトしたい場合はこんな感じで
        return redirect(url_for('rev'))

if __name__ == '__main__':
    app.debug = True # デバッグモード有効化
    app.run(host='0.0.0.0') # どこからでもアクセス可能に