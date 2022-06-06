from app import db
from datetime import datetime
from flask_login import UserMixin
import pytz

#ユーザテーブルUser(SQLAlchemy利用)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(12))

#記事テーブルMemo(SQLAlchemy利用)
class Memo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    body = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                default=datetime.now(pytz.timezone("Asia/Tokyo")))