from django.test import TestCase
from django.contrib.auth.models import User
from datetime import datetime
from SignIn.models import UserModel
from SignIn.forms import ProfileForm


class SignInFormsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='qwerty321')

    def tearDown(self):
        User.objects.get(id=1).delete()

    def test_forms_valid(self):
        """
        Testing forms with valid data
        """
        form = ProfileForm(data={'about': 'some data',
                                 'birthday': datetime.now().date(),
                                 'country': 'Ukraine',
                                 'photo': 'default_photo.png',
                                 })
        self.assertTrue(form.is_valid())
        model_type = type(form.instance)
        # check model type
        self.assertEqual(model_type, UserModel)

    def test_forms_invalid(self):
        """
        Testing forms with invalid data
        """
        form = ProfileForm(data={'about': 'some data',
                                 'birthday': datetime.now().date(),
                                 'country': '',
                                 'photo': 'default_photo.png'})
        self.assertFalse(form.is_valid())
