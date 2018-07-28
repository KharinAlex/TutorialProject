from django.test import TestCase
from django.contrib.auth.models import User
from datetime import datetime
from News.models import Article, Comment
import pytz


class NewsModelsTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='qwerty321')
        self.user2 = User.objects.create_user(username='user2', password='qwerty321')

    def tearDown(self):
        User.objects.all().delete()

    def test_models_custom(self):
        """
        Testing models
        """
        date = datetime.now(tz=pytz.UTC)
        Article.objects.create(Author=self.user1,
                               Title='Article title',
                               Content='Article content',
                               Date=date)
        article = Article.objects.get(id=1)
        self.assertEqual(article.Author, self.user1)
        self.assertEqual(article.Title, 'Article title')
        self.assertEqual(article.Content, 'Article content')
        self.assertEqual(article.Date, date)
        max_length = article._meta.get_field('Title').max_length
        self.assertEqual(max_length, 150)

        date = datetime.now(tz=pytz.UTC)
        Comment.objects.create(Author=self.user2,
                               Content='Comment content',
                               Date=date,
                               article_id=article)
        comment = Comment.objects.get(id=1)
        self.assertEqual(comment.Author, self.user2)
        self.assertEqual(comment.article_id, article)
        self.assertEqual(comment.Content, 'Comment content')
        self.assertEqual(comment.Date, date)

