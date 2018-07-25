from django.test import TestCase
from django.contrib.auth.models import User
from datetime import datetime
from SignIn.models import UserModel


class SignInModelsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='qwerty321')

    def tearDown(self):
        User.objects.get(id=1).delete()

    def test_models_default(self):
        """
        Testing default profile create
        """
        model = UserModel.objects.get(id=1)

        self.assertEqual(model.user_id, self.user)
        self.assertEqual(model.about, "")
        self.assertEqual(model.birthday, datetime.strptime("1970-01-01", "%Y-%m-%d").date())
        self.assertEqual(model.country, "")
        self.assertEqual(model.photo, "default_photo.png")
        model.delete()

    def test_models_custom(self):
        """
        Testing custom profile create
        """
        UserModel.objects.get(id=1).delete()
        UserModel.objects.create(user_id=self.user,
                                 about="about",
                                 birthday="2018-07-20",
                                 country="Ukraine",
                                 photo="some_photo.png")
        model = UserModel.objects.get(id=2)
        self.assertEqual(model.user_id, self.user)
        self.assertEqual(model.about, "about")
        self.assertEqual(model.birthday, datetime.strptime("2018-07-20", "%Y-%m-%d").date())
        self.assertEqual(model.country, "Ukraine")
        self.assertEqual(model.photo, "some_photo.png")
        max_length = model._meta.get_field('country').max_length
        self.assertEqual(max_length, 15)
        model.delete()
