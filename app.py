"""Blogly application."""

from flask import Flask, render_template
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


connect_db(app)

with app.app_context():
    db.create_all()


# with app.app_context():
#     user1 = User(first_name="Thorsten", last_name= "Test")
#     user2 = User(first_name="Dominic", last_name= "Doctest")
#     db.session.add(user1)
#     db.session.add(user2)
#     db.session.commit()    

@app.route("/")
def list_users():
    """List users and show add form."""

    users = User.query.all()
    return render_template("users.html", users=users)


@app.route("/<userid>")
def show_details(userid):
    """List users and show add form."""

    user = User.query.get_or_404(userid)
    return render_template("details.html", user=user)


@app.route("/add")
def show_add_form():
    """ render User Add form"""
    return render_template("add.html")