# posts/tests/test_pagination.py
from posts.posts_global import QUANT_OF_POSTS, QUANT_OF_POSTS_HALF
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Post, Group, User


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
            self.assertEqual(len(
                response.context.get("page_obj")), QUANT_OF_POSTS)

    def test_second_page_contains_five_records(self):
        """Проверка paginator - 5 постов 2 страница."""
        urls_names = {
            reverse('posts:posts'),
            reverse('posts:group_posts', kwargs={'slug': '99'}),
            reverse('posts:profile', kwargs={'username': 'testusername'})}
        for test_url in urls_names:
            response = self.client.get(test_url + '?page=2')
            self.assertEqual(len(
                response.context.get("page_obj")), QUANT_OF_POSTS_HALF)
