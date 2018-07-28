from django.test import TestCase
from django.contrib.auth.models import User
from News.models import Article, Comment
from News.forms import PostNewArticle, PostComment


class NewsFormsTest(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_forms_valid(self):
        """
        Testing forms with valid data
        """
        # PostNewArticle
        form = PostNewArticle(data={'Title': 'Article title',
                                    'Content': 'article content',
                                 })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.data['Title'], 'Article title')
        self.assertEqual(form.data['Content'], 'article content')
        model_type = type(form.instance)
        self.assertEqual(model_type, Article)

        # PostComment
        form = PostComment(data={'Content': 'comment content', })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.data['Content'], 'comment content')
        model_type = type(form.instance)
        self.assertEqual(model_type, Comment)

    def test_forms_invalid(self):
        """
        Testing forms with invalid data
        """
        form = PostNewArticle(data={'Title': 'Article title',
                                 })
        self.assertFalse(form.is_valid())

        form = PostComment(data={'Content': '', })
        self.assertFalse(form.is_valid())
