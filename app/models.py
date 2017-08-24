# coding: utf8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@127.0.0.1:3306/movie"
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
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # sign in time
    uuid = db.Column(db.String(255), unique=True)  # unique key
    userlogs = db.relationship('Userlog', backref='user')  # foreign key user log
    comments = db.relationship('Comment', backref='user')  # foreign key comment
    moviecols = db.relationship('Moviecol', backref='user')  # foreign key movie collection

    def __repr__(self):
        return "<User %r>" % self.name


# 会员登录日志
class Userlog(db.Model):
    __tablename__ = "userlog"
    id = db.Column(db.Integer, primary_key=True)  # id
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属会员
    ip = db.Column(db.String(100))  # 登录IP
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 登录时间

    def __repr__(self):
        return "<Userlog %r>" % self.id


# tag
class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)  # id
    name = db.Column(db.String(100), unique=True)  # name
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # add time
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
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))  # belongs to which tag
    area = db.Column(db.String(255))  # release area
    release_time = db.Column(db.Date)  # release time
    length = db.Column(db.String(100))  # play time
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # add time
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
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # add time

    def __repr__(self):
        return "<Preview %r>" % self.title


# comments
class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)  # id
    content = db.Column(db.Text)  # comment content
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # which movie
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # which user
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # add time

    def __repr__(self):
        return "<Comment %r>" % self.title


# movie collection
class Moviecol(db.Model):
    __tablename__ = "moviecol"
    id = db.Column(db.Integer, primary_key=True)  # id
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # which movie
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # which user
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # add time

    def __repr__(self):
        return "<Moviecol %r>" % self.id


# authentications
class Auth(db.Model):
    __tablename__ = "auth"
    id = db.Column(db.Integer, primary_key=True)  # id
    name = db.Column(db.String(100), unique=True)  # title
    url = db.Column(db.String(255), unique=True)  # urls for accession
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # add time

    def __repr__(self):
        return "<Auth %r>" % self.name


# roles
class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)  # id
    name = db.Column(db.String(100), unique=True)  # title
    auths = db.Column(db.String(600))  #
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # add time
    admins = db.relationship("Admin", backref='role')  # 管理员外键关系关联

    def __repr__(self):
        return "<Auth %r>" % self.name


# administrator
class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)  # id
    name = db.Column(db.String(100), unique=True)  # admin name
    pwd = db.Column(db.String(100))  # password
    is_super = db.Column(db.SmallInteger)  # suepr admin or not, 0 specify super admin
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))  # which role
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # add time
    adminlogs = db.relationship("Adminlog", backref='admin')  # log fk relationship
    oplogs = db.relationship("Oplog", backref='admin')  # operation log fk relationship

    def __repr__(self):
        return "<Admin %r>" % self.name


# admin login log
class Adminlog(db.Model):
    __tablename__ = "adminlog"
    id = db.Column(db.Integer, primary_key=True)  # id
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(100))  # 登录IP
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 登录时间

    def __repr__(self):
        return "<Adminlog %r>" % self.id


# operation log
class Oplog(db.Model):
    __tablename__ = "oplog"
    id = db.Column(db.Integer, primary_key=True)  # id
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(100))  # 登录IP
    reason = db.Column(db.String(600))  # operation reason
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 登录时间

    def __repr__(self):
        return "<Oplog %r>" % self.id


if __name__ == "__main__":
    db.create_all()
    # role = Role(
    #     name="超级管理员",
    #     auths=""
    # )
    #
    # from werkzeug.security import generate_password_hash
    #
    # admin = Admin(
    #     name="litacheng",
    #     pwd=generate_password_hash("zhengli"),
    #     is_super=0,
    #     role_id=1
    # )
    # db.session.add(admin)
    # db.session.commit()
