#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import template
from ..models import Article
from django.utils import timezone
from django.shortcuts import render
from django.template import Template, Context

register = template.Library()


@register.simple_tag
def my_side_content():
    all_article_list = Article.objects.filter(
        pub_date__lte=timezone.now()
    ).filter(published=True).order_by('-pub_date')
    context = {}
    context['all_article_list'] = all_article_list
    context['latest_article_list'] = all_article_list[:10]


    raw_template = """
        <div class="col-xs-12 col-sm-4 side-content">

    <div class="input-group search-area">
        <input type="text" class="form-control" id="search-text" placeholder="Search in kohaku.cc...">
                <span class="input-group-btn">
                    <button id="search-btn" class="btn btn-default" type="button"><span
                            class="glyphicon glyphicon-search" aria-hidden="true"></span></button>
                </span>
    </div>

    <div id="latest-article">
        <h3>Recent</h3>
        <ul class="side-content-ul">
            {% for article in latest_article_list %}
                <li><a href="{% url 'hpc:article_detail' article.url_title %}">{{ article.title }}</a></li>
            {% endfor %}

        </ul>
        <h3>Archives</h3>
        <ul class="side-content-ul">
            <li><a href="{% url 'hpc:all_list' %}">All ({{ all_article_list | length }})</a></li>
            {% regroup all_article_list by pub_date|date:"Y" as year_list %}
            {% for year in year_list %}
                <li><a href="{% url 'hpc:archive_year' year.grouper %}">{{ year.grouper }} ({{ year.list|length }})</a>
                </li>
            {% endfor %}
        </ul>
        <h3>Categories</h3>
        <ul class="side-content-ul">
            {% regroup all_article_list by category as type_list %}
            {% for category in type_list %}
                <li><a href="{% url 'hpc:category_list' category.grouper %}">{{ category.grouper }}
                    ({{ category.list|length }})</a></li>
            {% endfor %}
        </ul>
    </div>
</div>
    """
    t = Template(raw_template)
    c = Context(context)
    html = t.render(c)

    return html
