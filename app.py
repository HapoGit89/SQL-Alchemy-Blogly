"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


connect_db(app)

with app.app_context():
    db.create_all()


@app.route("/")
def list_users():
    """List users and show add form."""

    users = User.query.all()
    return render_template("users.html", users=users)


@app.route("/<userid>")
def show_details(userid):
    """List users and show add form."""

    user = User.query.get_or_404(userid)
    posts= Post.query.filter_by(user_id = userid).all()
    return render_template("details.html", user=user, posts=posts)


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

    if not (url):
        user = User(first_name = first_name, last_name=last_name)
    else:
        user = User(first_name = first_name, last_name=last_name, image_url=url)
    db.session.add(user)
    db.session.commit()
    return redirect ("/")

@app.route("/user/<userid>/delete", methods=["GET"])
def delete_user(userid):
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


@app.route("/user/<userid>/posts/new", methods = ["GET"])
def show_post_form(userid):
    user = user = User.query.get(userid)
    return render_template("newpost.html", user=user)

@app.route("/user/<userid>/posts/new", methods = ["POST"])
def add_new_post(userid):
    title = request.form['title']
    content = request.form['content']
    if not (title or content):
        user = user = User.query.get(userid)
        return render_template("newpost.html", user= user, error = "Please fill out both fields")
        
    db.session.add(Post(title = title, content = content, user_id=userid))
    db.session.commit()
    return redirect(f"/{userid}")


@app.route("/posts/<postid>")
def show_post(postid):
    post = Post.query.filter_by(id = postid).one()
    user = User.query.filter_by(id=post.user_id).one()
    return render_template("postdetails.html", user = user, post = post) 

@app.route("/posts/<postid>/delete")
def delete_post(postid):
    post = Post.query.filter_by(id = postid).one()
    user = User.query.filter_by(id=post.user_id).one()
    db.session.delete(post)
    db.session.commit()
    return redirect(f"/{user.id}")
                          








