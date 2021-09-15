from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from django.contrib.auth import get_user_model

from api.comments.serializers import CommentSerializer
from core.models import Article, Comment

COMMENT_PUBLIC_URL = reverse('comment_list')


def create_article(**params):
    return Article.objects.create(**params)


class CommentModelTests(TestCase):
    """Tests for article model"""

    def test_create_new_comment_successful(self):
        """Test creating a new article successful"""
        title = 'test'
        content = 'test'
        author = get_user_model().objects.create_user(email='test', password='test123321')
        article = create_article(title=title, author=author, body='testtesttest')
        new_comment = Comment.objects.create(article=article, content=content, author=author)
        comment_list = Comment.objects.all()
        self.assertEqual(new_comment.content, content)
        self.assertEqual(new_comment.id, 1)
        self.assertEqual(comment_list.get(id=1).content, content)


class PublicCommentAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_comment_create_login_required(self):
        payload = {
            'body': 'newBody',
        }
        res = self.client.post(COMMENT_PUBLIC_URL, payload)
        comment_list = Comment.objects.all()
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(comment_list.count(), 0)

    def test_update_comment_in_public_url(self):
        payload_patch = {
            'body': 'newBody',
        }
        res_patch = self.client.patch(COMMENT_PUBLIC_URL, payload_patch)
        self.assertEqual(res_patch.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_list_comments_successful(self):
        author = get_user_model().objects.create_user(email='test@test.com', password='testtesttest')
        article = create_article(title='test', body='test', author=author)
        Comment.objects.create(content='content', author=author, article=article)
        Comment.objects.create(content='content5555', author=author, article=article)

        res = self.client.get(COMMENT_PUBLIC_URL)

        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(comments.count(), 2)
        self.assertEqual(res.data['results'], serializer.data)
        print(res.data['count'])


class PrivateCommentAPITests(TestCase):

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

    def test_create_new_valid_comment(self):
        payload = {
            'content': 'testcontent',
            'article': self.article.id,
        }
        res = self.client.post(COMMENT_PUBLIC_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_comment_create_with_parent_successful(self):
        parent = {
            'content': 'testcontentparent',
            'article': self.article.id,
        }
        self.client.post(COMMENT_PUBLIC_URL, parent)

        parent_res = Comment.objects.get(content=parent['content'])

        comment = {
            'content': 'testcontent',
            'article': self.article.id,
            'parent': parent_res.id
        }
        res = self.client.post(COMMENT_PUBLIC_URL, comment)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # Check if parent don't serialize comment in endpoint list
        res_list = self.client.get(COMMENT_PUBLIC_URL)
        self.assertEqual(res_list.data['count'], 1)

    def test_comment_create_without_content(self):
        payload = {
            'content': 'testcontent',
        }
        res = self.client.post(COMMENT_PUBLIC_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_comment_create_without_article(self):
        payload = {
            'article': self.article.id,
        }
        res = self.client.post(COMMENT_PUBLIC_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_comment_retrieve_successful(self):
        payload = {
            'content': 'testcontentparent',
            'article': self.article.id,
        }
        res = self.client.post(COMMENT_PUBLIC_URL, payload)
        res1 = self.client.get('/api/comments/' + str(res.data['id']) + '/')
        comment = Comment.objects.get(content=payload['content'])
        serializer = CommentSerializer(comment)
        self.assertEqual(res1.status_code, status.HTTP_200_OK)
        self.assertEqual(res1.data['id'], serializer.data['id'])
        self.assertEqual(res1.data['content'], serializer.data['content'])
        self.assertEqual(res1.data['author'], serializer.data['author'])
        self.assertEqual(res1.data['date_posted'], serializer.data['date_posted'])

    def test_update_comment_success(self):
        payload = {
            'content': 'testcontentparent',
            'article': self.article.id,
        }
        res = self.client.post(COMMENT_PUBLIC_URL, payload)

        article = Article.objects.create(title='test', body='123', author=self.user)
        patch_payload = {
            'content': 'testcontentparent53123',
            'article': article.id,
        }
        patch_res = self.client.patch('/api/comments/' + str(res.data['id']) + '/', patch_payload)

        self.assertEqual(patch_res.status_code, status.HTTP_200_OK)
        self.assertTrue(patch_res.data['content'] != res.data['content'])
        self.assertTrue(payload['content'] != patch_res.data['content'])
        self.assertEqual(res.data['date_posted'], patch_res.data['date_posted'])

    def test_comment_update_without_article(self):
        payload = {
            'content': 'testcontentparent',
            'article': self.article.id,
        }
        res = self.client.post(COMMENT_PUBLIC_URL, payload)

        Article.objects.create(title='test', body='123', author=self.user)
        patch_payload = {
            'content': 'testcontentparent53123',
        }

        patch_res = self.client.patch('/api/comments/' + str(res.data['id']) + '/', patch_payload)

        self.assertEqual(patch_res.status_code, status.HTTP_200_OK)
        self.assertTrue(patch_res.data['content'] != res.data['content'])
        self.assertTrue(payload['content'] != patch_res.data['content'])
        self.assertEqual(res.data['date_posted'], patch_res.data['date_posted'])

    def test_comment_update_without_content(self):
        payload = {
            'content': 'testcontentparent',
            'article': self.article.id,
        }
        res = self.client.post(COMMENT_PUBLIC_URL, payload)

        article = Article.objects.create(title='test', body='123', author=self.user)
        patch_payload = {
            'article': article.id
        }

        patch_res = self.client.patch('/api/comments/' + str(res.data['id']) + '/', patch_payload)

        self.assertEqual(patch_res.status_code, status.HTTP_200_OK)
        self.assertTrue(patch_res.data['content'] == res.data['content'])
        self.assertTrue(payload['content'] == patch_res.data['content'])
        self.assertEqual(res.data['date_posted'], patch_res.data['date_posted'])

    def test_delete_comment_success(self):
        payload = {
            'content': 'testcontentparent',
            'article': self.article.id,
        }
        res = self.client.post(COMMENT_PUBLIC_URL, payload)

        delete_res = self.client.delete('/api/comments/' + str(res.data['id']) + '/')
        self.assertEqual(delete_res.status_code, status.HTTP_200_OK)

    def test_comment_create_without_authentication(self):
        self.client.logout()
        payload = {
            'content': 'testcontentparent',
            'article': self.article.id,
        }
        res = self.client.post(COMMENT_PUBLIC_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_comment_without_authentication(self):
        self.client.force_authenticate(self.user)
        new_comment = self.client.post('/api/comments/', {
            'content': 'testcontentparent',
            'article': self.article.id,
        })
        self.assertEqual(new_comment.status_code, status.HTTP_201_CREATED)
        self.client.logout()

        patch_payload = {
            'content': 'testcontentparent31254',
        }
        patch_res = self.client.patch('/api/comments/' + str(new_comment.data['id']) + '/', patch_payload)
        self.assertEqual(patch_res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_comment_from_another_user(self):
        new_user = get_user_model().objects.create_user(
            email='ruschakartur@gmail.com',
            password='testtest'
        )
        new_comment = self.client.post('/api/comments/', {
            'content': 'testcontentparent',
            'article': self.article.id,
        })
        self.assertEqual(new_comment.status_code, status.HTTP_201_CREATED)
        self.client.logout()
        self.client.force_authenticate(new_user)
        patch_payload = {
            'content': '1233211111111',
        }
        patch_res = self.client.patch('/api/comments/' + str(new_comment.data['id']) + '/', patch_payload)
        self.assertEqual(patch_res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(patch_res.data['detail'], self.default_permission_error)

    def test_delete_comment_from_another_user(self):
        new_user = get_user_model().objects.create_user(
            email='ruschakartur@gmail.com',
            password='testtest'
        )
        new_comment = self.client.post('/api/comments/', {
            'content': 'testcontentparent',
            'article': self.article.id,
        })
        self.assertEqual(new_comment.status_code, status.HTTP_201_CREATED)
        self.client.logout()
        self.client.force_authenticate(new_user)
        delete_res = self.client.delete('/api/comments/' + str(new_comment.data['id']) + '/')
        self.assertEqual(delete_res.status_code, status.HTTP_200_OK)
