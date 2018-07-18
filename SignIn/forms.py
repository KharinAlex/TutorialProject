from django.forms import ModelForm
from .models import UserModel


class ProfileForm(ModelForm):
    class Meta:
        model = UserModel
        fields = ('about', 'birthday', 'country', 'photo')

