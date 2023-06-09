from unittest import TestCase
from app import app
from flask import session
from models import db, User, Post
from flask_sqlalchemy import SQLAlchemy


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

with app.app_context():
   db.drop_all()
   db.create_all()



class Blogytests(TestCase):
    """ Add test users (user1 and user2) to db"""


    def setUp(self):


      with app.app_context():
        
        
  
        db.session.add(User(first_name="Thorsten", last_name= "Test"))
        db.session.add(User(first_name="Dominic", last_name= "Doctest"))
        user1 = User.query.filter_by(first_name="Thorsten").one()
        db.session.add(Post(title="Amazing Test", content="This test should work!", user_id=user1.id))
        db.session.commit()  
    
                 
    def tearDown(self):
      """Delete user1 and user2 from db"""

      with app.app_context():

        user1 = User.query.filter_by(first_name='Thorsten', last_name="Test").first()
        user2 = User.query.filter_by(first_name='Dominic', last_name="Doctest").first()
        post = Post.query.filter_by(title = "Amazing Test").one()

        print(post.user_id, user1.id)
        
        
        db.session.delete(post)
        db.session.commit()
        db.session.delete(user1)
        db.session.delete(user2)
        db.session.commit()



    
    def test_show_users(self):
         
         """Test "/" view function """
         with app.test_client() as client:
            res = client.get('/')
            self.assertIn("Thorsten Test </a></li>", str(res.data))
            self.assertIn("Dominic Doctest </a></li>", str(res.data))

    def test_show_add(self):
       
       """Test view function to show add form"""
       with app.test_client() as client:
            res = client.get('/add')
            self.assertIn('<p>first_name: <input name="first_name"></p>', str(res.data))
            self.assertEqual(200, res.status_code)

       


    def test_redirection_user_add(self):
        with app.test_client() as client:
            resp = client.post("/newuser", data = {"first_name":"Testi", "last_name": "testi2", "image_url": "www.google.de"})

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/")

    def test_delete(self):
       
          with app.test_client() as client:
            client.post("/newuser", data = {"first_name":"Testi", "last_name": "testi2", "image_url": "www.google.de"})
            resp2 = client.post("/user/3/delete")
            self.assertEqual(resp2.status_code, 405)


    def test_user_details(self):
       print("this is test 5")
       with app.app_context():
          user = User.query.filter_by(first_name='Thorsten', last_name="Test").first()
       
       with app.test_client() as client:
            res = client.get(f"/{user.id}")
            self.assertIn("Amazing Test", str(res.data))
            self.assertIn(" <h1>Thorsten Test</h1>", str(res.data))
        

    def test_post_redirect(self):
       with app.app_context():
            user = User.query.filter_by(first_name='Thorsten', last_name="Test").first()

       with app.test_client() as client:
            resp = client.post(f"/user/{user.id}/posts/new", data = {"title":"Testpost", "content": "This is a test post"})

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, f"/{user.id}")
            
       with app.app_context():
            post = Post.query.filter_by(title = "Testpost").first()
            db.session.delete(post)
            db.session.commit()

          
    
          

              