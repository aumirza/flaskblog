from . import  db , login_m as login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin , current_user
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id =db.Column(db.Integer(),primary_key=True)
    email =db.Column(db.String(120),nullable=False)
    username =db.Column(db.String(20),nullable=False)
    password =db.Column(db.String(20),nullable=False)
    posts = db.relationship('Post', backref='author',lazy=True)

    def __init__(self,email,username,password):
        self.email=email
        self.username=username
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password , password)


    def __repr__(self):
        return f"{self.id}{self.username}"


class Post(db.Model):
    __tablename__ = "posts"
    id =db.Column(db.Integer(),primary_key=True)
    title =db.Column(db.String(255),nullable=False)
    slug =db.Column(db.String(255),nullable=False)
    content =db.Column(db.Text(2200),nullable=False)
    created_on =db.Column(db.DateTime(),default=datetime.now)
    updated_on =db.Column(db.DateTime(),default=datetime.now,onupdate=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    catogary_id = db.Column(db.Integer, db.ForeignKey('catogaries.id'))


    def __init__(self,title,slug,content,catogary):
        self.title=title
        self.slug = slug
        self.content = content
        self.author = current_user
        self.catogary = catogary

    def __repr__(self):
        return f"{self.id}{self.title[0:10]}"


class Catogary(db.Model):
    __tablename__ = "catogaries"
    id =db.Column(db.Integer(),primary_key=True)
    name =db.Column(db.String(255),nullable=False)
    slug =db.Column(db.String(255),nullable=False)
    created_on =db.Column(db.DateTime(),default=datetime.now)
    posts = db.relationship('Post', backref='catogary')

    def __repr__(self):
        return f"{self.id}{self.name}"

    def __init__(self,name,slug):
        self.name =name 
        self.slug = slug

