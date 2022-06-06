from flask import Blueprint
from flask import render_template, request, redirect
from flask_login import login_required
from app.models.database import Memo
from app import db

mod_memo = Blueprint('memo', __name__, url_prefix='/memo')

#記事投稿画面
@mod_memo.route("/create", methods=['GET', 'POST'])
@login_required  #ログインしているユーザ以外のアクセスを制限する
def create():
    if request.method == "POST":
        title = request.form.get("title")
        body = request.form.get("body")

        #データベースインスタンスの生成及びデータの挿入
        memo = Memo(title = title, body = body)
        db.session.add(memo)
        db.session.commit()
        return redirect("/auth/")
    else:
        return render_template("create.html")

#記事更新画面
@mod_memo.route("/<int:id>/update", methods=['GET', 'POST'])
@login_required  #ログインしているユーザ以外のアクセスを制限する
def update(id):
    memo = Memo.query.get(id)
    if request.method == "GET":
        return render_template("update.html", memo = memo)
    else:
        #データベース(Memo)へのデータの更新
        memo.title = request.form.get("title")
        memo.body = request.form.get("body")
        db.session.commit()
        return redirect("/auth/")

#記事削除
@mod_memo.route("/<int:id>/delete", methods=['GET'])
@login_required  #ログインしているユーザ以外のアクセスを制限する
def delete(id):
    memo = Memo.query.get(id)
    db.session.delete(memo)
    db.session.commit()
    return redirect("/auth/")

