from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from datetime import datetime
from django.shortcuts import reverse
from News.forms import PostNewArticle, PostComment
from News.models import Article, Comment
import pytz


class NewsViewsTest(TestCase):
    def setUp(self):
        self.user1     = User.objects.create_user(username='user1', password='qwerty321')
        self.user2     = User.objects.create_user(username='user2', password='qwerty321')
        self.moderator = User.objects.create_user(username='moder', password='qwerty321')
        self.client    = Client()

        group = Group.objects.create(name='Moderator')
        self.moderator.groups.add(group)
        self.moderator.save()

    def tearDown(self):
        User.objects.get(id=1).delete()

    def test_article_list_view(self):
        """
        Testing article list view
        """
        for i in range(25):
            Article.objects.create(Author=self.user1,
                                   Title='Title',
                                   Content='Content',
                                   Date=datetime.now(tz=pytz.UTC))
        self.assertEqual(Article.objects.count(), 25)
        resp = self.client.get(reverse('News_page'))
        self.assertQuerysetEqual(Article.objects.order_by("-Date")[:20],
                                 resp.context['object_list'],
                                 transform=lambda x: x)

    def test_article_detail_view(self):
        """
        Testing article detail view
        """
        article = Article.objects.create(Author=self.user1,
                                         Title='Title',
                                         Content='Content',
                                         Date=datetime.now(tz=pytz.UTC))
        comment = Comment.objects.create(Author=self.user1,
                                         Content='Comment content',
                                         Date=datetime.now(tz=pytz.UTC),
                                         article_id=article)
        # for anonymous user
        resp = self.client.get(reverse('post_detail', kwargs={'pk': article.id, }))
        self.assertEqual(article, resp.context['article'])
        self.assertNotIn('comments', resp.context)

        # for authorized user
        log = self.client.login(username=self.user1.username, password='qwerty321')
        self.assertTrue(log)
        resp = self.client.get(reverse('post_detail', kwargs={'pk': article.id, }))
        self.assertEqual(article, resp.context['article'])
        self.assertIn('comments', resp.context)
        self.assertIn(comment, resp.context['comments'])

    def test_post_new_views(self):
        """
        Testing post new view
        """
        # for anonymous user
        response = self.client.get(reverse('new_post'))
        self.assertRedirects(response, reverse('Login')[:-1] + '?next=' + reverse('new_post'), target_status_code=301)

        # for authorized user
        log = self.client.login(username=self.user1.username, password='qwerty321')
        self.assertTrue(log)
        response = self.client.get(reverse('new_post'))
        self.assertEqual(response.status_code, 200)

        # article
        form = PostNewArticle(data={'Title': 'Article title',
                                    'Content': 'article content',
                                    })
        response = self.client.post(reverse('new_post'), form.data)
        self.assertTrue(Article.objects.filter(id=1).exists())
        article = Article.objects.get(id=1)
        self.assertRedirects(response, reverse('post_detail', kwargs={'pk': article.id}))
        self.assertEqual(article.Title, 'Article title')
        self.assertEqual(article.Content, 'article content')
        self.assertEqual(article.Author, self.user1)

        # comment
        form = PostComment(data={'Content': 'comment content', })
        response = self.client.post(reverse('post_comment', kwargs={'pk': article.id}), form.data)
        self.assertTrue(Comment.objects.filter(id=1).exists())
        comment = Comment.objects.get(id=1)
        self.assertRedirects(response, reverse('post_detail', kwargs={'pk': article.id}))
        self.assertEqual(comment.Content, 'comment content')
        self.assertEqual(comment.article_id, article)
        self.assertEqual(comment.Author, self.user1)

    def test_edit_article(self):
        """
        Testing edit view for article
        """
        # create article
        article = Article.objects.create(Author=self.user1,
                               Title='Article title',
                               Content='Article content',
                               Date=datetime.now(tz=pytz.UTC))
        # for anonymous user
        response = self.client.get(reverse('edit_post', kwargs={'pk': article.id}))
        self.assertRedirects(response,
                             reverse('Login')[:-1] + '?next=' + reverse('edit_post', kwargs={'pk': article.id}),
                             target_status_code=301)

        # for authorized user, but not author
        log = self.client.login(username=self.user2.username, password='qwerty321')
        self.assertTrue(log)
        response = self.client.get(reverse('edit_post', kwargs={'pk': article.id}))
        self.assertContains(response, 'You have no rights to preform this action')

        # for article's author
        log = self.client.login(username=self.user1.username, password='qwerty321')
        self.assertTrue(log)
        response = self.client.get(reverse('edit_post', kwargs={'pk': article.id}))
        self.assertEqual(article, response.context['article'])

        # for moderator
        log = self.client.login(username=self.moderator.username, password='qwerty321')
        self.assertTrue(log)
        response = self.client.get(reverse('edit_post', kwargs={'pk': article.id}))
        self.assertEqual(article, response.context['article'])

        form = PostNewArticle(data={'Title': 'Edited article title',
                                    'Content': 'New article content',
                                    })
        response = self.client.post(reverse('edit_post', kwargs={'pk': article.id, }),  form.data)
        self.assertRedirects(response, reverse('post_detail', kwargs={'pk': article.id, }))
        article = Article.objects.get(id=article.id)
        self.assertEqual(article.Title, 'Edited article title')
        self.assertEqual(article.Content, 'New article content')
        self.assertEqual(article.Author, self.moderator)

    def test_edit_comment(self):
        """
        Testing edit view for comments
        """
        # create article
        article = Article.objects.create(Author=self.user1,
                                         Title='Article title',
                                         Content='Article content',
                                         Date=datetime.now(tz=pytz.UTC))
        comment = Comment.objects.create(Author=self.user1,
                                         Content='Comment content',
                                         Date=datetime.now(tz=pytz.UTC),
                                         article_id=article)

        # for anonymous user
        response = self.client.get(reverse('edit_comment', kwargs={'pk': comment.id}))
        self.assertRedirects(response,
                             reverse('Login')[:-1] + '?next=' + reverse('edit_comment', kwargs={'pk': comment.id}),
                             target_status_code=301)

        # for authorized user, but not author
        log = self.client.login(username=self.user2.username, password='qwerty321')
        self.assertTrue(log)
        response = self.client.get(reverse('edit_comment', kwargs={'pk': comment.id}))
        self.assertContains(response, 'You have no rights to preform this action')

        # for comment's author
        log = self.client.login(username=self.user1.username, password='qwerty321')
        self.assertTrue(log)
        response = self.client.get(reverse('edit_comment', kwargs={'pk': comment.id}))
        self.assertEqual(comment, response.context['comment'])

        # for moderator
        log = self.client.login(username=self.moderator.username, password='qwerty321')
        self.assertTrue(log)
        response = self.client.get(reverse('edit_comment', kwargs={'pk': comment.id}))
        self.assertEqual(comment, response.context['comment'])

        form = PostComment(data={'Content': 'New comment content', })
        response = self.client.post(reverse('edit_comment', kwargs={'pk': comment.id, }),  form.data)
        self.assertRedirects(response, reverse('post_detail', kwargs={'pk': article.id, }))
        comment = Comment.objects.get(id=comment.id)
        self.assertEqual(comment.article_id, article)
        self.assertEqual(comment.Content, 'New comment content')
        self.assertEqual(comment.Author, self.moderator)

    def test_delete_article(self):
        """
        Testing delete view for article
        """
        article = Article.objects.create(Author=self.user1,
                                         Title='Title',
                                         Content='Content',
                                         Date=datetime.now(tz=pytz.UTC))
        comment = Comment.objects.create(Author=self.user1,
                                         Content='Comment content',
                                         Date=datetime.now(tz=pytz.UTC),
                                         article_id=article)
        # for anonymous user
        response = self.client.get(reverse('delete_post', kwargs={'pk': article.id}))
        self.assertRedirects(response,
                             reverse('Login')[:-1] + '?next=' + reverse('delete_post', kwargs={'pk': article.id}),
                             target_status_code=301)

        # for authorized user, but not author
        log = self.client.login(username=self.user2.username, password='qwerty321')
        self.assertTrue(log)
        response = self.client.get(reverse('delete_post', kwargs={'pk': article.id}))
        self.assertContains(response, 'You have no rights to preform this action')

        # for article's author
        log = self.client.login(username=self.user1.username, password='qwerty321')
        self.assertTrue(log)
        response = self.client.get(reverse('delete_post', kwargs={'pk': article.id}))
        self.assertRedirects(response, reverse('News_page'))

        self.assertNotIn(article, Article.objects.all())
        self.assertNotIn(comment, Comment.objects.all())

    def test_delete_comment(self):
        """
        Testing delete view for comments
        """
        article = Article.objects.create(Author=self.user1,
                                         Title='Title',
                                         Content='Content',
                                         Date=datetime.now(tz=pytz.UTC))
        comment = Comment.objects.create(Author=self.user1,
                                         Content='Comment content',
                                         Date=datetime.now(tz=pytz.UTC),
                                         article_id=article)
        # for anonymous user
        response = self.client.get(reverse('delete_comment', kwargs={'pk': comment.id}))
        self.assertRedirects(response,
                             reverse('Login')[:-1] + '?next=' + reverse('delete_comment', kwargs={'pk': comment.id}),
                             target_status_code=301)

        # for authorized user, but not author
        log = self.client.login(username=self.user2.username, password='qwerty321')
        self.assertTrue(log)
        response = self.client.get(reverse('delete_comment', kwargs={'pk': comment.id}))
        self.assertContains(response, 'You have no rights to preform this action')

        # for comment's author
        log = self.client.login(username=self.user1.username, password='qwerty321')
        self.assertTrue(log)
        response = self.client.get(reverse('delete_comment', kwargs={'pk': comment.id}))
        self.assertRedirects(response, reverse('post_detail', kwargs={'pk': article.id}))

        self.assertNotIn(comment, Comment.objects.all())
