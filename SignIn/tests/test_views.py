from django.test import TestCase, Client
from django.contrib.auth.models import User


class SignInViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='qwerty321')
        self.client = Client()

    def tearDown(self):
        User.objects.get(id=1).delete()

    def test_views_login(self):
        # correct login check
        response = self.client.post('/auth/login/', {'username': 'user',
                                                     'password': 'qwerty321'})
        self.assertRedirects(response, '/')
        self.assertTrue(self.user.is_authenticated)
        # incorrect login check
        response = self.client.post('/auth/login/', {'username': 'user23',
                                                     'password': ''})
        self.assertEqual(response.status_code, 200)

    def test_view_regist(self):
        # check simple get request
        response = self.client.get('/auth/registration/')
        self.assertEqual(response.status_code, 200)
        # correct registration check
        response = self.client.post('/auth/registration/', {'username': 'user2',
                                                            'password1': 'qwerty111',
                                                            'password2': 'qwerty111'})
        self.assertRedirects(response, '/auth/login/')
        log = self.client.login(username='user2', password='qwerty111')
        self.assertTrue(log)
        # incorrect registration check
        response = self.client.post('/auth/registration/', {'username': 'user2',
                                                            'password1': 'qwerty111',
                                                            'password2': 'qwerty222'})
        self.assertEqual(response.status_code, 200)

        self.client.logout()

    def test_view_logout(self):
        response = self.client.get('/auth/logout/')
        self.assertRedirects(response, '/', 302)

    def test_profile_view(self):
        # for anonymous user
        response = self.client.get('/auth/profile/')
        self.assertRedirects(response, '/auth/login?next=/auth/profile/', target_status_code=301)
        # for authorized user
        log = self.client.login(username='user', password='qwerty321')
        self.assertTrue(log)
        response = self.client.get('/auth/profile/')
        self.assertTrue(response.status_code, 200)

    def test_profile_edit(self):
        # for anonymous user
        response = self.client.get('/auth/profile/edit/')
        self.assertEqual(response.status_code, 302)

        # for authorized user
        log = self.client.login(username='user', password='qwerty321')
        self.assertTrue(log)
        response = self.client.get('/auth/profile/edit/')
        self.assertTrue(response.status_code, 200)

        response = self.client.post('/auth/profile/edit/', {'about': 'something',
                                                            'photo': 'new_photo.png'})
        self.assertEqual(response.status_code, 200)
