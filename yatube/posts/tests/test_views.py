# posts/tests/test_views.py
from django import forms
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Post, Group

User = get_user_model()


class PostViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_with_post = User.objects.create_user(username='testusername')
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user_with_post
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
        # Создаем второй клиент
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(self.user)

    def test_pages_users_correct_template(self):
        """Проверка URL-адреса на использование соответствующего шаблона."""
        templates_pages_names = {
            'posts/index.html': reverse('posts:posts'),
            'posts/group_list.html': reverse(
                'posts:group_posts', kwargs={'slug': '99'}),
            'posts/profile.html': reverse(
                'posts:profile', kwargs={'username': 'test'}),
            'posts/post_detail.html': (
                reverse('posts:post_detail',
                        kwargs={'post_id': self.post.pk})),
            'posts/create_post.html': reverse('posts:post_create')
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.guest_client.get(reverse('posts:posts'))
        test_object = response.context["page_obj"][0]
        post_text = test_object.text
        post_author = test_object.author.username
        self.assertEqual(post_text, 'Тестовый текст',
                         'Получение текста - ошибка.')
        self.assertEqual(post_author, 'testusername',
                         'Получение текста - ошибка.')

    def test_group_posts_show_correct_context(self):
        """Шаблон группы group posts сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse
                                              ('posts:group_posts',
                                               kwargs={'slug': '99'}))
        test_object = response.context["group"]
        group_title_0 = test_object.title
        group_slug_0 = test_object.slug
        self.assertEqual(group_title_0, 'group')
        self.assertEqual(group_slug_0, '99')

    def test_profile_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': 'testusername'}))
        self.assertEqual = (response.context['author'], 'testusername')
        self.assertEqual = (response.context['posts'], 'Тестовый текст')

    def test_post_detail_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.pk}))
        self.assertEqual = (response.context['detail_post'], 'Тестовый текст')
        self.assertEqual = (response.context['post_count'], 1)

    def test_create_post_show_correct_context(self):
        """Шаблон create post сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_edit_post_show_correct_context(self):
        """Шаблон edit post сформирован с правильным контекстом."""
        # логинимся нужным пользователем
        self.authorized_client.force_login(self.user_with_post)
        response = self.authorized_client.get(
            reverse('posts:post_edit',
                    kwargs={'post_id': f'{self.user_with_post.pk}'}),
        )
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_create_view_post(self):
        """Проверка правильности создания и отображения поста."""
        self.authorized_client.force_login(self.user_with_post)
        # создание дополнительного тестового поста
        self.post = Post.objects.create(
            text='Тестовый текст2',
            author=self.user_with_post,
            # title='group_test'
        )
        self.group = Group.objects.create(
            title='group_test',
            slug='999',
            description='for create post test'
        )
        # проверка отображения нового поста на странице нужной группы
        response = self.authorized_client.get(reverse
                                              ('posts:group_posts',
                                               kwargs={'slug': '999'}))
        test_group_object = response.context['group']
        self.assertEqual(str(test_group_object), 'group_test',
                         'Нет нового поста на странице нужной группы')
        self.assertNotEqual(str(test_group_object), 'group',
                            'Новый пост отображается в чужой группе')
        # проверки index страницы на появление нового поста
        response = self.authorized_client.get(reverse('posts:posts'))
        test_object = response.context['page_obj'][0]
        test_text = test_object.text
        test_author = test_object.author.username
        self.assertEqual(test_text, 'Тестовый текст2',
                         'Получение текста2 - ошибка.')
        self.assertEqual(test_author, 'testusername',
                         'Проверка author2 - ошибка.')
        self.assertEqual(str(test_group_object), 'group_test',
                         'Проверка группы - ошибка.')
        # проверки отображения нового поста на страниц profile
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': 'testusername'}))
        self.assertEqual = (response.context['author'], 'testusername',
                            'На странице профайла не отображается'
                            'новое сообщение {self.user_with_post}')
        self.assertEqual = (response.context['posts'], 'Тестовый текст2'
                            'На странице профайла не отображается'
                            'новое сообщение {self.user_with_post}')


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='testusername')
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            description='Тестовое описание',
            slug='99',
        )
        cls.posts = []
        for i in range(15):
            cls.posts.append(Post(
                text=f'Тестовый пост {i}',
                author=cls.user,
                group=cls.group))
        Post.objects.bulk_create(cls.posts)

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='Test')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_first_page_contains_ten_records(self):
        """Проверка paginator - 10 постов 1 страница."""
        urls_names = {
            reverse('posts:posts'),
            reverse('posts:group_posts', kwargs={'slug': '99'}),
            reverse('posts:profile', kwargs={'username': 'testusername'})}
        for test_url in urls_names:
            response = self.client.get(test_url)
            self.assertEqual(len(response.context.get("page_obj")), 10)

    def test_second_page_contains_three_records(self):
        """Проверка paginator - 5 постов 2 страница."""
        urls_names = {
            reverse('posts:posts'),
            reverse('posts:group_posts', kwargs={'slug': '99'}),
            reverse('posts:profile', kwargs={'username': 'testusername'})}
        for test_url in urls_names:
            response = self.client.get(test_url + '?page=2')
            self.assertEqual(len(response.context.get("page_obj")), 5)
