# yatube/users/form.py
from django import forms
from django.core.exceptions import ValidationError
# from pytils.translit import slugify  # взято из теории
from django.utils.text import slugify  # взято из инета

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'image', 'group')
        text = forms.CharField(label='Текст поста')
        image = forms.ImageField(label='Изображение')
        group = forms.CharField(label='Наименование группы')

    # Валидация поля slug
    def clean_slug(self):
        """Обрабатывает случай, если slug не уникален."""
        cleaned_data = super().clean()
        slug = cleaned_data.get('slug')
        if not slug:
            title = cleaned_data.get('title')
            slug = slugify(title)[:100]
        if Post.objects.filter(slug=slug).exists():
            raise ValidationError(
                f'Адрес "{slug}" уже существует, '
                'придумайте уникальное значение'
            )
        return slug
