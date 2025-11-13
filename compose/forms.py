from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150, label='ユーザー名')
    password = forms.CharField(widget=forms.PasswordInput, label='パスワード')

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("そのユーザー名は既に使われています。")
        return username