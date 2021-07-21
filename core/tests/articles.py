from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, force_authenticate

from django.contrib.auth import get_user_model

from api.articles.serializers import ArticlePublicSerializer, ArticleSerializer
from core.models import Article, Tag

ARTICLE_PUBLIC_URL = reverse('article_list')


def create_tag(**params):
    return Tag.objects.create(**params)


class ArticleModelTests(TestCase):
    """Tests for article model"""

    def test_create_new_article_successful(self):
        """Test creating a new article successful"""
        title = 'test'
        body = 'test'
        author = get_user_model().objects.create_user(email='test@gm.com', password='testtesttest')
        new_article = Article.objects.create(title=title, body=body, author=author)
        self.assertEqual(new_article.title, title)
        self.assertEqual(new_article.id, 1)


class PublicArticleAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_login_required(self):
        payload = {
            'title': 'testTitle',
            'body': 'newBody',
            'update_tags': 'test'
        }

        res = self.client.post(ARTICLE_PUBLIC_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_article_without_login(self):
        payload_patch = {
            'title': 'testTitle1',
            'body': 'newBody',
            'update_tags': 'test'
        }
        res_patch = self.client.patch(ARTICLE_PUBLIC_URL, payload_patch)
        self.assertEqual(res_patch.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_list_articles_successful(self):
        author = get_user_model().objects.create_user(email='test@gm.com', password='testtesttest')

        Article.objects.create(title='test123', body='content', author=author)
        Article.objects.create(title='test321', body='content5555', author=author)

        res = self.client.get(ARTICLE_PUBLIC_URL)

        articles = Article.objects.all()
        serializer = ArticlePublicSerializer(articles, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)


class PrivateArticleAPITests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@test.com',
            'testtest'
        )
        self.client = APIClient()
        self.client.login(email='test@test.com', password='test@test.com')
        self.client.force_authenticate(self.user)

    def test_create_new_valid_article(self):
        payload = {
            'title': 'testTitle',
            'body': 'newBody',
            'update_tags': 'test'
        }
        res = self.client.post(ARTICLE_PUBLIC_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_article_without_title(self):
        payload = {
            'body': 'newBody',
            'update_tags': 'test'
        }
        res = self.client.post(ARTICLE_PUBLIC_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_article_without_body(self):
        payload = {
            'title': 'new_title',
            'update_tags': 'test'
        }
        res = self.client.post(ARTICLE_PUBLIC_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_article_without_tags(self):
        payload = {
            'title': 'new_title',
            'body': 'test'
        }
        res = self.client.post(ARTICLE_PUBLIC_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_article_by_slug_success(self):
        payload = {
            'title': 'Arturka',
            'body': 'newBody',
            'update_tags': 'test'
        }
        res = self.client.post(ARTICLE_PUBLIC_URL, payload)
        res1 = self.client.get('/api/articles/' + res.data['slug'] + '/')
        article = Article.objects.get(title='Arturka')
        serializer = ArticleSerializer(article)
        self.assertEqual(res1.status_code, status.HTTP_200_OK)
        self.assertEqual(res1.data['id'], serializer.data['id'])
        self.assertEqual(res1.data['title'], serializer.data['title'])
        self.assertEqual(res1.data['tags'], serializer.data['tags'])

    def test_update_article_success(self):
        payload = {
            'title': 'Arturka',
            'body': 'newBody',
            'update_tags': 'test'
        }
        patch_payload = {
            'title': 'New title',
            'body': 'hahahah new body',
            'update_tags': 'Badaboy'
        }
        res = self.client.post(ARTICLE_PUBLIC_URL, payload)
        patch_res = self.client.patch('/api/articles/' + res.data['slug'] + '/', patch_payload)
        self.assertEqual(patch_res.status_code, status.HTTP_200_OK)
        self.assertTrue(patch_res.data['title'] != res.data['title'])
        self.assertTrue(payload['title'] != patch_res.data['title'])
        self.assertEqual(res.data['author'], patch_res.data['author'])
