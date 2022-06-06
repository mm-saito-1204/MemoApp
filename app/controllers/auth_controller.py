from flask import Blueprint
from flask import render_template, request, redirect
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, app
from app.models.database import User, Memo

mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

#ログインマネージャー生成
login_manager = LoginManager()
login_manager.init_app(app)

#最新時点のユーザ情報を読み取る（必須）
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#トップ画面
@mod_auth.route("/", methods=["GET", "POST"])
@login_required  #ログインしているユーザ以外のアクセスを制限する
def index():
    if request.method == "GET":
        memos = Memo.query.all()
    return render_template("index.html", memos = memos)

#ユーザ登録画面
@mod_auth.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == "POST":  #POST
        addName = request.form.get("username")
        addPass = request.form.get("password")

        nameExists = User.query.filter_by(username=addName).first()
        if nameExists is None:
            #データベースインスタンスの生成及びデータの挿入
            user = User(username = addName, password = generate_password_hash(addPass, method="sha256"))  #パスワードをsha256でハッシュ化しuserへ挿入
            db.session.add(user)
            db.session.commit()
            return redirect("/auth/login")
        else:
            return redirect("/auth/signup")
    else:  #GET
        return render_template("signup.html")

#ログイン画面
@mod_auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        #userテーブルからusername列がusername変数の値と同じ行を抽出する(１つだけ)
        user = User.query.filter_by(username=username).first()
        if user is None:
            print("IDが間違っています")
            return redirect("/auth/login")
        else:
            checkResult = check_password_hash(user.password, password)
            if checkResult:
                login_user(user)
                return redirect("/auth/")
    else:
        return render_template("/login.html")

#ログアウト
@mod_auth.route("/logout")
@login_required  #ログインしているユーザ以外のアクセスを制限する
def out():
    logout_user()
    return redirect("/auth/login")

# flaskの起動         -> flask run
# 
# flaskの終了         -> Ctrl + C
# 
# flaskの環境変数の変更 -> export FLASK_APP=実行ファイル名
# 
# Debug modeの変更    -> export FLASK_ENV=development   (ONにしておくと、ファイル保存時に自動でflaskへ反映してくれる)
#
# データベース(テーブル)初期作成時コマンド  -> from 実行ファイル名 import db  (dbはSQLAlchemyのインスタンス名)
#                                        db.create_all()
#
# SQLite 拡張機能起動方法   -> command + shift + p -> SQLite: Open Database