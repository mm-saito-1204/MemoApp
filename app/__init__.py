from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
#データベース生成（連携）
db = SQLAlchemy(app)

# Sample HTTP error handling
# @app.errorhandler(404)
# def not_found(error):
#     return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
from app.controllers.auth_controller import mod_auth
from app.controllers.memo_controller import mod_memo

# Register blueprint(s) ブループリントの設定
app.register_blueprint(mod_auth)
app.register_blueprint(mod_memo)

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()

#ブートストラップ生成
bootstrap = Bootstrap(app)