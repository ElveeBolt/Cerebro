from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Division


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        required=True,
        label='Логин пользователя',
        help_text='Last Name',
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите логин...',
            'class': 'form-control'
        })
    )
    name = forms.CharField(
        required=True,
        label='Имя пользователя',
        help_text='Last Name',
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите имя...',
            'class': 'form-control'
        })
    )
    division = forms.ModelChoiceField(
        required=True,
        label='Подразделение',
        help_text='Last Name',
        queryset=Division.objects.all(),
        widget=forms.Select(attrs={
            'placeholder': 'Введите имя...',
            'class': 'form-select'
        })
    )
    comment = forms.CharField(
        required=False,
        label='Комментарий',
        widget=forms.Textarea(attrs={
            'rows': 5,
            'placeholder': 'Введите комментарий...',
            'class': 'form-control'
        })
    )
    password1 = forms.CharField(
        required=True,
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'placeholder': 'Введите пароль...',
            'class': 'form-control'
        })
    )
    password2 = forms.CharField(
        required=True,
        label='Повторите пароль',
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'placeholder': 'Повторите пароль...',
            'class': 'form-control'
        }),
        strip=False
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'name', 'division', 'comment', 'password1', 'password2']


class SignInForm(forms.Form):
    username = forms.CharField(
        required=True,
        label='Логин:',
        help_text='Last Name',
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите логин...',
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        required=True,
        label='Пароль:',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Введите пароль...',
            'class': 'form-control'
        })
    )