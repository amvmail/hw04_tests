# yatube/users/form.py
from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')
        text = forms.CharField(label='Текст поста')
        group = forms.CharField(label='Наименование группы')
        image = forms.ImageField(label='Поле для изображения')
