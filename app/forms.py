from django import forms
from api.validator import *
from django.forms.widgets import RadioSelect


class PostStatusForm(forms.Form):
    STATUS_CHOICES = [
        ('draft', '下書き'),
        ('private', '非公開'),
        ('publish', '公開')]

    status = forms.ChoiceField(widget=RadioSelect,
                               choices=STATUS_CHOICES,
                               error_messages=ERROR_MESSAGES)


class PostForm(forms.Form):
    title = forms.CharField(required=True,
                            error_messages=ERROR_MESSAGES)
    publish_date = forms.CharField(required=True,
                                   error_messages=ERROR_MESSAGES)
    contents = forms.CharField(required=True,
                               error_messages=ERROR_MESSAGES)


class LoginForm(forms.Form):
    username = forms.CharField(required=True,
                               error_messages=ERROR_MESSAGES)
    password = forms.CharField(required=True,
                               error_messages=ERROR_MESSAGES)
