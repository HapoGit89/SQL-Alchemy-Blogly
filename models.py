"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import time

db = SQLAlchemy()

def connect_db(app):
    """Connect to database"""

    db.app = app
    db.init_app(app)


class User (db.Model):
    """ User """

    __tablename__ = "users"

    def __repr__(self):
        """Show User Info"""
        p = self
        return f"User {p.id}, {p.first_name} {p.last_name}"


    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    first_name = db.Column(db.String(20),
                          nullable = False)
    last_name = db.Column(db.String(20),
                          nullable = False)
    image_url = db.Column(db.Text,      
                          default = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460__340.png")
    
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")
    

class Post (db.Model):
    """Post"""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    title = db.Column(db.String(30),
                      nullable = False)
    content = db.Column(db.Text,
                        nullable = False)
    created_at = db.Column(db.DateTime,
                           default = datetime.fromtimestamp(time.time()) )
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'))
    

    posttags = db.relationship('PostTag', backref = 'posts', cascade="all, delete-orphan")

    tag = db.relationship('Tag', secondary = 'posttags', backref ='posts')

class Tag(db.Model):
    """Tag"""

    def __repr__(self):
        """Show User Info"""
        p = self
        return f"Tag {p.id}, name : {p.name}"

    __tablename__ = "tags"

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    tag_name = db.Column(db.String(20),
                     nullable = False,
                    unique = True)
    
    taggedposts = db.relationship('PostTag', backref = 'tags', cascade="all, delete-orphan")

    postings = db.relationship('Post', secondary = 'posttags', backref = 'tags')
    


class PostTag(db.Model):
    """Post and Tags M2M"""

    __tablename__ = "posttags"

    post_id = db.Column(db.Integer,
               db.ForeignKey('posts.id'),
               primary_key= True)
    tag_id = db.Column(db.Integer,
               db.ForeignKey('tags.id'),
               primary_key= True)



