"""Blogly application."""

from flask import Flask, render_template, request, redirect
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


@app.route("/newuser", methods = ["POST"])
def add_user():
    """Adds user to database and redirects to User List"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    url = request.form['image_url']

    user = User(first_name = first_name, last_name=last_name, image_url=url)
    db.session.add(user)
    db.session.commit()
    return redirect ("/")

@app.route("/user/<userid>/delete")
def delete_user(userid):
    print(f"this is before the request, user is is {userid}")
    user = User.query.get(userid)
    db.session.delete(user)
    db.session.commit()
    return redirect ('/')


@app.route("/user/<userid>/edit", methods = ["GET"])
def edit_user_page(userid):
    user = user = User.query.get(userid)
    return render_template("edit.html", user=user)


@app.route("/user/<userid>/edit", methods = ["POST"])
def edit_user(userid):
    user = user = User.query.get(userid)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']
    db.session.add(user)
    db.session.commit()
    return redirect (f"/{userid}")







