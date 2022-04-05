# posts/tests/test_urls.py
from http import HTTPStatus

from django.test import TestCase, Client
from posts.models import Post, Group, User


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='testusername')
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user
        )
        cls.group = Group.objects.create(
            title='group',
            slug='99',
            description='for test'
        )

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем пользователя
        self.user = User.objects.create_user(username='test')
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(self.user)

    def test_about_url_exists_at_desired_location(self):
        """Проверка адреса /about/author/ и шаблона ."""
        response = self.guest_client.get('/about/author/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about/about_author.html',
                                'Используется неправильный шаблон.')

    def test_about_tech_url_exists_at_desired_location(self):
        """Проверка адреса /about/tech/ и шаблона ."""
        response = self.guest_client.get('/about/tech/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about/tech.html',
                                'Используется неправильный шаблон.')

    def test_group_slug_url_exists_at_desired_location(self):
        """Проверка адреса /group/slug/ и шаблона."""
        response = self.guest_client.get(f'/group/{self.group.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/group_list.html',
                                'Используется неправильный шаблон.')
        response = self.authorized_client.get(f'/group/{self.group.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/group_list.html',
                                'Используется неправильный шаблон.')

    def test_profile_url_exists_at_desired_location(self):
        """Проверка адреса /profile/username/ и шаблона."""
        response = self.guest_client.get(f'/profile/{self.post.author}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/profile.html',
                                'Используется неправильный шаблон.')
        response = self.authorized_client.get(f'/profile/{self.post.author}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/profile.html',
                                'Используется неправильный шаблон.')

    def test_post_id_edit_url_exists_at_desired_location(self):
        """Проверка адреса и шаблона для автор. пользователя /posts/post_id/edit/
         на редакторование."""
        response = self.authorized_client.get(f'/posts/{self.post.pk}/edit/')
        if self.user == self.post.author:
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'posts/create_post.html',
                                    'Используется неправильный шаблон.')

    def test_post_detail_url_exists_at_desired_location(self):
        """Проверка адреса и шаблона деталей поста /posts/post_id/."""
        response = self.authorized_client.get(f'/posts/{self.post.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_detail.html',
                                'Используется неправильный шаблон.')

    def test_index_url_exists_at_desired_location(self):
        """Проверка доступности адреса  и шаблона индексной страницы /."""
        address = '/'
        response = self.guest_client.get(address)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'posts/index.html',
                                'Используется неправильный шаблон.')
        response = self.authorized_client.get(address)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'posts/index.html',
                                'Используется неправильный шаблон.')

    def test_create_post_url_exists_at_desired_location(self):
        """Проверка доступности адреса для автор_пользователя /create/."""
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/create_post.html',
                                'Используется неправильный шаблон.')

    def test_unexisting_url_exists_at_desired_location(self):
        """Проверка доступности несуществующего адреса для пользователя."""
        response = self.authorized_client.get('/unexisting/')
        self.assertEqual(response.status_code, 404)
