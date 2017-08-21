#!/usr/bin/env python
# -*- coding: utf-8 -*-

def get_model():
    from models import CommentWithTitle
    return CommentWithTitle


def get_form():
    from forms import CommentFormWithTitle
    return CommentFormWithTitle
