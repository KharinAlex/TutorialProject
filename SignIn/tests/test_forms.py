from django.test import TestCase
from datetime import datetime
from SignIn.models import UserModel
from SignIn.forms import ProfileForm


class SignInFormsTest(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

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
        self.assertEqual(model_type, UserModel)
        self.assertEqual(form.data['about'], 'some data')
        self.assertEqual(form.data['birthday'], datetime.now().date())
        self.assertEqual(form.data['country'], 'Ukraine')
        self.assertEqual(form.data['photo'], 'default_photo.png')

    def test_forms_invalid(self):
        """
        Testing forms with invalid data
        """
        form = ProfileForm(data={'about': 'some data',
                                 'birthday': datetime.now().date(),
                                 'country': '',
                                 'photo': 'default_photo.png'})
        self.assertFalse(form.is_valid())
