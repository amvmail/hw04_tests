# yatube/posts/tests/forms.py

import shutil

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse
from posts.forms import PostForm
from posts.models import Group, Post

User = get_user_model()


class PostFormCreateTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_with_post = User.objects.create_user(
            username='testusername'
        )
        cls.post = Post.objects.create(
            text='Тестовый текст3',
            author=cls.user_with_post
        )
        cls.group = Group.objects.create(
            title='group_form',
            slug='9999',
            description='for test form'
        )
        cls.form = PostForm()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user_with_post)

    def test_create_post(self):
        """Проверка правильности создания тестового поста."""
        self.authorized_client.force_login(self.user_with_post)
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый текст4',
            'group': self.group.pk
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, (reverse(
            'posts:profile', kwargs={'username': 'testusername'})), 302)
        test_post_1 = Post.objects.get(id=self.post.pk + 1)
        test_author_1 = User.objects.get(username='testusername')
        test_group_1 = Group.objects.get(pk=1)

        self.assertEqual(test_post_1.text, 'Тестовый текст4')
        self.assertEqual(str(test_author_1), 'testusername')
        self.assertEqual(str(test_group_1), 'group_form')
        self.assertEqual(Post.objects.count(), posts_count + 1,
                         'Новый пост не сохранен')

    def test_edit_post(self):
        """Проверка редактирования поста."""
        self.authorized_client.force_login(self.user_with_post)
        # присваиваю id поста и группу для редактирования + проверка
        if self.post.text == 'Тестовый текст3':
            post_id = self.post.pk
        response = self.authorized_client.get(
           reverse('posts:post_detail', kwargs={'post_id': post_id}))
        self.assertEqual = (self.post.author, {self.user_with_post})
        self.assertEqual = (self.post.text, 'Тестовый текст3')
        self.assertEqual = (self.group.title, 'group_form')
        # редактирование поста
        form_data = {
            'text': 'Тестовый текст3 edited',
            'group': self.group.pk
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': post_id}),
            data=form_data,
            follow=True
        )
        self.post_1 = response.context
        self.assertEqual = (self.post.text, 'Тестовый текст3 edited')
        self.assertEqual = (self.group.title, 'group_form')
        self.assertTrue(
            Post.objects.filter(
                group='1',
                text='Тестовый текст3 edited',
            ).exists()
        )

    def test_create_guest_new_post(self):
        """Проверка невозможности создания тестового поста без авторизации."""
        form_data = {
            'text': 'Тестовый пост от неавторизованного пользователя',
            'group': self.group.id
        }
        self.guest_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )
        self.assertFalse(Post.objects.filter(
            text='Тестовый пост от неавторизованного пользователя').exists())

    def test_post_with_picture(self):
        """Проверка загрузки тестового поста с изображением."""
        self.authorized_client.force_login(self.user_with_post)
        count_posts = Post.objects.count()
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        form_data = {
            'text': 'Пост с image',
            'group': self.group.id,
            'image': uploaded
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )
        test_post_2 = Post.objects.get(id=self.group.id + 1)
        test_author = User.objects.get(username='testusername')
        test_group = Group.objects.get(title='group_form')
        self.assertEqual(Post.objects.count(), count_posts + 1)
        self.assertRedirects(response, (reverse(
            'posts:profile', kwargs={'username': 'testusername'})), 302)
        self.assertEqual(test_post_2.text, 'Пост с image')
        self.assertEqual(test_author.username, 'testusername')
        self.assertEqual(test_group.title, 'group_form')
