#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""kohakucc_hostus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""


from django.conf.urls import url, include
from django.contrib import admin
from . import views
import settings
from django.views import static

urlpatterns = [
    url(r'^7/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    # infinite loading
    url(r'^infinite/$', views.infinite, name='infinite'),
    url(r'^comments/', include('django_comments.urls')),
    url(r'^summernote/', include('django_summernote.urls')),
    # url(r'^hpc/', include('hpc.urls')),
    url(r'', include('hpc.urls')),
    url(r'^wx/', include('wechat.urls')),

    url(r'^chat/', include('chat.urls'))

    # 生产环境中去掉这一样，由nginx处理静态文件
    # url(r'^media/(?P<path>.*)$',static.serve,{'document_root':settings.MEDIA_ROOT}),
]