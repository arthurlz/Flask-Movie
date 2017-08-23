# coding: utf8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@127.0.0.1:8889/movie"
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
    userlogs = db.relationship('Userlog', backref='user')  # foreign key user log
    comments = db.relationship('Comment', backref='user')  # foreign key comment
    moviecols = db.relationship('Moviecol', backref='user')  # foreign key movie collection

    def __repr__(self):
        return "<User %r>" % self.name


# 会员登录日志
class Userlog(db.Model):
    __tablename__ = "userlog"
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属会员
    ip = db.Column(db.String(100))  # 登录IP
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 登录时间

    def __repr__(self):
        return "<Userlog %r>" % self.id


# tag
class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)  # id
    name = db.Column(db.String(100), unique=True)  # name
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # add time
    movies = db.relationship("Movie", backref="tag")  # movie foreign key

    def __repr__(self):
        return "<Tag %r>" % self.name


# movie
class Movie(db.Model):
    __tablename__ = "movie"
    id = db.Column(db.Integer, primary_key=True)  # id
    title = db.Column(db.String(255), unique=True)  # title
    url = db.Column(db.String(255), unique=True)  # url
    info = db.Column(db.String(255), unique=True)  # infomation
    logo = db.Column(db.String(255), unique=True)  # cover
    star = db.Column(db.SmallInteger)  # start class
    playnum = db.Column(db.BigInteger)  # clicks
    commentnum = db.Column(db.BigInteger)  # comment number
    tag_id = db.Column(db.Integer, db.ForeignKey('tag_id'))  # belongs to which tag
    area = db.Column(db.String(255))  # release area
    release_time = db.Column(db.Date)  # release time
    length = db.Column(db.String(100))  # play time
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # add time
    comments = db.relationship("Comment", backref="movie")  # comment foreign key
    moviecols = db.relationship("Moviecol", backref="movie")  # movie collection foreign key

    def __repr__(self):
        return "<Movie %r>" % self.title


# before release promotion
class Preview(db.Model):
    __tablename__ = "preview"
    id = db.Column(db.Integer, primary_key=True)  # id
    title = db.Column(db.String(255), unique=True)  # title
    logo = db.Column(db.String(255), unique=True)  # cover
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # add time

    def __repr__(self):
        return "<Preview %r>" % self.title


# comments
class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)  # id
    content = db.Column(db.Text)  # comment content
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id')) # which movie
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # which user
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # add time

    def __repr__(self):
        return "<Comment %r>" % self.title

# movie collection
class Moviecol(db.Model):
    __tablename__ = "moviecol"
    id = db.Column(db.Integer, primary_key=True)  # id
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # which movie
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # which user
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # add time

    def __repr__(self):
        return "<Moviecol %r>" % self.id