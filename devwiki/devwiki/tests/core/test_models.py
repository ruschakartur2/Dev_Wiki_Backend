from unittest import TestCase

from django.contrib.auth import get_user_model

from devwiki.devwiki.pkg.core.models import Article


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
