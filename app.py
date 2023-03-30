"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db, User, Post, Tag, PostTag

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
    tags = Tag.query.all()
    return render_template("users.html", users=users, tags = tags)


@app.route("/<userid>")
def show_details(userid):
    """Show user details and user posts."""

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
    tags = Tag.query.all()
    return render_template("newpost.html", user=user, tags = tags)

@app.route("/user/<userid>/posts/new", methods = ["POST"])
def add_new_post(userid):
    title = request.form['title']
    content = request.form['content']
    tags = request.form.getlist('tag')

    if not (title or content):
        user = user = User.query.get(userid)
        return render_template("newpost.html", user= user, error = "Please fill out both fields")
        
    db.session.add(Post(title = title, content = content, user_id=userid))
    db.session.commit()
    post = Post.query.filter_by(title = title, content = content).one()
    for tag in tags:
        tagobj = Tag.query.filter_by(tag_name = f"{tag}").one()
        posttag = PostTag(post_id = post.id, tag_id = tagobj.id)
        db.session.add(posttag)
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


@app.route("/posts/<postid>/edit", methods = ["GET"])
def show_post_edit(postid):
    post = Post.query.filter_by(id = postid).one()
    return render_template ("editpost.html", post=post)
                          


@app.route("/posts/<postid>/edit", methods = ["POST"])
def edit_post(postid):
    post = Post.query.filter_by(id = postid).one()
    post.title = request.form['title']
    post.content = request.form['content']
    db.session.add(post)
    db.session.commit()
    return redirect (f"/posts/{post.id}")



@app.route("/tags/new")
def show_tag_form():
    return render_template("createtag.html")

@app.route("/tags/new", methods = ["POST"])
def create_tag():
    name = request.form['name']
    db.session.add(Tag(tag_name= name))
    db.session.commit()
    return redirect ("/")


@app.route("/tags/<tagid>")
def show_tag_details(tagid):
    tag = Tag.query.filter_by(id=tagid).one()
    posts = tag.posts
    print (posts)
    return render_template("showtag.html", posts = posts, tag=tag)


