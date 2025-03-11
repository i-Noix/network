from django.db.models import Max
from django.test import TestCase, Client

from .models import Posts, Like, User

# Create your tests here.
class PostsTestCase(TestCase):

    def setUp(self):

        # Create users.
        self.user_1 = User.objects.create(username = 'Ron')
        self.user_2 = User.objects.create(username = 'Harry')

        # Create posts.
        self.p1 = Posts.objects.create(author = self.user_1, content = 'Hello world')
        self.p2 = Posts.objects.create(author = self.user_1, content = '       ')


    def test_valid_post(self):
        self.assertTrue(self.p1.is_valid_post())

    def test_invalid_post(self):
        self.assertFalse(self.p2.is_valid_post())

    def test_valid_following(self):
        self.user_1.following.add(self.user_2)
        self.assertTrue(self.user_1.is_valid_following())
    
    def test_invalid_following(self):
        self.assertFalse(self.user_1.following.filter(id=self.user_1.id).exists())
        self.user_1.following.add(self.user_1)
        self.assertTrue(self.user_1.following.filter(id=self.user_1.id).exists())
        self.assertFalse(self.user_1.is_valid_following())
        self.assertFalse(self.user_1.following.filter(id=self.user_1.id).exists())

    def test_followers_count(self):
        self.user_1.following.add(self.user_2)
        self.assertEqual(self.user_1.following.count(), 1)
        self.assertEqual(self.user_2.followers.count(), 1)

    def test_multiple_followings(self):
        user_3 = User.objects.create(username = 'Hermione')
        self.user_1.following.add(self.user_2, user_3)
        user_3.following.add(self.user_2)
        self.assertEqual(self.user_1.following.count(), 2)
        self.assertEqual(self.user_2.followers.count(), 2)

    def test_index(self):
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 2)

    