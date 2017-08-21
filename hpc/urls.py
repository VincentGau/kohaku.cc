#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url, include, handler404, handler500

from . import views
from haystack.query import SearchQuerySet


handler404 = 'hpc.views.page_not_found'
handler500 = 'hpc.views.page_error'

app_name = 'hpc'
urlpatterns = [
    # # url(r'^$', views.index, name='index'),
    # url(r'^blog/$', views.index, name='index'),
    # url(r'^blog/(?P<url_title>[\S]+)/$', views.article_detail, name='article_detail'),

    url(r'^blog/$', views.ArticleListView.as_view(), name='blog_index'),
    url(r'^life/$', views.life, name='life'),
    url(r'^about/$', views.about, name='about'),
    url(r'^blog/all/$', views.ArticleAllView.as_view(), name='all_list'),
    url(r'^blog/(?P<url_title>[^/]+)/$', views.ArticleDetailView.as_view(), name='article_detail'),
    url(r'^blog/archive/(?P<year>\d{4})/$', views.ArticleYearArchive.as_view(), name='archive_year'),
    url(r'^blog/archive/(?P<year>\d{4})/(?P<month>\d{2})/$', views.ArticleMonthArchive.as_view(), name='archive_month'),
    url(r'^blog/category/(?P<cat>[\S]+)/$', views.ArticleCatView.as_view(), name='category_list'),

    url(r'^upload/$', views.article_image_upload, name='article_image_upload'),
    url(r'^testpage/$', views.test_page, name='test_page'),


    url(r'^search/', views.MySearchView.as_view(), name='my_haystack_search'),

]
