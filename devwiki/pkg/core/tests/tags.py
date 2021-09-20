from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from django.contrib.auth import get_user_model

from api.tags.serializers import TagsSerializer
from core.models import Article, Tag

TAG_PUBLIC_URL = reverse('tag_list')


def create_article(**params):
    return Article.objects.create(**params)


class TagModelTests(TestCase):
    """Tests for article model"""

    def test_create_new_comment_successful(self):
        """Test creating a new article successful"""
        title = 'test'
        author = get_user_model().objects.create_user(email='test', password='test123321')
        create_article(title='1233321', author=author, body='testtesttest')
        new_tag = Tag.objects.create(title=title)
        tag_list = Tag.objects.all()
        self.assertEqual(new_tag.title, title)
        self.assertEqual(new_tag.id, 1)
        self.assertEqual(tag_list.get(id=1).title, title)


class PublicTagAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_tag_create_login_required(self):
        payload = {
            'title': 'newBody',
        }
        res = self.client.post(TAG_PUBLIC_URL, payload)
        tag_list = Tag.objects.all()
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(tag_list.count(), 0)

    def test_update_tag_in_public_url(self):
        payload_patch = {
            'title': 'newTitle',
        }
        res_patch = self.client.patch(TAG_PUBLIC_URL, payload_patch)
        self.assertEqual(res_patch.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_list_tags_successful(self):
        author = get_user_model().objects.create_user(email='test@test.com', password='testtesttest')
        create_article(title='test', body='test', author=author)
        Tag.objects.create(title='title1')
        Tag.objects.create(title='title2')

        res = self.client.get(TAG_PUBLIC_URL)

        tags = Tag.objects.all()
        serializer = TagsSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(tags.count(), 2)
        self.assertEqual(res.data, serializer.data)


class PrivateTagAPITests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@test.com',
            'testtest'
        )
        self.article = create_article(title='testtest', body='testbody', author=self.user)
        self.default_permission_error = 'You do not have permission to perform this action.'
        self.client = APIClient()
        self.client.login(email='test@test.com', password='test@test.com')
        self.client.force_authenticate(self.user)

    def test_create_new_valid_tag(self):
        payload = {
            'title': 'Tagggg',
            'articles': [self.article]

        }
        res = self.client.post(TAG_PUBLIC_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_tag_create_without_title(self):
        payload = {
            'title': '',
            'articles': [self.article]
        }
        res = self.client.post(TAG_PUBLIC_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_tag_retrieve_successful(self):
        payload = {
            'title': 'tagggg',
            'articles': [self.article]

        }
        res = self.client.post(TAG_PUBLIC_URL, payload)
        res1 = self.client.get('/api/tags/' + str(res.data['id']) + '/')
        tag = Tag.objects.get(title=payload['title'])
        serializer = TagsSerializer(tag)
        self.assertEqual(res1.status_code, status.HTTP_200_OK)
        self.assertEqual(res1.data['id'], serializer.data['id'])
        self.assertEqual(res1.data['title'], serializer.data['title'])
        self.assertEqual(res1.data['articles'], serializer.data['articles'])

    def test_tag_update_success(self):
        payload = {
            'title': 'titletitle',
            'articles': [self.article],
        }
        res = self.client.post(TAG_PUBLIC_URL, payload)
        print(res)
        article = Article.objects.create(title='test', body='123', author=self.user)
        patch_payload = {
            'title': 'testcontentparent53123',
            'articles': [article.id],
        }
        patch_res = self.client.patch('/api/tags/' + str(res.data['id']) + '/', patch_payload)

        self.assertEqual(patch_res.status_code, status.HTTP_200_OK)
        self.assertTrue(payload['title'] != patch_res.data['title'])
        self.assertTrue(payload['articles'] != patch_res.data['articles'])

    def test_create_tag_title_unique(self):
        payload = {
            'title': 'titletitle',
        }

        self.client.post(TAG_PUBLIC_URL, payload)
        demo_res = self.client.post(TAG_PUBLIC_URL, payload)

        self.assertEqual(demo_res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_tag_success(self):
        payload = {
            'title': 'testtitle',
        }
        res = self.client.post(TAG_PUBLIC_URL, payload)

        delete_res = self.client.delete('/api/tags/' + str(res.data['id']) + '/')
        self.assertEqual(delete_res.status_code, status.HTTP_204_NO_CONTENT)

    def test_tag_create_without_authentication(self):
        self.client.logout()
        payload = {
            'content': 'testcontentparent',
        }
        res = self.client.post(TAG_PUBLIC_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_tag_without_authentication(self):
        self.client.force_authenticate(self.user)
        new_tag = self.client.post('/api/tags/', {
            'title': 'title'
        })
        self.assertEqual(new_tag.status_code, status.HTTP_201_CREATED)
        self.client.logout()

        patch_payload = {
            'title': 'testcontentparent31254',
        }
        patch_res = self.client.patch('/api/tags/' + str(new_tag.data['id']) + '/', patch_payload)
        self.assertEqual(patch_res.status_code, status.HTTP_401_UNAUTHORIZED)
