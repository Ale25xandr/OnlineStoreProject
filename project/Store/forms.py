from django.contrib.auth.models import User
from django.forms import PasswordInput
from django_summernote.widgets import SummernoteWidget
from django import forms
from .models import Ads, Response


class AdsForm(forms.ModelForm):
    class Meta:
        model = Ads
        fields = '__all__'
        widgets = {'blog_post': SummernoteWidget()}


class AdsCreateForm(forms.ModelForm):
    class Meta:
        model = Ads
        fields = ['Heading', 'Description', 'Content', 'Category', ]
        widgets = {'Content': SummernoteWidget()}
        labels = {'Heading': 'Заголовок',
                  'Description': 'Описание',
                  'Content': 'Содержимое',
                  'Category': 'Категория'}


class ResponseCreateForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['Text']
        labels = {'Text': 'Текст'}


class RegisterUserForm(forms.ModelForm):
    email = forms.CharField(error_messages={'required': 'Please let us know what to call you!'}, required=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        widgets = {'password': PasswordInput()}

    def save(self, commit=True):
        user = super(RegisterUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class CodeForm(forms.ModelForm):
    code = forms.CharField(max_length=6, label='Code')

    class Meta:
        model = User
        fields = []


class AdsFormUpdate(forms.ModelForm):
    class Meta:
        model = Ads
        fields = ['Heading', 'Description', 'Content', 'Category', ]
        widgets = {'Content': SummernoteWidget()}
        labels = {'Heading': 'Заголовок',
                  'Description': 'Описание',
                  'Content': 'Содержимое',
                  'Category': 'Категория'}

