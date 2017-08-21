#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django import forms
from django_comments.forms import CommentForm
from models import CommentWithTitle


class CommentFormWithTitle(CommentForm):
    title = forms.CharField(max_length=300)

    def get_comment_create_data(self):
        # Use the data of the superclass, and add in the title field
        data = super(CommentFormWithTitle, self).get_comment_create_data()
        data['title'] = self.cleaned_data['title']
        return data
