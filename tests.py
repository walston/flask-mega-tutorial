from app.models import User, Post
from app import app, db
import unittest
from datetime import datetime, timezone, timedelta
import os
os.environ['DATABASE_URL'] = 'sqlite://'


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='susan', email='susan@example.com')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))

    def test_follow(self):
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        following = db.session.scalars(u1.following.select()).all()
        followers = db.session.scalars(u1.followers.select()).all()
        self.assertEqual(following, [])
        self.assertEqual(followers, [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.following_count(), 1)
        self.assertEqual(u2.followers_count(), 1)
        u1_following = db.session.scalars(u1.following.select()).all()
        u2_followers = db.session.scalars(u2.followers.select()).all()
        self.assertEqual(u1_following[0].username, 'susan')
        self.assertEqual(u2_followers[0].username, 'john')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.following_count(), 0)
        self.assertEqual(u2.followers_count(), 0)

    def test_follow_posts(self):
        # create four users
        john = User(username='john', email='john@example.com')
        susy = User(username='susan', email='susan@example.com')
        mary = User(username='mary', email='mary@example.com')
        dave = User(username='david', email='david@example.com')

        # create four posts
        now = datetime.now(timezone.utc)
        p1 = Post(body="post from john", author=john,
                  timestamp=now + timedelta(seconds=1))
        p2 = Post(body="post from susan", author=susy,
                  timestamp=now + timedelta(seconds=4))
        p3 = Post(body="post from mary", author=mary,
                  timestamp=now + timedelta(seconds=3))
        p4 = Post(body="post from david", author=dave,
                  timestamp=now + timedelta(seconds=2))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        # setup the followers
        john.follow(susy)
        john.follow(dave)
        susy.follow(mary)
        mary.follow(dave)
        db.session.commit()

        # check the following posts of each user
        feed1 = db.session.scalars(john.following_posts()).all()
        feed2 = db.session.scalars(susy.following_posts()).all()
        feed3 = db.session.scalars(mary.following_posts()).all()
        feed4 = db.session.scalars(dave.following_posts()).all()
        self.assertEqual(feed1, [p2, p4, p1])
        self.assertEqual(feed2, [p2, p3])
        self.assertEqual(feed3, [p3, p4])
        self.assertEqual(feed4, [p4])


if __name__ == '__main__':
    unittest.main(verbosity=2)
