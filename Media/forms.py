from django import forms
from .models import UploadImage

# создаем форму на базе модели
class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UploadImage   # имя модели с которой строится форма
        fields = ('image', )  # поля, которые должны быть в форме