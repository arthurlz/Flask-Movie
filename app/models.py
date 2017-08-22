# coding: utf8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:zhengli23@127.0.0.1:8889/movie"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)


# 会员
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)  # id
    name = db.Column(db.String(100), unique=True)  # nickname
    pwd = db.Column(db.String(100))  # password
    email = db.Column(db.String(100), unique=True)  # email
    phone = db.Column(db.String(11), unique=True)  # phone number
    info = db.Column(db.Text)  # profile
    face = db.Column(db.String(255), unique=True)  # avatar
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # sign in time
    uuid = db.Column(db.String(255), unique=True)  # unique key
    userlogs = db.relationship('Userlog', backref='user') #foreign key user log

    def __repr__(self):
        return "<User %r>" % self.nae

#会员登录日志
class Userlog(db.Model):
    __tablename__ = "userlog"
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # 所属会员
    ip = db.Column(db.String(100)) # 登录IP
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow) # 登录时间

    def __repr__(self):
        return "<Userlog %r>" % self.id