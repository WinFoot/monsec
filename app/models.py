# -*- coding:utf-8 -*- 
from app import db

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')
    
    def __repr__(self):
        return '<User %r>' % (self.nickname)    
        
class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)

# 安全月报类
class Sheet(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    level = db.Column(db.Integer) # 风险指数
    name = db.Column(db.String(140))  # 月报名称 2016-01
    timestamp = db.Column(db.DateTime) # 创建时间
    vuls = db.relationship('Vul', backref = 'sheet', lazy = 'dynamic')
    eves = db.relationship('Eve', backref = 'sheet', lazy = 'dynamic')
    
    def __repr__(self):
        return '<Sheet %r>' % (self.name)    

# 安全漏洞类
class Vul(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    level = db.Column(db.String(140))  # 漏洞等级
    type = db.Column(db.String(140))   # 漏洞类型
    name = db.Column(db.String(140))   # 漏洞名称
    time = db.Column(db.String(140)) # 发生时间
    timestamp = db.Column(db.DateTime) # 创建时间
    sheet_id = db.Column(db.Integer, db.ForeignKey('sheet.id'))

    def __repr__(self):
        return '<Vul %r>' % (self.name)

# 安全事件类
class Eve(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    level = db.Column(db.String(140)) # 事件等级
    type = db.Column(db.String(140)) # 事件类型
    name = db.Column(db.String(140)) # 事件名称
    time = db.Column(db.String(140)) # 发生时间
    timestamp = db.Column(db.DateTime) # 创建时间
    sheet_id = db.Column(db.Integer, db.ForeignKey('sheet.id'))

    def __repr__(self):
        return '<Eve %r>' % (self.name)

