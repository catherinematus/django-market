from typing import re
from django import forms
from django.contrib.auth import password_validation

from .models import Order, Review
from django.contrib.auth.models import User
import re


class ContactForm(forms.ModelForm):
    # user_name = forms.CharField(label="Имя", widget=forms.TextInput, required=True)
    # phone = forms.CharField(label="Телефон", widget=forms.TextInput, required=True)

    class Meta:
        model = Order
        fields = [
            'user_name',
            'phone',
            'delivery',
            'payment',
        ]

        widgets = {
            'delivery': forms.RadioSelect,
            'payment': forms.RadioSelect,
        }

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        regexp_string = r'^\+375-(25|29|33|44|17)-[0-9]{3}-[0-9]{2}-[0-9]{2}$'
        match = re.fullmatch(regexp_string, phone)
        if not match:
            self.add_error('phone', 'Пожалуйста, введите правильный номер в формате +375-**-***-**-**')
            # raise forms.ValidationError(f'Введите правильный номер телефона в формате +375-хх-ххх-хх-хх')
        return self.cleaned_data


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            self.add_error('username', f'Пользователь с логином {username} не найден в системе.')
            # raise forms.ValidationError(f'Пользователь с логином {username} не найден в системе.')
        user = User.objects.filter(username=username).first()
        if user:
            if not user.check_password(password):
                self.add_error('password', 'Неверный пароль')
                # raise forms.ValidationError("Неверный пароль")
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password']


class RegisterUserForm(forms.ModelForm):
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput)
    first_name = forms.CharField(label="Имя", widget=forms.TextInput, required=True)
    last_name = forms.CharField(label="Фамилия", widget=forms.TextInput, required=False)
    email = forms.EmailField(label="Почта", widget=forms.EmailInput, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'
        self.fields['password2'].label = 'Подтвердите пароль'
        self.fields['first_name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['email'].label = 'Электронная почта'

    def clean_user_name(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            self.add_error('username', f'Пользователь с логином {username} уже существует. Придумайте другой логин')
        return self.cleaned_data

    def clean_password2(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password2 != password:
            self.add_error('password2', 'Пароль не подтвержден')
        return self.cleaned_data

    def save(self, commit=True):
        user = super(RegisterUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class ReviewForm(forms.ModelForm):
    # your_name = forms.CharField(label="Ваше имя", max_length=100)
    # comment = forms.TextField()

    class Meta:
        model = Review
        fields = ['author',
                  'text',
                  ]
