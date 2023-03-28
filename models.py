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

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    first_name = db.Column(db.String(20),
                          nullable = False)
    last_name = db.Column(db.String(20),
                          nullable = False)
    image_url = db.Column(db.Text,
                          nullable = True)
    

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

