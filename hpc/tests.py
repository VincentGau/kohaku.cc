from django.test import TestCase

# Create your tests here.

from django.utils import timezone
import datetime
from .models import Article
from django.core.urlresolvers import reverse


def create_article(title, author, content, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Article.objects.create(title=title, author=author, content=content, pub_date=time)


class ArticleViewsTest(TestCase):
    def test_index_view_with_no_article(self):
        response = self.client.get(reverse('hpc:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No articles are available.")
        self.assertQuerysetEqual(response.context['latest_article_list'], [])

    def test_index_view_with_a_past_question(self):
        """
        Questions with a pub_date in the past should be displayed on the
        index page.
        """
        create_article(title='past article', author='1', content='1', days=-30)
        response = self.client.get(reverse('hpc:index'))
        self.assertQuerysetEqual(
            response.context['latest_article_list'],
            ['<Article: past article>']
        )

    def test_index_view_with_a_future_question(self):
        """
        Questions with a pub_date in the future should not be displayed on
        the index page.
        """
        create_article(title='future article', author='1', content='1', days=30)
        response = self.client.get(reverse('hpc:index'))
        self.assertContains(response, "No articles are available.")
        self.assertQuerysetEqual(response.context['latest_article_list'], [])

    def test_index_view_with_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        should be displayed.
        """
        create_article(title='past article', author='1', content='1', days=-30)
        create_article(title='future article', author='1', content='1', days=30)
        response = self.client.get(reverse('hpc:index'))
        self.assertQuerysetEqual(
            response.context['latest_article_list'],
            ['<Article: past article>']
        )

    def test_index_view_with_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_article(title='past article1', author='1', content='1', days=-30)
        create_article(title='past article2', author='1', content='1', days=-10)
        response = self.client.get(reverse('hpc:index'))
        self.assertQuerysetEqual(
            response.context['latest_article_list'],
            ['<Article: past article2>', '<Article: past article1>']
        )


class SearchViewTest(TestCase):
    def test_search_view_with_no_result(self):
        response = self.client.get(reverse('hpc:my_haystack_search'), kwargs={'q': 'test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Take a bite")
