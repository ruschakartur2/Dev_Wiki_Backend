from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from django.contrib.auth import get_user_model

from api.articles.serializers import ArticlePublicSerializer, ArticleSerializer
from core.models import Article, Tag

ARTICLE_PUBLIC_URL = reverse('article_list')


def create_tag(**params):
    return Tag.objects.create(**params)



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

    def test_update_article_in_public_url(self):
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
            email='1@j.com',
            password='testtest'
        )
        self.default_permission_error = 'You do not have permission to perform this action.'
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

    def test_create_article_body_with_less_symbols(self):
        payload = {
            'title': 'test title',
            'body': '123456789',
            'update_tags': '[]'
        }
        res = self.client.post(ARTICLE_PUBLIC_URL, payload)
        self.assertEqual(res.data['body'][0], 'Ensure this value has at least 10 characters (it has 9).')
        self.assertEqual(res.data['body'][0].code, 'min_length')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_unique_title_article(self):
        payload = {
            'title': 'testTitle',
            'body': 'newBodyffffffffffffffffffffffffffffffff',
            'update_tags': 'test'
        }
        self.client.post(ARTICLE_PUBLIC_URL, payload)
        payload2 = {
            'title': 'testTitle',
            'body': 'newBody432fffffffffffffffffffff',
            'update_tags': 'test534543'
        }
        self.assertEqual(payload['title'], payload2['title'])
        res2 = self.client.post(ARTICLE_PUBLIC_URL, payload2)
        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_article_without_title(self):
        payload = {
            'body': 'newBodyffffffffffffffffffff',
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
            'body': 'testffffffffffffffffffffffffffffffffffffffff'
        }
        res = self.client.post(ARTICLE_PUBLIC_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_article_by_slug_success(self):
        payload = {
            'title': 'Arturka',
            'body': 'newBodyfffffffffffffffffffffffffffff',
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
            'body': 'newBodyfffffffffffffffffffffffffffffffffffff',
            'update_tags': 'test'
        }
        patch_payload = {
            'title': 'New title',
            'body': 'hahahah new bodyffffff',
            'update_tags': 'Badaboy'
        }
        res = self.client.post(ARTICLE_PUBLIC_URL, payload)
        patch_res = self.client.patch('/api/articles/' + res.data['slug'] + '/', patch_payload)
        self.assertEqual(patch_res.status_code, status.HTTP_200_OK)
        self.assertTrue(patch_res.data['title'] != res.data['title'])
        self.assertTrue(payload['title'] != patch_res.data['title'])
        self.assertEqual(res.data['author'], patch_res.data['author'])

    def test_delete_article_success(self):
        payload = {
            'title': 'Arturka',
            'body': 'newBodyfffffffffffffffffffffffffffffffffffff',
            'update_tags': 'test'
        }
        res = self.client.post(ARTICLE_PUBLIC_URL, payload)

        delete_res = self.client.delete('/api/articles/' + res.data['slug'] + '/')
        self.assertEqual(delete_res.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_article_without_authentication(self):
        new_article = self.client.post('/api/articles/', {
            'title': 'testtestMoretest',
            'body': 'ultratestffffffffffffffffffffffffff',
            'update_tags': '[]'
        })
        self.assertEqual(new_article.status_code, status.HTTP_201_CREATED)
        self.client.logout()

        patch_payload = {
            'title': '123',
            'body': '321ffffffffffffffffffffffffffffffff',
            'update_tags': '231'
        }
        patch_res = self.client.patch('/api/articles/' + new_article.data['slug'] + '/', patch_payload)
        self.assertEqual(patch_res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_article_from_another_user(self):
        new_user = get_user_model().objects.create_user(
            email='ruschakartur@gmail.com',
            password='testtest'
        )
        new_article = self.client.post('/api/articles/', {
            'title': 'testtestMoretest',
            'body': 'ultratestfffffffffffffffffffffffffffffff',
            'update_tags': 'megaTESTT'
        })
        self.assertEqual(new_article.status_code, status.HTTP_201_CREATED)
        self.client.logout()
        self.client.force_authenticate(new_user)
        patch_payload = {
            'title': '123',
            'body': '321fffffffffffffffffffffffffff',
            'update_tags': '231'
        }
        patch_res = self.client.patch('/api/articles/' + new_article.data['slug'] + '/', patch_payload)
        self.assertEqual(patch_res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(patch_res.data['detail'], self.default_permission_error)

    def test_delete_article_from_another_user(self):
        new_user = get_user_model().objects.create_user(
            email='ruschakartur1@gmail.com',
            password='testtest1'
        )
        new_article = self.client.post('/api/articles/', {
            'title': 'testtestMoretest',
            'body': 'ultratestfdsfdsfdsfdsfdsfdsfs',
            'update_tags': 'megaTESTT'
        })
        self.assertEqual(new_article.status_code, status.HTTP_201_CREATED)
        self.client.logout()
        self.client.force_authenticate(new_user)
        delete_res = self.client.delete('/api/articles/' + new_article.data['slug'] + '/')
        self.assertEqual(delete_res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(delete_res.data['detail'], self.default_permission_error)

    def test_get_newest_articles(self):
        self.client.post('/api/articles/', {
            'title': 'testtestMoretest',
            'body': 'ultratestfsdfsdfsdgggfsfds',
            'update_tags': 'megaTESTT'
        })
        self.client.post('/api/articles/', {
            'title': '2',
            'body': 'ultratest2ffsdfdsfdsfdsfds',
            'update_tags': 'megaT2'
        })
        self.client.post('/api/articles/', {
            'title': '3',
            'body': 'ultratest3fdsfsafsadfsdfsdfsd',
            'update_tags': 'megaTESTT3'
        })
        res = self.client.get('/api/articles/?new=1/')
        articles = Article.objects.all().order_by('created_at')
        serializer = ArticlePublicSerializer(articles, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    def test_get_newest_articles_failed(self):
        self.client.post('/api/articles/', {
            'title': 'testtestMoretest',
            'body': 'ultratestfsdfsadfdsfdsfds',
            'update_tags': 'megaTESTT'
        })
        self.client.post('/api/articles/', {
            'title': '2',
            'body': 'ultratest2dasfdsgfdsgsfsad',
            'update_tags': 'megaT2'
        })
        self.client.post('/api/articles/', {
            'title': '3',
            'body': 'ultratest3fffffffffffffff',
            'update_tags': 'megaTESTT3'
        })
        res = self.client.get('/api/articles/?ordering=created_at/')
        # Change order in reverse stack
        articles = Article.objects.all().order_by('-created_at')
        serializer = ArticlePublicSerializer(articles, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(res.data['results'], serializer.data)

    def test_get_popular_articles(self):
        res1 = self.client.post('/api/articles/', {
            'title': 'testtestMoretest',
            'body': 'ultratest',
            'update_tags': 'megaTESTT'
        })
        res2 = self.client.post('/api/articles/', {
            'title': '2',
            'body': 'ultratest2',
            'update_tags': 'megaT2'
        })
        res3 = self.client.post('/api/articles/', {
            'title': '3',
            'body': 'ultratest3',
            'update_tags': 'megaTESTT3'
        })
        self.client.get('/api/articles/' + res1.data['slug'] + '/')
        self.client.get('/api/articles/' + res1.data['slug'] + '/')
        self.client.get('/api/articles/' + res1.data['slug'] + '/')
        self.client.get('/api/articles/' + res2.data['slug'] + '/')
        self.client.get('/api/articles/' + res3.data['slug'] + '/')
        self.client.get('/api/articles/' + res2.data['slug'] + '/')
        self.client.get('/api/articles/' + res1.data['slug'] + '/')

        res = self.client.get('/api/articles/?popular=1')
        self.assertEqual(res.data['results'][0]['visits'], 4)
        articles = Article.objects.all().order_by('-visits')
        serializer = ArticlePublicSerializer(articles, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    def test_get_popular_articles_failed(self):
        """Added don't needed slash in url and functional not working"""
        res1 = self.client.post('/api/articles/', {
            'title': 'testtestMoretest',
            'body': 'ultratest',
            'update_tags': 'megaTESTT'
        })
        res2 = self.client.post('/api/articles/', {
            'title': '2',
            'body': 'ultratest2',
            'update_tags': 'megaT2'
        })
        res3 = self.client.post('/api/articles/', {
            'title': '3',
            'body': 'ultratest3',
            'update_tags': 'megaTESTT3'
        })

        self.client.get('/api/articles/' + res1.data['slug'] + '/')
        self.client.get('/api/articles/' + res1.data['slug'] + '/')
        self.client.get('/api/articles/' + res1.data['slug'] + '/')
        self.client.get('/api/articles/' + res2.data['slug'] + '/')
        self.client.get('/api/articles/' + res3.data['slug'] + '/')
        self.client.get('/api/articles/' + res2.data['slug'] + '/')
        self.client.get('/api/articles/' + res1.data['slug'] + '/')
        # Added don't needed slash in url and functional not working
        res = self.client.get('/api/articles/?popular=1/')
        # Change order in reverse stack
        articles = Article.objects.all().order_by('-visits')
        serializer = ArticlePublicSerializer(articles, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'][0]['visits'], 1)
        self.assertNotEqual(res.data['results'], serializer.data)
