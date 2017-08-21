from __future__ import unicode_literals
from django.core.urlresolvers import reverse

from django.db import models
from django.contrib import admin
from django_comments.moderation import CommentModerator, moderator
from django.template import loader
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.core.mail import send_mail
import logging

logger = logging.getLogger('mylogger')


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# Create your models here.

class Tag(models.Model):
    ''' Tag '''
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=100)  # title of the article
    url_title = models.CharField(max_length=100, unique=True)  # title (in English) in the article url
    author = models.CharField(max_length=20)
    category = models.CharField(max_length=20, default='life')
    tags = models.ManyToManyField(Tag)
    content = models.TextField()
    pub_date = models.DateTimeField('date published')
    published = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        # return reverse('hpc:article_detail', args=[str(self.url_title)])
        return reverse('hpc:article_detail', kwargs={'url_title': self.url_title})


class ArticleModerator(CommentModerator):
    email_notification = True

    # enable_field = 'enable_comments'

    def email(self, comment, content_object, request):
        """
        Send email notification of a new comment to site staff when email
        notifications have been requested.

        """
        if not self.email_notification:
            return
        recipient_list = [manager_tuple[1] for manager_tuple in settings.MANAGERS]
        t = loader.get_template('comments/comment_notification_email.txt')
        c = {
            'comment'       : comment,
            'content_object': content_object,
            'site'          : get_current_site(request),
        }
        subject = ('[%(site)s] New comment posted on "%(object)s"') % {
            'site'  : get_current_site(request).name,
            'object': content_object,
        }
        message = t.render(c)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, fail_silently=True)

        par = comment.parent
        if par:
            t1 = loader.get_template('comments/comment_reply_notification_email.txt')
            c1 = {
                'comment'       : comment,
                'content_object': content_object,
                'site'          : get_current_site(request),
            }
            subject1 = ('[%(site)s] Your comment posted on "%(object)s" is replied') % {
                'site'  : get_current_site(request).name,
                'object': content_object,
            }
            message1 = t1.render(c1)
            recipient_list1 = [par.user_email]
            send_mail(subject1, message1, settings.DEFAULT_FROM_EMAIL, recipient_list1, fail_silently=True)
            # print par.user_email

        # log
        ip = get_client_ip(request)
        log_msg = 'New comment on {0} from {1}'.format(content_object, ip)
        logger.info(log_msg)


moderator.register(Article, ArticleModerator)
