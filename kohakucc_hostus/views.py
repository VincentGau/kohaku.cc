from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from hpc.models import Article
from django.http import HttpResponse
import json
from django.template import Template, Context

from django.template.loader import get_template
import logging

logger = logging.getLogger('mylogger')

# pagesize for infinite loading
pagesize = 6


def index(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # ip = x_forwarded_for.split(',')[0]
        ip = x_forwarded_for
    else:
        ip = request.META.get('REMOTE_ADDR')
    log_msg = '{0} index'.format(ip)
    logger.info(log_msg)

    all_article_list = Article.objects.filter(published=True).order_by('-pub_date')
    latest_article_list = all_article_list[:10]
    context = {
        'all_article_list'   : all_article_list,
        'articles_for_this_page'   : all_article_list[:pagesize],
        'latest_article_list': latest_article_list
    }
    return render(request, 'hpc/index.html', context)


def infinite(request):
    if request.method == 'GET' and 'page' in request.GET:
        total_num = Article.objects.count()
        page = int(request.GET['page'])
        start_index = pagesize * (page - 1)
        end_index = pagesize * page if pagesize * page < total_num else total_num

        # start_index >= total_num means all articles were loaded
        if start_index >= total_num:
            data = {'end': 'true', 'html': 'false'}
            return HttpResponse(json.dumps(data, ensure_ascii=False))

        articles_for_this_page = Article.objects.filter(published=True).order_by('-pub_date')[start_index:end_index]

        # Important: synchronized the raw_template string with the index.html and blog_index.html template
        raw_template = """
            {% load comments %}
            {% for article in articles_for_this_page %}
                <article class="article-in-list">
                    {% get_comment_count for article as comment_count %}
                    <h1><a href="{{ article.get_absolute_url }}">{{ article.title | title }}</a></h1>
                    <time>{{ article.pub_date }}</time>
                    <div class="separator">|</div>
                    <a href="{{ article.get_absolute_url }}#comment-list"><span>{{ comment_count }} comments</span></a>
                    <div class="article-content">
                        <p>
                            {{ article.content | linebreaks | truncatechars_html:100 }}
                            <a href="{% url 'hpc:article_detail' article.url_title %}">
                                <nobr>Read more>></nobr>
                            </a>
                        </p>
                    </div>
                </article>
            {% endfor %}
        """
        # t = Template(raw_template)
        t = get_template('hpc/infinite_article_template.html')
        # c = Context({'articles_for_this_page': articles_for_this_page})
        # html = t.render(c)
        html = t.render({'articles_for_this_page': articles_for_this_page})

        data = {"html": html, 'page': page, 'end': 'false'}
        if pagesize * page >= total_num:
            data["end"] = "true"

        return HttpResponse(json.dumps(data, ensure_ascii=False))
