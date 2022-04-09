# posts/tests/test_comments.py
import unittest
import shutil
from django.conf import settings
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Post, Group, User, Comment
from posts.forms import PostForm, CommentForm


class CommentFormCreateTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_with_post = User.objects.create_user(
            username='testusername'
        )
        cls.post = Post.objects.create(
            text='Тестовый текст33',
            author=cls.user_with_post
        )
        cls.group = Group.objects.create(
            title='group_form',
            slug='9999',
            description='for test form'
        )
        cls.form = CommentForm()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user_with_post)

    def test_create_guest_new_comment(self):
        """Проверка невозможности создания тестового комментария без авторизации."""
        post_id = self.post.pk
        form_data = {
            'text': 'Тестовый коментарий от неавторизованного пользователя',
        }
        self.guest_client.post(
            reverse('posts:add_comment', kwargs={'post_id': post_id}),
            data=form_data,
            follow=True,
        )
        self.assertFalse(Comment.objects.filter(
            text='Тестовый коментарий от неавторизованного пользователя').exists())

    # @unittest.skip('пропускаем')
    def test_create_view_comment(self):
        """Проверка правильности создания и отображения комментария."""
        self.authorized_client.force_login(self.user_with_post)
        # создание дополнительного тестового поста
        self.post = Post.objects.create(
            text='Тестовый текст33',
            author=self.user_with_post,
        )
        # проверка отображения нового поста на страниц post detail
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.pk}))
        self.assertEqual = (response.context['detail_post'], 'Тестовый текст33')
        post_id = self.post.pk
        form_data = {
            'text': 'Тестовый коментарий от авторизованного пользователя',
        }
        self.authorized_client.post(
            reverse('posts:add_comment', kwargs={'post_id': post_id}),
            data=form_data,
            follow=True,
        )
        self.assertTrue(Comment.objects.filter(
            text='Тестовый коментарий от авторизованного пользователя').exists())