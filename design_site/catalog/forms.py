import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Request, DesignCategory


class RegistrationForm(UserCreationForm):
    fio = forms.CharField(label='ФИО', max_length=100, required=True,
                          #widget=forms.TextInput(attrs={'pattern': '^[а-яА-ЯёЁ\s\-]*$'})
                          )
    username = forms.CharField(label='Логин', max_length=100, required=True,
                               #widget=forms.TextInput(attrs={'pattern': '^[a-zA-Z\-]*$'})
                               )
    email = forms.EmailField(label='Email', required=True)
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)
    consent = forms.BooleanField(label='Согласие на обработку данных', required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = CustomUser
        fields = ['fio', 'username', 'email', 'password1', 'password2', 'consent']

    def clean_fio(self):
        fio = self.cleaned_data.get('fio')
        if not fio:
            raise forms.ValidationError('Это поле обязательно для заполнения.')
        if not re.match(r'^[а-яА-ЯёЁ\s\-]*$', fio):
            raise forms.ValidationError('Поле ФИО должно содержать только кириллические буквы, дефис и пробелы.')
        return fio

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError('Это поле обязательно для заполнения.')
        if not re.match(r'^[a-zA-Z\-]*$', username):
            raise forms.ValidationError('Логин должен содержать только латинские буквы и дефис.')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким логином уже существует.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('Это поле обязательно для заполнения.')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Пароли не совпадают.')
        return password2


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин', max_length=100, required=True)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput, required=True)
    error_message = None

    def add_error_message(self, message):
        self.error_message = message



class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['title', 'description', 'category','request_photo']


class DesignCategoryForm(forms.ModelForm):
    class Meta:
        model = DesignCategory
        fields = ['name']
