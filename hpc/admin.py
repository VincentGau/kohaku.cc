from django.contrib import admin

# Register your models here.
import models

from django_summernote.admin import SummernoteModelAdmin


# class ArticleAdmin(admin.ModelAdmin):
#     list_display = ('title', 'url_title', 'author', 'pub_date', 'published')
#     list_filter = ('author', 'published')

class ArticleAdmin(SummernoteModelAdmin):
    list_display = ('title', 'url_title', 'author', 'pub_date', 'published')
    list_filter = ('author', 'published')

admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.Tag)
