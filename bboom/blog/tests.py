from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Post, User


class APITest(APITestCase):
    """ API Testing """

    def setUp(self) -> None:
        self.user: User = User.objects.create_user(
            name='test',
            email='test@gmail.com',
            password='qwerty'
        )
        self.client = APIClient()

    def test_all_users(self):
        User.objects.create(
            name='test2',
            email='test2@gmail.com',
            password='dqwerty2'
        )

        url = reverse('users')
        response = self.client.get(url)

        assert len(response.json()) == 2
        assert response.status_code == 200

    def test_all_posts_of_user(self):
        another_user = User.objects.create(
            name='test4',
            email='test4@gmail.com',
            password='dioawdoawdqwerty4')

        Post.objects.create(
            title='Test',
            body='test body',
            user=self.user
        )

        Post.objects.create(
            title='Test2',
            body='test body2',
            user=self.user
        )

        Post.objects.create(
            title='Test3',
            body='test body3',
            user=another_user
        )

        url = reverse('user-post', kwargs={'user': self.user.id})
        self.client.force_login(self.user)
        response = self.client.get(url)

        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_delete_post(self):
        post = Post.objects.create(
            title='Test',
            body='test body',
            user=self.user
        )
        self.client.force_login(self.user)
        url = reverse('del-post', kwargs={'pk': post.id})
        response = self.client.delete(url)
        assert response.status_code == 204
