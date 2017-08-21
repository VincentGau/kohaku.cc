# -*- coding: UTF-8 -*-

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from .models import Article
from django.views import generic
from django.utils import timezone
from haystack.generic_views import SearchView
from haystack.query import SearchQuerySet
import os
import logging
import urllib

logger = logging.getLogger('mylogger')

# *************************使用generic view之前*****************************
# def index(request):
#     latest_article_list = Article.objects.order_by('-pub_date')
#     context = {'latest_article_list': latest_article_list}
#     return render(request, 'hpc/blog_index.html', context)
#     # return HttpResponse("You're in the blog page.")
#
#
# def article_detail(request, url_title):
#     article = get_object_or_404(Article, url_title=url_title)
#     context = {
#         'article': article
#     }
#     return render(request, 'hpc/article_detail.html', context)


# ***************************使用generic view***************************

# pagesize when displaying article list in the table
table_pagesize = 10


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # ip = x_forwarded_for.split(',')[0]
        ip = x_forwarded_for
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def life(request):
    return render(request, 'hpc/life.html')


def about(request):
    ip = get_client_ip(request)
    log_msg = '{0} {1}'.format(ip, request.path)
    logger.info(log_msg)
    return render(request, 'hpc/about.html')


def article_image_upload(request):
    if request.method == "POST":
        myFile = request.FILES.get('myfile', None)
        if not myFile:
            return HttpResponse("No file found")
        # print myFile.name
        des_file = os.path.join("media\\upload", myFile.name)

        with open(des_file, 'wb+') as f:
            for chunk in myFile.chunks():
                f.write(chunk)
        return HttpResponse("Success.")


def test_page(request):
    return render(request, 'hpc/test.html')


"""
the 3 views (archive, category, all article) share the same template 'category.html'
"""


class ArticleListView(generic.ListView):
    model = Article
    template_name = 'hpc/blog_index.html'

    def get_context_data(self, **kwargs):
        ip = get_client_ip(self.request)
        log_msg = '{0} {1}'.format(ip, self.request.path)
        logger.info(log_msg)

        context = super(ArticleListView, self).get_context_data(**kwargs)
        all_article_list = Article.objects.filter(
            pub_date__lte=timezone.now()
        ).filter(published=True).order_by('-pub_date')
        context['all_article_list'] = all_article_list
        context['latest_article_list'] = all_article_list[:10]

        return context


class ArticleDetailView(generic.DetailView):
    model = Article
    template_name = 'hpc/article_detail.html'

    def get_object(self, **kwargs):
        ip = get_client_ip(self.request)
        log_msg = '{0} {1}'.format(ip, self.request.path)
        logger.info(log_msg)
        return get_object_or_404(Article, url_title=self.kwargs.get("url_title"))

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        all_article_list = Article.objects.filter(
            pub_date__lte=timezone.now()
        ).filter(published=True).order_by('-pub_date')
        # context['latest_article_list'] = all_article_list[:10]
        # context['all_article_list'] = all_article_list

        all_article_list_l = list(all_article_list)
        cur_article = Article.objects.get(url_title=self.kwargs.get("url_title"))
        cur_index = all_article_list_l.index(cur_article)
        prev = cur_index - 1 if cur_index > 0 else 9999
        next = cur_index + 1 if cur_index < len(all_article_list_l) - 1 else 9999
        context['prev_article'] = all_article_list_l[cur_index - 1] if prev != 9999 else None
        context['next_article'] = all_article_list_l[cur_index + 1] if next != 9999 else None

        return context


class ArticleCatView(generic.ListView):
    model = Article
    template_name = 'hpc/article_list.html'
    context_object_name = 'article_list'
    paginate_by = table_pagesize

    def get_queryset(self):
        ip = get_client_ip(self.request)
        log_msg = '{0} {1}'.format(ip, self.request.path.encode("utf8"))
        logger.info(log_msg)
        return Article.objects.filter(category=self.kwargs.get("cat")).filter(published=True).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super(ArticleCatView, self).get_context_data(**kwargs)
        all_article_list = Article.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')
        # context['latest_article_list'] = all_article_list[:10]
        # context['all_article_list'] = all_article_list
        cat = self.kwargs.get("cat")
        context['title'] = ":: %s - Haku's ::" % cat.upper()
        context['table_title_1'] = 'Category of '
        context['table_title_2'] = cat

        return context


class ArticleAllView(generic.ListView):
    model = Article
    template_name = 'hpc/article_list.html'
    context_object_name = 'article_list'
    paginate_by = table_pagesize

    def get_queryset(self):
        ip = get_client_ip(self.request)
        log_msg = '{0} {1}'.format(ip, self.request.path)
        logger.info(log_msg)
        return Article.objects.filter(published=True).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super(ArticleAllView, self).get_context_data(**kwargs)
        all_article_list = Article.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')
        # context['latest_article_list'] = all_article_list[:10]
        # context['all_article_list'] = all_article_list
        context['title'] = ":: All articles - Haku's ::"
        context['table_title_1'] = "All articles"
        context['table_title_2'] = ''
        return context


class ArticleMonthArchive(generic.MonthArchiveView):
    allow_empty = True
    allow_future = False
    queryset = Article.objects.filter(published=True)
    template_name = 'hpc/archive_blog.html'
    context_object_name = 'article_list'
    date_field = 'pub_date'
    year_format = '%Y'
    month_format = '%m'

    def get_context_data(self, **kwargs):
        context = super(ArticleMonthArchive, self).get_context_data(**kwargs)
        all_article_list = Article.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')
        # context['latest_article_list'] = all_article_list[:10]
        # context['all_article_list'] = all_article_list

        return context


class ArticleYearArchive(generic.YearArchiveView):
    allow_empty = True
    allow_future = False
    queryset = Article.objects.filter(published=True)
    make_object_list = True
    context_object_name = 'article_list'
    template_name = 'hpc/article_list.html'
    date_field = 'pub_date'
    year_format = '%Y'
    paginate_by = table_pagesize

    def get_context_data(self, **kwargs):
        ip = get_client_ip(self.request)
        log_msg = '{0} {1}'.format(ip, self.request.path)
        logger.info(log_msg)

        context = super(ArticleYearArchive, self).get_context_data(**kwargs)
        all_article_list = Article.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')
        # context['latest_article_list'] = all_article_list[:10]
        # context['all_article_list'] = all_article_list

        context['title'] = ":: Archive of %s - Haku's ::" % self.kwargs.get("year")
        context['table_title_1'] = "Archive of "
        context['table_title_2'] = self.kwargs.get("year")

        return context


class MySearchView(SearchView):
    def get_queryset(self, **kwargs):
        # print kwargs
        # print self.request.META['QUERY_STRING']
        # print self.kwargs
        ip = get_client_ip(self.request)
        log_msg = '{0} {1}?{2}'.format(ip, self.request.path, urllib.unquote(self.request.META['QUERY_STRING']))
        logger.info(log_msg)
        queryset = super(MySearchView, self).get_queryset()
        # further filter queryset based on some set of criteria
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(MySearchView, self).get_context_data(*args, **kwargs)
        all_article_list = Article.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')
        # context['latest_article_list'] = all_article_list[:10]
        # context['all_article_list'] = all_article_list
        return context


def page_not_found():
    return render_to_response('404.html')


def page_error():
    return render_to_response('500.html')
