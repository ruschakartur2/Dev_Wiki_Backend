from django.test import TestCase

# Create your tests here.

from main import models


class MainTest(TestCase):

    def test_article_create_successful(self):
        article = models.Article(
            title='Test',
            body='TEST test test',
            author='Tester'
        )
        article.save()
